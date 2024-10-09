# CodeRider CodeReview

## How to set up

Copy `.env.example` to `.env`, and set ENV:

```.env
CR_AI_BOT_TOKEN=""
# CR_MR_PROJECT_PATH=""
# CR_MR_IID=""
```

Install dependencies:

```shell
poetry install
```

## Publish

Update versions of `pyproject.toml` and `coderider_codereview/__init__.py` and `readme.md`.

https://pypi.org/project/coderider-codereview/

It's necessary for the first time:

```shell
poetry config pypi-token.pypi <pypi-token>
```

Build with Cython and generate package with poetry:

```shell
poetry run python setup.py
poetry build
poetry publish
poetry run python setup.py clean
```

## Use it in local

```shell
pip install coderider_codereview
CR_AI_BOT_TOKEN="" CR_MR_PROJECT_PATH="" CR_MR_IID="" crcr
```

## GitLab CI Template File

https://jihulab.com/-/snippets/6198

```yaml
include:
  - remote: 'https://jihulab.com/-/snippets/6198/raw/main/coderider-codereview-0.5.1.yml'
```

``` yaml
# 0.6.0

CodeRiderCodeReview:
  stage: test
  image: python:3.11
  variables:
  # CR_AI_BOT_TOKEN: "<Set it through GitLab CI/CD variables>"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      needs:
        - job: semgrep-sast
          optional: true
          artifacts: true
        - job: secret_detection
          optional: true
          artifacts: true
  before_script: [ ]
  after_script: [ ]
  script:
    - ls -l gl-sast-report.json || true
    - ls -l gl-secret-detection-report.json || true
    - pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    - pip install --no-cache-dir coderider-codereview==0.6.0
    - crcr

# Override artifacts paths
sast:
  artifacts:
    access: 'developer'
    reports:
      sast: gl-sast-report.json
    paths: [ gl-sast-report.json ]
  rules:
    - when: never
  script:
    - echo "$CI_JOB_NAME is used for configuration only, and its script should not be executed"
    - exit 1

.secret-analyzer:
  artifacts:
    access: 'developer'
    reports:
      secret_detection: gl-secret-detection-report.json
    paths: [ gl-secret-detection-report.json ]

```

## Dependencies

- Vulnerability comments in diff:  GitLab >= 16.5
- Customize analyzer settings: Premium Plan
- Project Access Token: Premium Plan
