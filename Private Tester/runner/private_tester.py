from __future__ import annotations

"""Run hidden pytest tests against one submitted student commit.

This script intentionally keeps the design simple:
- student repositories start this project as a downstream GitLab pipeline;
- this project owns the token that can clone the private tests;
- tests are selected by repository path convention instead of by extra config.
- the CI image already contains Python, Git, pytest, and requests, so no
  internet/package installation is needed during the job.

The functions below are split around the few ideas that are easy to get wrong:
deriving the test folder from the GitLab path, cloning private repositories
without putting tokens in URLs, and reporting the final result back to GitLab.
"""

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


def main() -> int:
    """Coordinate one complete autotest run.

    The downstream student pipeline has already told us which project path and
    exact commit SHA to test. This function gathers defaults, announces a
    running status in GitLab, clones the hidden tests and student code into a
    temporary workspace, runs pytest, then posts the final pass/fail status.
    """

    configure_logging()

    course_path = course_root_path()
    course_name = os.getenv("COURSE_NAME", course_path)
    gitlab_url = os.getenv("GITLAB_BASE_URL") or os.getenv("CI_SERVER_URL")
    if not gitlab_url:
        raise RuntimeError("GITLAB_BASE_URL or CI_SERVER_URL is not set")
    gitlab_url = gitlab_url.rstrip("/")
    api_url = (os.getenv("GITLAB_API_URL") or os.getenv("CI_API_V4_URL") or f"{gitlab_url}/api/v4").rstrip("/")
    token = env("ROOT_CI_TOKEN")
    token_user = env("ROOT_CI_USERNAME", "oauth2")

    student_project_path = env("STUDENT_PROJECT_PATH")
    student_commit_sha = env("STUDENT_COMMIT_SHA")
    private_pipeline_url = env("CI_PIPELINE_URL", "")

    auto_tester_project = env(
        "PYTHON_AUTO_TESTER_PROJECT_PATH",
        DEFAULT_AUTO_TESTER_PROJECT.format(course_path=course_path),
    )
    auto_tester_ref = env("PYTHON_AUTO_TESTER_REF", "main")

    exercise_group, exercise_repo = parse_student_path(student_project_path, course_path)
    status_name = f"autotest/{exercise_group}/{exercise_repo}"

    LOGGER.info("Course: %s", course_name)
    LOGGER.info("Course path: %s", course_path)
    LOGGER.info("Student repo: %s", student_project_path)
    LOGGER.info("Student commit: %s", student_commit_sha)
    LOGGER.info("Hidden test folder: tests/%s/%s", exercise_group, exercise_repo)

    set_commit_status(
        api_url,
        token,
        student_project_path,
        student_commit_sha,
        status_name,
        "running",
        "Hidden Python tests are running.",
        private_pipeline_url,
    )

    try:
        with tempfile.TemporaryDirectory(prefix="sigit-autotest-") as temp_dir_name:
            temp_dir = Path(temp_dir_name)
            askpass = make_askpass(temp_dir)
            git_env = os.environ.copy()
            git_env.update(
                {
                    "GIT_ASKPASS": str(askpass),
                    "GIT_TERMINAL_PROMPT": "0",
                    "GIT_USERNAME": token_user,
                    "GIT_PASSWORD": token,
                }
            )

            auto_tester_dir = temp_dir / "python-auto-tester"
            student_dir = temp_dir / "student-submission"

            LOGGER.info("Cloning Python Auto Tester...")
            clone_and_checkout(gitlab_url, auto_tester_project, auto_tester_ref, auto_tester_dir, git_env)

            LOGGER.info("Cloning student submission...")
            clone_and_checkout(gitlab_url, student_project_path, student_commit_sha, student_dir, git_env)

            tests_dir = auto_tester_dir / "tests" / exercise_group / exercise_repo
            if not tests_dir.is_dir():
                raise RuntimeError(f"Missing hidden tests folder: tests/{exercise_group}/{exercise_repo}")

            LOGGER.info("Running pytest...")
            pytest_env = os.environ.copy()
            pytest_env["PYTHONPATH"] = str(student_dir)
            pytest_result = subprocess.run(
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

        if pytest_result.returncode == 0:
            set_commit_status(
                api_url,
                token,
                student_project_path,
                student_commit_sha,
                status_name,
                "success",
                "Hidden Python tests passed.",
                private_pipeline_url,
            )
        else:
            set_commit_status(
                api_url,
                token,
                student_project_path,
                student_commit_sha,
                status_name,
                "failed",
                "Hidden Python tests failed.",
                private_pipeline_url,
            )
        return pytest_result.returncode

    except Exception as exc:
        LOGGER.error("Auto tester failed before pytest could finish: %s", exc)
        set_commit_status(
            api_url,
            token,
            student_project_path,
            student_commit_sha,
            status_name,
            "failed",
            "Auto tester setup failed.",
            private_pipeline_url,
        )
        return 1


def parse_student_path(project_path: str, course_path: str) -> tuple[str, str]:
    """Turn the student repository path into the hidden test folder key.

    The course layout itself is the mapping mechanism. A repo at
    `sigitxviii/students/sigituser00-group/basic/04-house-application` maps to
    hidden tests at `tests/basic/04-house-application`. Keeping this as a convention avoids a
    separate manifest that teachers would have to maintain and debug.
    """

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
    """Clone a GitLab project and pin it to one branch, tag, or commit.

    Both repositories are cloned the same way: the hidden tests are pinned to
    their configured branch, while the student repository is pinned to the exact
    merge-request commit SHA. Pinning the student checkout avoids accidentally
    testing a branch after it has moved.
    """

    clone_url = build_clone_url(gitlab_url, project_path)
    run(["git", "clone", "--quiet", "--no-tags", clone_url, str(destination)], env=git_env)
    run(["git", "-C", str(destination), "checkout", "--quiet", "--detach", ref_or_sha], env=git_env)


def build_clone_url(gitlab_url: str, project_path: str) -> str:
    """Build a clone URL from a GitLab project path.

    GitLab project paths can contain spaces, such as `Auto Tests`, so the URL
    must be encoded. Slashes stay as slashes because they separate GitLab groups
    and subgroups.
    """

    return f"{gitlab_url.rstrip('/')}/{quote(project_path, safe='/')}.git"


def make_askpass(temp_dir: Path) -> Path:
    """Create a temporary Git credential helper for the CI token.

    Git needs credentials to clone private projects, but putting the token in
    the clone URL would make logs and error messages riskier. `GIT_ASKPASS`
    lets Git ask a tiny temporary script for the username/password instead.
    """

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
    """Post the visible pass/fail status back to the student commit.

    The downstream pipeline's own result lives in `Private Tester`, but students
    and merge requests need a result on the submitted commit. GitLab commit
    statuses provide that bridge without adding MR comments or artifacts.
    """

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
    """Run setup commands that should stop the pipeline when they fail.

    This wrapper is used for infrastructure steps such as cloning repositories.
    Pytest is not run through this helper because a failing test suite is an
    expected outcome that still needs custom status reporting.
    """

    printable = " ".join(command)
    LOGGER.info("$ %s", printable)
    subprocess.run(command, env=env, check=True)


def configure_logging() -> None:
    """Make GitLab job logs readable without using scattered print calls."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
    )


def course_root_path() -> str:
    """Find the course root group path from GitLab's built-in variables.

    GitLab exposes the root namespace path as `CI_PROJECT_ROOT_NAMESPACE`.
    For this setup, that means a project under
    `sigitxviii/students/...` or `sigitxviii/auto-tests/...` can discover
    `sigitxviii` without a manually maintained `COURSE_PATH` variable.
    `COURSE_PATH` still works as an override for local testing or unusual
    layouts.
    """

    return env("COURSE_PATH", os.getenv("CI_PROJECT_ROOT_NAMESPACE"))


def env(name: str, default: str | None = None) -> str:
    """Read required configuration with clear errors and simple defaults.

    Most values come from GitLab's built-in CI variables or from defaults in this
    file. The only truly required custom secret is `ROOT_CI_TOKEN`.
    """

    value = os.getenv(name, default)
    if value is None or value == "":
        raise RuntimeError(f"{name} is not set")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
