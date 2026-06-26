# Python Auto Tester

This is the private hidden-tests repository:

```text
sigitxviii/auto-tests/python-auto-tester
```

Students should not be members of this project.

## Test Mapping Convention

Student repositories must follow this path:

```text
sigitxviii/students/sigituserXX-group/ExerciseName/ExerciseRepo
```

The runner maps that to hidden tests here:

```text
tests/ExerciseName/ExerciseRepo/
```

For example:

```text
sigitxviii/students/sigituser00-group/basic/04-house-application
```

runs:

```text
tests/basic/04-house-application/
```

## Adding Tests

Create normal pytest files under the matching folder. Keep assertion messages
student-friendly, because sanitized assertion messages are shown in the merge
request comment.
