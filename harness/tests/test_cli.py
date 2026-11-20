import pytest
import yaml

from harness.cli import main
from harness.config import DEFAULT_SPEC, load_config


def test_cli_lists_the_registered_workflow(capsys):
    assert main(["list-workflows"]) == 0
    assert capsys.readouterr().out == "micro-single-task\n"


def test_bundled_workflow_spec_is_packaged_and_loadable():
    config = load_config()
    assert config.benchmark_slug == "inference-micro-single-task"
    assert len(config.providers) == 10


def test_spec_with_provider_rows_is_refused(tmp_path):
    spec = yaml.safe_load(DEFAULT_SPEC.read_text(encoding="utf-8"))
    spec["providers"]["vendors"] = {"together": {"model_key": "zai-org/GLM-5.3-Flash"}}
    path = tmp_path / "spec.yaml"
    path.write_text(yaml.safe_dump(spec), encoding="utf-8")
    with pytest.raises(ValueError, match="tools/<tool>.yaml"):
        load_config(path)
