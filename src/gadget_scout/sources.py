from __future__ import annotations

import json
from pathlib import Path

from gadget_scout.models import CandidateProduct, ProductStage, SourceRegion


def load_fixture_candidates(path: str | Path) -> list[CandidateProduct]:
    fixture_path = Path(path)
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    candidates: list[CandidateProduct] = []
    for item in data:
        candidates.append(
            CandidateProduct(
                source_name=item["source_name"],
                source_region=SourceRegion(item["source_region"]),
                source_url=item["source_url"],
                product_name=item["product_name"],
                highlight=item["highlight"],
                country_region=item["country_region"],
                stage=ProductStage(item.get("stage", "unknown")),
                product_category=list(item.get("product_category", [])),
                target_audience=item.get("target_audience", ""),
                novelty_reason=item.get("novelty_reason", ""),
                trend_reason=item.get("trend_reason", ""),
                evidence=list(item.get("evidence", [])),
                commercial_judgment=item.get("commercial_judgment", ""),
                showroom_fit=item.get("showroom_fit", ""),
                risks=list(item.get("risks", [])),
                raw_score_signals=dict(item.get("raw_score_signals", {})),
            )
        )
    return candidates
