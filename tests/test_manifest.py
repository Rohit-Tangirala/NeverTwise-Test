from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]


def test_manifest_has_twenty_documented_scenarios():
    data = yaml.safe_load((ROOT / "scenarios" / "manifest.yaml").read_text())
    scenarios = data["scenarios"]
    assert len(scenarios) >= 20
    required = {
        "id",
        "description",
        "category",
        "affected_files",
        "setup",
        "reproduction",
        "expected_behavior",
        "expected_verdicts",
        "guardrail",
        "cleanup",
    }
    assert all(required <= set(item) for item in scenarios)
    assert len({item["id"] for item in scenarios}) == len(scenarios)
