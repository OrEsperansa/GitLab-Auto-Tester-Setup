# Student Exercise Repo Template

Copy `.gitlab-ci.yml` into every student exercise repo.

For the normal `SigitXVIII` setup, no CI/CD variables are required in the
student repo. The template asks GitLab for the root namespace path with:

```text
CI_PROJECT_ROOT_NAMESPACE
```

For this course, that value is `sigitxviii`, so the template triggers:

```text
sigitxviii/auto-tests/private-tests
```

The only remaining template variable is:

```text
PRIVATE_TESTER_REF=main
```

No trigger token is needed. GitLab starts `Private Tester` as a downstream
pipeline using the permissions of the user who started the student pipeline.

The template runs only for merge requests targeting the default branch.

It passes the root namespace path, student project path, and exact commit SHA
to `Private Tester`.
