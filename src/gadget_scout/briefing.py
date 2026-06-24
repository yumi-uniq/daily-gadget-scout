from __future__ import annotations

from gadget_scout.models import SelectedProduct, SourceRegion


def format_daily_briefing(
    selected_by_region: dict[SourceRegion, list[SelectedProduct]], run_date: str
) -> str:
    domestic = selected_by_region.get(SourceRegion.DOMESTIC, [])
    overseas = selected_by_region.get(SourceRegion.OVERSEAS, [])
    if not domestic and not overseas:
        return (
            f"今日好物雷达 {run_date}\n\n"
            "今日无高置信推荐，未强行凑数。\n\n"
            "观察到的弱信号：\n"
            "- 候选质量未达到高置信阈值，建议保留观察但不推进。"
        )

    lines = [
        f"今日好物雷达 {run_date}",
        "",
        f"国内入选 {len(domestic)} 个，海外入选 {len(overseas)} 个。",
        "",
    ]

    for title, items in (("国内 Top", domestic), ("海外 Top", overseas)):
        lines.extend([title, ""])
        if not items:
            lines.extend(["无高置信推荐。", ""])
            continue
        for index, item in enumerate(items, start=1):
            candidate = item.candidate
            lines.extend(
                [
                    (
                        f"{index}. {candidate.product_name}｜"
                        f"{item.recommendation_action.value}｜{item.score.total}"
                    ),
                    candidate.highlight,
                    f"为什么值得看：{candidate.trend_reason}",
                    f"下一步建议：{candidate.commercial_judgment}",
                    f"链接：{candidate.source_url}",
                    "",
                ]
            )

    lines.extend(["今日信号：", "- 国内和海外分别评分、分别排序；未设置未来好物/趋势好物固定比例。"])
    return "\n".join(lines).strip()
