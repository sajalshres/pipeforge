# SPDX-FileCopyrightText: 2025-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import yaml
from click.testing import CliRunner

from pipeforge.cli import app

runner = CliRunner()


def _write_sample_spec(tmp_path: Path) -> Path:
    spec = tmp_path / "bamboo.yml"
    spec.write_text(
        """
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
        - script: echo "second command"
""",
        encoding="utf-8",
    )
    return spec


def test_convert_to_bitbucket(tmp_path):
    spec = _write_sample_spec(tmp_path)
    result = runner.invoke(app, ["convert", str(spec), "--target", "bitbucket"])
    assert result.exit_code == 0, result.stdout
    output = yaml.safe_load(result.stdout)
    assert output["pipelines"]["default"], "Bitbucket pipelines default steps missing"


def test_convert_to_gitlab(tmp_path):
    spec = _write_sample_spec(tmp_path)
    result = runner.invoke(app, ["convert", str(spec), "--target", "gitlab"])
    assert result.exit_code == 0, result.stdout
    output = yaml.safe_load(result.stdout)
    assert "stages" in output
    job_keys = [key for key in output.keys() if key not in {"stages", "variables"}]
    assert job_keys, "GitLab jobs should exist"
