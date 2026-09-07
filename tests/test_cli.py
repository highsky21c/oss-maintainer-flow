from pathlib import Path

from oss_maintainer_flow.cli import write_output


def test_write_output_creates_parent_directories(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "triage.md"

    write_output("# Triage\n", output)

    assert output.read_text(encoding="utf-8") == "# Triage\n"
