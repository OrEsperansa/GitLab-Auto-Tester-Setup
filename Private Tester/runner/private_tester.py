from __future__ import annotations

"""Run hidden pytest tests against one submitted student commit."""

from dataclasses import dataclass
import logging
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

import requests


DEFAULT_AUTO_TESTER_PROJECT = "{course_path}/auto-tests/python-auto-tester"
LOGGER = logging.getLogger("private_tester")


@dataclass(frozen=True)
class GitLabConfig:
    base_url: str
    api_url: str


@dataclass(frozen=True)
class GitCredentials:
    username: str
    token: str


@dataclass(frozen=True)
class ProjectCheckout:
    project_path: str
    ref: str


@dataclass(frozen=True)
class Exercise:
    group: str
    repo: str

    @property
    def tests_path(self) -> str:
        return f"tests/{self.group}/{self.repo}"

    @property
    def status_name(self) -> str:
        return f"autotest/{self.group}/{self.repo}"


@dataclass(frozen=True)
class StudentSubmission:
    project_path: str
    commit_sha: str
    exercise: Exercise


@dataclass(frozen=True)
class AutotestConfig:
    course_name: str
    course_path: str
    gitlab: GitLabConfig
    credentials: GitCredentials
    hidden_tests: ProjectCheckout
    student: StudentSubmission
    private_pipeline_url: str


def main() -> int:
    configure_logging()
    config = load_config()
    log_config(config)
    mark_tests_running(config)

    try:
        pytest_exit_code = run_autotest(config)
    except Exception as exc:
        LOGGER.error("Auto tester failed before pytest could finish: %s", exc)
        mark_setup_failed(config)
        return 1

    mark_tests_finished(config, pytest_exit_code)
    return pytest_exit_code


def load_config() -> AutotestConfig:
    course_path = course_root_path()
    student_project_path = env("STUDENT_PROJECT_PATH")
    exercise_group, exercise_repo = parse_student_path(student_project_path, course_path)

    return AutotestConfig(
        course_name=os.getenv("COURSE_NAME", course_path),
        course_path=course_path,
        gitlab=load_gitlab_config(),
        credentials=GitCredentials(
            username=env("ROOT_CI_USERNAME", "oauth2"),
            token=env("ROOT_CI_TOKEN"),
        ),
        hidden_tests=ProjectCheckout(
            project_path=env(
                "PYTHON_AUTO_TESTER_PROJECT_PATH",
                DEFAULT_AUTO_TESTER_PROJECT.format(course_path=course_path),
            ),
            ref=env("PYTHON_AUTO_TESTER_REF", "main"),
        ),
        student=StudentSubmission(
            project_path=student_project_path,
            commit_sha=env("STUDENT_COMMIT_SHA"),
            exercise=Exercise(exercise_group, exercise_repo),
        ),
        private_pipeline_url=env("CI_PIPELINE_URL", ""),
    )


def load_gitlab_config() -> GitLabConfig:
    base_url = os.getenv("GITLAB_BASE_URL") or os.getenv("CI_SERVER_URL")
    if not base_url:
        raise RuntimeError("GITLAB_BASE_URL or CI_SERVER_URL is not set")

    base_url = base_url.rstrip("/")
    api_url = os.getenv("GITLAB_API_URL") or os.getenv("CI_API_V4_URL") or f"{base_url}/api/v4"

    return GitLabConfig(base_url=base_url, api_url=api_url.rstrip("/"))


def log_config(config: AutotestConfig) -> None:
    LOGGER.info("Course: %s", config.course_name)
    LOGGER.info("Course path: %s", config.course_path)
    LOGGER.info("Student repo: %s", config.student.project_path)
    LOGGER.info("Student commit: %s", config.student.commit_sha)
    LOGGER.info("Hidden test folder: %s", config.student.exercise.tests_path)


def mark_tests_running(config: AutotestConfig) -> None:
    post_student_status(config, "running", "Hidden Python tests are running.")


def mark_setup_failed(config: AutotestConfig) -> None:
    post_student_status(config, "failed", "Auto tester setup failed.")


def mark_tests_finished(config: AutotestConfig, pytest_exit_code: int) -> None:
    if pytest_exit_code == 0:
        post_student_status(config, "success", "Hidden Python tests passed.")
        return

    post_student_status(config, "failed", "Hidden Python tests failed.")


def post_student_status(config: AutotestConfig, state: str, description: str) -> None:
    set_commit_status(
        config.gitlab.api_url,
        config.credentials.token,
        config.student.project_path,
        config.student.commit_sha,
        config.student.exercise.status_name,
        state,
        description,
        config.private_pipeline_url,
    )


def run_autotest(config: AutotestConfig) -> int:
    with tempfile.TemporaryDirectory(prefix="sigit-autotest-") as temp_dir_name:
        workspace = Path(temp_dir_name)
        git_env = authenticated_git_env(config.credentials, workspace)
        hidden_tests_dir = workspace / "python-auto-tester"
        student_dir = workspace / "student-submission"

        clone_hidden_tests(config, hidden_tests_dir, git_env)
        clone_student_submission(config, student_dir, git_env)

        tests_dir = find_tests_dir(hidden_tests_dir, config.student.exercise)
        return run_pytest(student_dir, tests_dir)


def authenticated_git_env(credentials: GitCredentials, workspace: Path) -> dict[str, str]:
    git_env = os.environ.copy()
    git_env.update(
        {
            "GIT_ASKPASS": str(make_askpass(workspace)),
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_USERNAME": credentials.username,
            "GIT_PASSWORD": credentials.token,
        }
    )
    return git_env


def clone_hidden_tests(config: AutotestConfig, destination: Path, git_env: dict[str, str]) -> None:
    LOGGER.info("Cloning Python Auto Tester...")
    clone_and_checkout(
        config.gitlab.base_url,
        config.hidden_tests.project_path,
        config.hidden_tests.ref,
        destination,
        git_env,
    )


def clone_student_submission(config: AutotestConfig, destination: Path, git_env: dict[str, str]) -> None:
    LOGGER.info("Cloning student submission...")
    clone_and_checkout(
        config.gitlab.base_url,
        config.student.project_path,
        config.student.commit_sha,
        destination,
        git_env,
    )


def find_tests_dir(hidden_tests_dir: Path, exercise: Exercise) -> Path:
    tests_dir = hidden_tests_dir / "tests" / exercise.group / exercise.repo
    if not tests_dir.is_dir():
        raise RuntimeError(f"Missing hidden tests folder: {exercise.tests_path}")
    return tests_dir


def run_pytest(student_dir: Path, tests_dir: Path) -> int:
    LOGGER.info("Running pytest...")
    pytest_env = os.environ.copy()
    pytest_env["PYTHONPATH"] = str(student_dir)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(tests_dir),
            "-q",
            "--tb=short",
        ],
        cwd=student_dir,
        env=pytest_env,
        check=False,
    )
    return result.returncode


def parse_student_path(project_path: str, course_path: str) -> tuple[str, str]:
    pattern = (
        rf"^{re.escape(course_path)}/students/"
        r"sigituser[0-9]{2}-group/"
        r"([A-Za-z0-9_.-]+)/"
        r"([A-Za-z0-9_.-]+)$"
    )
    match = re.fullmatch(pattern, project_path, flags=re.IGNORECASE)
    if not match:
        expected = f"{course_path}/students/sigituserXX-group/ExerciseName/ExerciseRepo"
        raise RuntimeError(f"Student project path must match: {expected}")
    return match.group(1).lower(), match.group(2).lower()


def clone_and_checkout(
    gitlab_url: str,
    project_path: str,
    ref_or_sha: str,
    destination: Path,
    git_env: dict[str, str],
) -> None:
    clone_url = build_clone_url(gitlab_url, project_path)
    run(["git", "clone", "--quiet", "--no-tags", clone_url, str(destination)], env=git_env)
    run(["git", "-C", str(destination), "checkout", "--quiet", "--detach", ref_or_sha], env=git_env)


def build_clone_url(gitlab_url: str, project_path: str) -> str:
    return f"{gitlab_url.rstrip('/')}/{quote(project_path, safe='/')}.git"


def make_askpass(temp_dir: Path) -> Path:
    script = temp_dir / "git-askpass.sh"
    script.write_text(
        "#!/bin/sh\n"
        "case \"$1\" in\n"
        "  *Username*) printf '%s\\n' \"$GIT_USERNAME\" ;;\n"
        "  *Password*) printf '%s\\n' \"$GIT_PASSWORD\" ;;\n"
        "  *) printf '\\n' ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    script.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    return script


def set_commit_status(
    api_url: str,
    token: str,
    project_id: str,
    sha: str,
    name: str,
    state: str,
    description: str,
    target_url: str,
) -> None:
    payload = {
        "state": state,
        "name": name,
        "context": name,
        "description": description,
    }
    if target_url:
        payload["target_url"] = target_url

    response = requests.post(
        f"{api_url}/projects/{quote(str(project_id), safe='')}/statuses/{sha}",
        headers={"PRIVATE-TOKEN": token},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()


def run(command: list[str], env: dict[str, str] | None = None) -> None:
    LOGGER.info("$ %s", " ".join(command))
    subprocess.run(command, env=env, check=True)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
    )


def course_root_path() -> str:
    return env("COURSE_PATH", os.getenv("CI_PROJECT_ROOT_NAMESPACE"))


def env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"{name} is not set")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
