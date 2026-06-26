# Offline Requirements

This setup must run without internet access. The GitLab job must not run
`apt-get`, `pip install`, or download public Docker images.

## Required Container Image

Create this image in JFrog Artifactory:

```text
artifactory.school/sigitxviii/python-autotester:3.12
```

The image must contain:

```text
Python 3.12
git
ca-certificates
pytest
requests
```

Why each item is needed:

```text
Python 3.12       runs the private_tester.py script and student Python code
git               clones Python Auto Tester and student submissions
ca-certificates   lets git/requests trust the internal GitLab HTTPS certificate
pytest            runs the hidden tests
requests          posts pass/fail commit status back to GitLab
```

## Dockerfile

The `Private Tester` repository contains a ready-to-use `Dockerfile` for this
image.

Build and push it as:

```text
docker build -t artifactory.school/sigitxviii/python-autotester:3.12 .
docker push artifactory.school/sigitxviii/python-autotester:3.12
```

The Artifactory image used by the normal test pipeline is:

```text
artifactory.school/sigitxviii/python-autotester:3.12
```

## GitLab Runner Requirement

The GitLab runners must be able to pull this image from:

```text
artifactory.school
```

If Artifactory requires authentication, configure the runner or GitLab CI
variables with Docker registry credentials.

## GitLab Requirement

In `sigitxviii/auto-tests/private-tests`, add:

```text
ROOT_CI_TOKEN=<token that can clone the hidden tests and student repos>
```

This token must have enough permissions to:

```text
read repositories
set commit statuses through the GitLab API
```

No public internet access is required during the CI job once the image exists.
