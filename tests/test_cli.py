import json
from pathlib import Path

from gadget_scout.cli import run_dry_run


def test_run_dry_run_writes_json_and_markdown(tmp_path):
    result = run_dry_run(
        fixture_path=Path("tests/fixtures/candidates.json"),
        output_dir=tmp_path,
        run_date="2026-06-23",
        max_items_per_region=10,
        min_score=75,
    )

    report = json.loads(result.json_path.read_text(encoding="utf-8"))
    markdown = result.markdown_path.read_text(encoding="utf-8")

    assert result.domestic_selected_count == 1
    assert result.overseas_selected_count == 2
    assert report["domestic_selected_count"] == 1
    assert report["overseas_selected_count"] == 2
    assert report["max_items_per_region"] == 10
    assert "今日好物雷达 2026-06-23" in markdown
