# Setup Guide

This guide sets up hidden pytest tests for student merge requests.

## 1. Create The GitLab Projects

Create these two projects:

```text
sigitxviii/auto-tests/private-tests
sigitxviii/auto-tests/python-auto-tester
```

Use these permissions:

```text
Private Tester: public, students can run pipelines
Python Auto Tester: private, students should not have access
```

## 2. Push The Files

Push this folder to:

```text
Private Tester/ -> sigitxviii/auto-tests/private-tests
```

Push this folder to:

```text
Python Auto Tester/ -> sigitxviii/auto-tests/python-auto-tester
```

Copy this file into every student exercise repo:

```text
Student Exercise Repo Template/.gitlab-ci.yml
```

## 3. Add Private Tester Variables

In GitLab, open:

```text
sigitxviii/auto-tests/private-tests > Settings > CI/CD > Variables
```

Add these variables:

```text
ROOT_CI_TOKEN=<token that can clone Python Auto Tester and student repos>
```

Mark `ROOT_CI_TOKEN` as masked.

Usually this is the only variable you need.

Optional overrides:

```text
ROOT_CI_USERNAME=oauth2
COURSE_NAME=SigitXVIII
COURSE_PATH=sigitxviii
PYTHON_AUTO_TESTER_PROJECT_PATH=sigitxviii/auto-tests/python-auto-tester
PYTHON_AUTO_TESTER_REF=main
```

You normally do not need to set `GITLAB_BASE_URL`; GitLab provides it
automatically as `CI_SERVER_URL`.

## 4. Prepare The Offline Runner Image

Create the image described in `REQUIRED.md` and push it to:

```text
artifactory.school/sigitxviii/python-autotester:3.12
```

The pipeline does not run `apt-get` or `pip install`; everything required must
already be inside this image.

## 5. Student Repo Structure

Student repos must be under this path:

```text
sigitxviii/students/sigituserXX-group/ExerciseName/ExerciseRepo
```

Example:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

## 6. Hidden Test Structure

Hidden tests must match the student repo path.

For this student repo:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

Put tests here:

```text
Python Auto Tester/tests/basic/04-house-application/
```

Example test file:

```text
Python Auto Tester/tests/basic/04-house-application/test_smoke.py
```

## 7. How It Runs

When a student opens or updates a merge request:

1. The student repo pipeline starts.
2. The student `.gitlab-ci.yml` starts `Private Tester` as a downstream pipeline.
3. `Private Tester` clones `Python Auto Tester`.
4. `Private Tester` clones the exact student commit.
5. `Private Tester` runs the matching pytest folder.
6. The pipeline passes or fails.
7. A commit status is posted back to the student commit.

## 8. Test The Setup

Create a test student repo:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

Add the split animal exercise files from `Student Exercise Repo Template`:

```text
animal.py
dog.py
cat.py
summary.py
```

Copy in:

```text
Student Exercise Repo Template/.gitlab-ci.yml
```

Create a merge request.

Expected result:

```text
Student pipeline starts Private Tester.
Private Tester runs tests/basic/04-house-application.
The pipeline passes.
```

Then break one behavior, for example change `Dog.speak()` in `dog.py`:

```python
def speak(self):
    return f"{self.name} says hello!"
```

Expected result:

```text
Private Tester pipeline fails.
The pytest failure appears in the job log.
```

## 9. Adding A New Exercise

For a new student repo:

```text
sigitxviii/students/sigituser00-group/basic/05-next-exercise
```

Create hidden tests here:

```text
Python Auto Tester/tests/basic/05-next-exercise/
```

No code changes are needed in `Private Tester`.
