from typer.testing import CliRunner

from inferforge.cli import app


def test_cli_help() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "InferForge inference optimization toolkit." in result.output
    assert "serve" in result.output


def test_cli_placeholder_commands() -> None:
    runner = CliRunner()

    benchmark = runner.invoke(app, ["benchmark"])
    replay = runner.invoke(app, ["replay", "examples/workload.json"])
    report = runner.invoke(app, ["report"])

    assert benchmark.exit_code == 0
    assert "planned for a later phase" in benchmark.output
    assert replay.exit_code == 0
    assert "planned for a later phase" in replay.output
    assert "examples/workload.json" in replay.output
    assert report.exit_code == 0
    assert "planned for a later phase" in report.output
