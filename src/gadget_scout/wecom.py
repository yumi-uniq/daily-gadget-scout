from __future__ import annotations

from gadget_scout.models import SelectedProduct, SourceRegion


def _text(value: object) -> list[dict[str, str]]:
    return [{"type": "text", "text": str(value)}]


def build_smartsheet_records(
    selected_by_region: dict[SourceRegion, list[SelectedProduct]], run_date: str
) -> dict[SourceRegion, list[dict[str, dict[str, list[dict[str, str]]]]]]:
    output: dict[SourceRegion, list[dict[str, dict[str, list[dict[str, str]]]]]] = {
        SourceRegion.DOMESTIC: [],
        SourceRegion.OVERSEAS: [],
    }
    region_label = {
        SourceRegion.DOMESTIC: "国内",
        SourceRegion.OVERSEAS: "海外",
    }
    for region, selected in selected_by_region.items():
        for item in selected:
            candidate = item.candidate
            values = {
                "日期": _text(run_date),
                "分类": _text(item.classification.value),
                "产品名": _text(candidate.product_name),
                "一句话亮点": _text(candidate.highlight),
                "来源链接": _text(candidate.source_url),
                "国家/地区": _text(candidate.country_region),
                "来源区域": _text(region_label[region]),
                "产品阶段": _text(candidate.stage.value),
                "预计上市时间": _text("未知"),
                "品类": _text(", ".join(candidate.product_category)),
                "目标人群": _text(candidate.target_audience),
                "为什么新奇": _text(candidate.novelty_reason),
                "为什么可能火": _text(candidate.trend_reason),
                "关键证据": _text("；".join(candidate.evidence)),
                "商业判断": _text(candidate.commercial_judgment),
                "展厅适配建议": _text(candidate.showroom_fit),
                "风险": _text("；".join(candidate.risks)),
                "综合分": _text(item.score.total),
                "推荐动作": _text(item.recommendation_action.value),
                "去重ID": _text(item.dedupe_id),
            }
            output[region].append({"values": values})
    return output


def build_wecom_text_payload(content: str) -> dict[str, object]:
    return {
        "msgtype": "text",
        "text": {"content": content},
    }
