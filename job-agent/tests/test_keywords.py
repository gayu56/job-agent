from utils.keywords import compute_keyword_stats


def test_keyword_coverage_basic():
    jd_kw = ["Python", "SQL", "AWS"]
    resume = "Built pipelines in Python and SQL on AWS."
    s = compute_keyword_stats(jd_kw, resume)
    assert s["total_keywords"] == 3
    assert s["coverage_percent"] == 100
    assert len(s["missing"]) == 0


def test_keyword_missing():
    s = compute_keyword_stats(["Kubernetes", "Excel"], "I use Excel daily.")
    assert len(s["missing"]) >= 1
