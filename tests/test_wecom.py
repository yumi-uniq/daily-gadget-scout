from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates
from gadget_scout.wecom import build_smartsheet_records, build_wecom_text_payload


def test_build_smartsheet_records_uses_expected_fields_without_owner():
    selected = select_top_products_by_region(
        load_fixture_candidates("tests/fixtures/candidates.json")
    )

    records = build_smartsheet_records(selected, run_date="2026-06-23")

    first_values = records[SourceRegion.OVERSEAS][0]["values"]
    assert "负责人" not in first_values
    assert first_values["日期"][0]["text"] == "2026-06-23"
    assert first_values["来源区域"][0]["text"] == "海外"
    assert first_values["推荐动作"][0]["text"] == "展厅合作"
    assert first_values["综合分"][0]["text"] == "91"
    assert "去重ID" in first_values

    domestic_values = records[SourceRegion.DOMESTIC][0]["values"]
    assert domestic_values["来源区域"][0]["text"] == "国内"
    assert domestic_values["推荐动作"][0]["text"] == "供应链推进"


def test_build_wecom_text_payload_wraps_briefing():
    selected = select_top_products_by_region(
        load_fixture_candidates("tests/fixtures/candidates.json")
    )
    briefing = format_daily_briefing(selected, run_date="2026-06-23")

    payload = build_wecom_text_payload(briefing)

    assert payload == {
        "msgtype": "text",
        "text": {"content": briefing},
    }
