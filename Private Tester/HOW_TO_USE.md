# How To Use

This guide is for the normal teacher workflow after the setup is complete.

## Project Roles

You work mainly in two repositories:

```text
sigitxviii/auto-tests/python-auto-tester
sigitxviii/students/sigituserXX-group/<category>/<exercise-repo>
```

Use `python-auto-tester` for hidden tests.

Use each student exercise repo for starter code and the student-facing
`.gitlab-ci.yml`.

## Folder Convention

The hidden test folder must match the student repo path.

Student repo:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

Hidden tests:

```text
python-auto-tester/tests/basic/04-house-application/
```

The runner uses this convention automatically. No extra config file is needed.

## Add A New Exercise

1. Create the student repo:

   ```text
   sigitxviii/students/sigituserXX-group/basic/05-some-exercise
   ```

2. Copy the student CI file into that repo:

   ```text
   Student Exercise Repo Template/.gitlab-ci.yml
   ```

3. Add starter code files to the student repo.

4. Create the matching hidden test folder:

   ```text
   python-auto-tester/tests/basic/05-some-exercise/
   ```

5. Add pytest files there:

   ```text
   test_structure.py
   test_models.py
   test_behavior.py
   ```

6. Push both repositories.

The next merge request to the default branch will run the hidden tests.

## Write Hidden Tests

Hidden tests are normal pytest tests.

Example:

```python
import importlib


def test_dog_inherits_from_animal():
    animal = importlib.import_module("animal")
    dog = importlib.import_module("dog")

    assert issubclass(dog.Dog, animal.Animal)
```

For split files, import the expected modules:

```python
def test_summary_uses_polymorphism():
    dog = importlib.import_module("dog")
    cat = importlib.import_module("cat")
    summary = importlib.import_module("summary")

    animals = [dog.Dog("Rex", "Labrador"), cat.Cat("Luna", indoor=True)]

    assert summary.create_animal_summary(animals) == [
        "Rex says woof!",
        "Luna says meow!",
    ]
```

Write clear assertion messages when possible. Students can see pytest output in
the pipeline log.

## Current Example Exercise

Current student repo:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

Current hidden test folder:

```text
python-auto-tester/tests/basic/04-house-application/
```

Current expected student files:

```text
animal.py
dog.py
cat.py
summary.py
```

The hidden tests check an OOP animal inheritance exercise.

## How A Student Submission Runs

1. Student opens or updates a merge request to the default branch.
2. The student repo pipeline starts.
3. The student pipeline starts `private-tests` as a downstream pipeline.
4. `private-tests` clones:

   ```text
   python-auto-tester
   the exact student commit
   ```

5. `private-tests` runs the matching hidden pytest folder.
6. The job passes or fails.
7. A commit status is posted back to the student commit.

## Check Results

Open the student repo:

```text
Build > Pipelines
```

Open the newest pipeline.

Then open the downstream `private-tests` pipeline/job to see pytest output.

Useful things to look for:

```text
INFO: Student repo: ...
INFO: Student commit: ...
INFO: Hidden test folder: ...
Running pytest...
```

If tests fail, pytest shows which test failed and why.

## Common Failures

### Missing hidden tests folder

Error:

```text
Missing hidden tests folder: tests/<category>/<exercise-repo>
```

Fix:

Create the matching folder in `python-auto-tester`.

### Student path does not match

Error:

```text
Student project path must match: sigitxviii/students/sigituserXX-group/ExerciseName/ExerciseRepo
```

Fix:

Move or rename the student repo so it follows the required path convention.

### Cannot clone hidden tests

Error mentions clone failure or `403`.

Fix:

Check `ROOT_CI_TOKEN` in `private-tests`. It must be able to read:

```text
sigitxviii/auto-tests/python-auto-tester
```

### Image cannot be pulled

Error mentions:

```text
artifactory.school/sigitxviii/python-autotester:3.12
```

Fix:

Check Artifactory image availability and runner registry permissions.

## Change The Course Or GitLab Paths

The normal setup discovers the root group path from GitLab:

```text
CI_PROJECT_ROOT_NAMESPACE
```

For `sigitxviii/students/...`, that value is:

```text
sigitxviii
```

That value is used to find:

```text
sigitxviii/auto-tests/private-tests
sigitxviii/auto-tests/python-auto-tester
artifactory.school/sigitxviii/python-autotester:3.12
```

You normally do not need to set `COURSE_NAME`, `COURSE_PATH`,
`PRIVATE_TESTER_PROJECT_PATH`, or `PYTHON_AUTO_TESTER_PROJECT_PATH`.

## Local Testing Before Push

From this workspace, you can run hidden tests against the local student files:

```powershell
$env:PYTHONPATH = (Resolve-Path "Student Exercise Repo Template").Path
python -m pytest "Python Auto Tester/tests/basic/04-house-application" -q
```

This is useful before pushing hidden tests to GitLab.
