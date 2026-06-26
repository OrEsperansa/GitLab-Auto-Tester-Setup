# SigitXVIII Hidden Python Autotester

This workspace contains the three pieces for your GitLab setup:

```text
Private Tester/              public runner project
Python Auto Tester/          private hidden pytest project
Student Exercise Repo Template/
```

## GitLab Layout

Create these projects:

```text
sigitxviii/auto-tests/private-tests
sigitxviii/auto-tests/python-auto-tester
```

`Private Tester` can be public. `Python Auto Tester` should be private.

## Required Variables

In `Private Tester`, add this masked CI/CD variable:

```text
ROOT_CI_TOKEN=<token that can read Python Auto Tester and student repos, and can post commit statuses>
```

Usually this is the only variable you need. The runner infers the GitLab URL
from `CI_SERVER_URL`, defaults `COURSE_NAME` to `SigitXVIII`, and defaults the
hidden tests project to `sigitxviii/auto-tests/python-auto-tester`.

Optional overrides:

```text
ROOT_CI_USERNAME=oauth2
COURSE_NAME=SigitXVIII
COURSE_PATH=sigitxviii
PYTHON_AUTO_TESTER_PROJECT_PATH=sigitxviii/auto-tests/python-auto-tester
PYTHON_AUTO_TESTER_REF=main
```

For offline school-network setup, see `REQUIRED.md`. The CI job expects the
prebuilt image:

```text
artifactory.school/sigitxviii/python-autotester:3.12
```

For day-to-day teacher workflow, see `HOW_TO_USE.md`.

For the normal `SigitXVIII` setup, student repos do not need any CI/CD
variables. The student `.gitlab-ci.yml` already points to:

```text
PRIVATE_TESTER_PROJECT_PATH=sigitxviii/auto-tests/private-tests
COURSE_PATH=sigitxviii
PRIVATE_TESTER_REF=main
COURSE_NAME=SigitXVIII
```

Only add those variables on the `SigitXVIII/Students` group if you want to
override the defaults without editing the `.gitlab-ci.yml`.

Because this uses a GitLab downstream pipeline, the user who starts the student
pipeline must have permission to run pipelines in `Private Tester`.

## Student Repo Path Convention

Student repos must live at:

```text
sigitxviii/students/sigituserXX-group/ExerciseName/ExerciseRepo
```

Examples:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

The runner maps the path to hidden tests like this:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

runs:

```text
Python Auto Tester/tests/basic/04-house-application/
```

## What Happens in a Merge Request

1. The student repo pipeline starts `Private Tester` as a downstream pipeline.
2. `Private Tester` validates the student project path.
3. `Private Tester` clones `Python Auto Tester` using `ROOT_CI_TOKEN`.
4. `Private Tester` clones the student repo and checks out the exact
   `STUDENT_COMMIT_SHA`.
5. It runs the matching pytest folder with the student repo on `PYTHONPATH`.
6. It posts a commit status named:

   ```text
   autotest/ExerciseName/ExerciseRepo
   ```

## Log Safety

`Private Tester` is public, so keep tests written with clear assertion messages
and avoid printing secrets from tests. The runner does not print token values or
clone URLs with credentials. Pytest output is visible because that is the easiest
thing for students and teachers to debug.

## Local Checks

From this workspace:

```bash
python -m venv .venv
.venv/Scripts/python -m pip install pytest requests
.venv/Scripts/python -m pytest "Private Tester/tests_runner" -q
.venv/Scripts/python -m compileall "Private Tester"
```
