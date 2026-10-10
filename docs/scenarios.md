# Scenario Lab

`scenarios/manifest.yaml` is the source of truth for reproducible cases. Every entry records its category, affected files, setup, reproduction, expected application behavior, allowed NeverTwice verdicts, required guardrail, and cleanup.

List cases with:

```powershell
python scripts/run_scenario.py --list
```

A mutation run requires both a clean Git state and explicit `--allow-modify`. The current runner captures the application test result and `nt check` result separately. Missing `nt` produces `NOT EVALUABLE`, never a false detection pass. Mutation-specific changes should be made in a disposable Git worktree and removed by the operator after evidence is captured.
