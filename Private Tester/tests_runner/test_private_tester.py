import pytest

from runner.private_tester import build_clone_url, course_root_path, parse_student_path


def test_parse_student_path_accepts_expected_shape():
    exercise_group, exercise_repo = parse_student_path(
        "sigitxviii/students/sigituser00-group/basic/04-house-application",
        "sigitxviii",
    )

    assert exercise_group == "basic"
    assert exercise_repo == "04-house-application"


def test_parse_student_path_rejects_wrong_course():
    with pytest.raises(RuntimeError):
        parse_student_path(
            "othercourse/students/sigituser00-group/basic/04-house-application",
            "sigitxviii",
        )


def test_build_clone_url_encodes_spaces_but_keeps_slashes():
    assert (
        build_clone_url("https://gitlab.example.com", "sigitxviii/auto-tests/python-auto-tester")
        == "https://gitlab.example.com/sigitxviii/auto-tests/python-auto-tester.git"
    )


def test_course_root_path_uses_gitlab_root_namespace(monkeypatch):
    monkeypatch.delenv("COURSE_PATH", raising=False)
    monkeypatch.setenv("CI_PROJECT_ROOT_NAMESPACE", "sigitxviii")

    assert course_root_path() == "sigitxviii"


def test_course_root_path_allows_manual_override(monkeypatch):
    monkeypatch.setenv("COURSE_PATH", "othercourse")
    monkeypatch.setenv("CI_PROJECT_ROOT_NAMESPACE", "sigitxviii")

    assert course_root_path() == "othercourse"
