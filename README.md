# PipeForge

[![PyPI - Version](https://img.shields.io/pypi/v/pipeforge.svg)](https://pypi.org/project/pipeforge)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipeforge.svg)](https://pypi.org/project/pipeforge)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Targets](#targets)
- [License](#license)

## Installation

```console
pip install pipeforge
```

## Usage

PipeForge is a small CLI that reads Atlassian Bamboo Specs YAML and emits pipeline files for other CI providers. It keeps an internal, vendor-neutral model so additional targets (Bitbucket Pipelines, GitLab CI/CD, GitHub Actions, and more) can be added without changing the CLI surface.

```console
# Show the supported input sources and output targets
pipeforge list

# Convert a Bamboo spec to Bitbucket Pipelines (prints to stdout)
pipeforge convert bamboo-spec.yml --target bitbucket

# Override the pipeline name and write a GitLab CI file
pipeforge convert bamboo-spec.yml --target gitlab --name "My Pipeline" -o .gitlab-ci.yml

# Future: switch sources as more parsers are added
pipeforge convert bitbucket-pipelines.yml --source bitbucket --target gitlab
```

### Minimal Bamboo example

```yaml
plan:
  name: Example Plan
variables:
  APP_ENV: dev
jobs:
  - name: build
    tasks:
      - script:
          - echo "build"
  - test:
      tasks:
        - script:
            - echo "run tests"
```

## Targets

- `bitbucket` - `bitbucket-pipelines.yml`
- `gitlab` - `.gitlab-ci.yml`
- `github` - `.github/workflows/pipeforge.yml`

Each renderer flattens the Bamboo steps into the closest equivalent for the target CI platform and exports variables as `export KEY="VALUE"` statements so they can be executed immediately. Renderers live under `pipeforge/renderers/` and parsers under `pipeforge/parsers/` to make adding new providers straightforward.

## License

`pipeforge` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
