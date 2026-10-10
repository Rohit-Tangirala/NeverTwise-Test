from scripts.run_scenario import load_manifest, run_selected


def test_manifest_loads_and_runner_requires_explicit_mutation():
    scenarios = load_manifest()
    result = run_selected(scenarios[0], allow_modify=False)
    assert len(scenarios) >= 20
    assert result.status == "SKIPPED"
