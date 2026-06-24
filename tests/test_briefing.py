from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates


def test_format_daily_briefing_includes_top_items_and_actions():
    selected = select_top_products_by_region(
        load_fixture_candidates("tests/fixtures/candidates.json")
    )

    briefing = format_daily_briefing(selected, run_date="2026-06-23")

    assert "今日好物雷达 2026-06-23" in briefing
    assert "国内入选 1 个，海外入选 2 个。" in briefing
    assert "国内 Top" in briefing
    assert "海外 Top" in briefing
    assert "DeskBot Companion｜展厅合作｜91" in briefing
    assert "AI Pocket Projector｜供应链推进｜82" in briefing
    assert "Smart Ring Lab｜内容优先｜80" in briefing
    assert "链接：" in briefing


def test_format_daily_briefing_for_no_qualified_items():
    briefing = format_daily_briefing(
        {SourceRegion.DOMESTIC: [], SourceRegion.OVERSEAS: []},
        run_date="2026-06-23",
    )

    assert "今日无高置信推荐，未强行凑数。" in briefing
    assert "观察到的弱信号：" in briefing
