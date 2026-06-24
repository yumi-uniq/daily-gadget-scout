from gadget_scout.models import ProductStage, RecommendationAction
from gadget_scout.scoring import classify_candidate, score_candidate
from gadget_scout.sources import load_fixture_candidates


def test_score_candidate_uses_weighted_signals():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[0]

    score = score_candidate(candidate)

    assert score.total == 80
    assert score.novelty == 18
    assert score.risk_penalty == 5


def test_content_action_for_high_novelty_crowdfunding_item():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[0]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert classification == "未来好物"
    assert action == RecommendationAction.CONTENT_FIRST


def test_supply_chain_action_for_mature_commercial_item():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[1]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert candidate.stage == ProductStage.LAUNCHED
    assert classification == "趋势好物"
    assert action == RecommendationAction.SUPPLY_CHAIN


def test_showroom_partnership_action_for_high_showroom_fit():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[2]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert classification == "趋势好物"
    assert action == RecommendationAction.SHOWROOM_PARTNERSHIP
