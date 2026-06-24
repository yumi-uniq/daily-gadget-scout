from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates
from gadget_scout.wecom import build_smartsheet_records, build_wecom_text_payload


@dataclass(frozen=True)
class DryRunResult:
    domestic_selected_count: int
    overseas_selected_count: int
    json_path: Path
    markdown_path: Path


def run_dry_run(
    fixture_path: Path,
    output_dir: Path,
    run_date: str,
    max_items_per_region: int = 10,
    min_score: int = 75,
) -> DryRunResult:
    candidates = load_fixture_candidates(fixture_path)
    selected = select_top_products_by_region(
        candidates,
        max_items_per_region=max_items_per_region,
        min_score=min_score,
    )
    briefing = format_daily_briefing(selected, run_date=run_date)
    records = build_smartsheet_records(selected, run_date=run_date)
    bot_payload = build_wecom_text_payload(briefing)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{run_date}-dry-run.json"
    markdown_path = output_dir / f"{run_date}-briefing.md"

    json_payload = {
        "run_date": run_date,
        "max_items_per_region": max_items_per_region,
        "min_score": min_score,
        "domestic_selected_count": len(selected[SourceRegion.DOMESTIC]),
        "overseas_selected_count": len(selected[SourceRegion.OVERSEAS]),
        "records": {
            region.value: region_records for region, region_records in records.items()
        },
        "bot_payload": bot_payload,
    }
    json_path.write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown_path.write_text(briefing, encoding="utf-8")
    return DryRunResult(
        domestic_selected_count=len(selected[SourceRegion.DOMESTIC]),
        overseas_selected_count=len(selected[SourceRegion.OVERSEAS]),
        json_path=json_path,
        markdown_path=markdown_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the daily gadget scout pipeline.")
    parser.add_argument("--fixtures", default="tests/fixtures/candidates.json")
    parser.add_argument("--out", default="runs")
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--max-items-per-region", type=int, default=10)
    parser.add_argument("--min-score", type=int, default=75)
    args = parser.parse_args()

    result = run_dry_run(
        fixture_path=Path(args.fixtures),
        output_dir=Path(args.out),
        run_date=args.run_date,
        max_items_per_region=args.max_items_per_region,
        min_score=args.min_score,
    )
    print(f"domestic_selected_count={result.domestic_selected_count}")
    print(f"overseas_selected_count={result.overseas_selected_count}")
    print(f"json_path={result.json_path}")
    print(f"markdown_path={result.markdown_path}")


if __name__ == "__main__":
    main()
