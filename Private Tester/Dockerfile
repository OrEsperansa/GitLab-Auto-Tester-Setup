# This image is used by Private Tester/.gitlab-ci.yml.
# It contains everything needed to run runner/private_tester.py without
# installing packages during the GitLab job.
FROM python:3.12-slim

# git clones the private test repository and the student's submitted repo.
# ca-certificates lets Python and Git trust HTTPS GitLab/Artifactory endpoints.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# pytest runs the hidden tests.
# requests posts the pass/fail commit status back to GitLab.
RUN pip install --no-cache-dir \
    "pytest>=8.0,<9.0" \
    "requests>=2.31,<3.0"

# The CI job checks out the Private Tester repository into its own workspace.
# This default directory is only here for humans who run the image manually.
WORKDIR /autotester
