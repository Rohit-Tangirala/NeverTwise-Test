from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CommandResult:
    command: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    supported: bool = True


@dataclass
class ScenarioResult:
    scenario_id: str
    status: str
    application: CommandResult | None
    never_twice: CommandResult | None
    note: str


def load_manifest() -> list[dict[str, Any]]:
    manifest = yaml.safe_load((ROOT / "scenarios" / "manifest.yaml").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("scenarios"), list):
        raise ValueError("scenarios/manifest.yaml must contain a scenarios list")
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
    for scenario in manifest["scenarios"]:
        missing = required - set(scenario)
        if missing:
            raise ValueError(f"{scenario.get('id', '<unknown>')} missing fields: {sorted(missing)}")
    return manifest["scenarios"]


def run_command(command: list[str], cwd: Path = ROOT) -> CommandResult:
    try:
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    except FileNotFoundError as error:
        return CommandResult(command, None, "", str(error), supported=False)
    return CommandResult(command, completed.returncode, completed.stdout, completed.stderr)


def nt_check(cwd: Path = ROOT) -> CommandResult:
    return run_command(["nt", "check"], cwd=cwd)


def list_scenarios(scenarios: list[dict[str, Any]]) -> None:
    for scenario in scenarios:
        print(f"{scenario['id']} [{scenario['category']}] {scenario['description']}")


def ensure_clean_repository() -> None:
    status = run_command(["git", "status", "--porcelain"])
    if status.returncode != 0:
        raise RuntimeError("This runner must be launched from a Git repository")
    if status.stdout.strip():
        raise RuntimeError(
            "Working tree is not clean; use an isolated worktree or commit changes first"
        )


def create_worktree(scenario_id: str) -> Path:
    worktree_root = ROOT / "worktrees"
    worktree_root.mkdir(exist_ok=True)
    worktree = Path(tempfile.mkdtemp(prefix=f"{scenario_id.lower()}-", dir=worktree_root))
    result = run_command(["git", "worktree", "add", "--detach", str(worktree), "HEAD"])
    if result.returncode != 0:
        worktree.rmdir()
        raise RuntimeError(result.stderr.strip() or "Unable to create isolated Git worktree")
    return worktree


def remove_worktree(worktree: Path) -> None:
    result = run_command(["git", "worktree", "remove", "--force", str(worktree)])
    if result.returncode != 0 and worktree.exists():
        raise RuntimeError(result.stderr.strip() or "Unable to remove isolated Git worktree")


def run_selected(scenario: dict[str, Any], allow_modify: bool) -> ScenarioResult:
    if not allow_modify:
        return ScenarioResult(
            scenario["id"], "SKIPPED", None, None, "Mutation requires --allow-modify"
        )
    ensure_clean_repository()
    worktree = create_worktree(scenario["id"])
    try:
        application = run_command([sys.executable, "-m", "pytest", "-q"], cwd=worktree)
        never_twice = nt_check(cwd=worktree)
        if not never_twice.supported:
            status = "NOT EVALUABLE"
            note = "nt executable is unavailable; application and NeverTwice results are separate"
        else:
            status = (
                "PASS" if application.returncode == 0 and never_twice.returncode == 0 else "FAIL"
            )
            note = (
                "Application tests and nt check captured; verdict semantics require "
                "scenario-specific review"
            )
        return ScenarioResult(scenario["id"], status, application, never_twice, note)
    finally:
        remove_worktree(worktree)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run NeverTwice Test Lab scenarios safely")
    parser.add_argument("scenario", nargs="?", help="Scenario ID")
    parser.add_argument("--list", action="store_true", help="List available scenarios")
    parser.add_argument(
        "--allow-modify", action="store_true", help="Explicitly allow isolated mutation commands"
    )
    parser.add_argument("--report", type=Path, help="Write JSON report")
    args = parser.parse_args()
    scenarios = load_manifest()
    if args.list:
        list_scenarios(scenarios)
        return 0
    if not args.scenario:
        parser.error("provide a scenario ID or --list")
    scenario = next((item for item in scenarios if item["id"] == args.scenario), None)
    if scenario is None:
        parser.error(f"unknown scenario: {args.scenario}")
    result = run_selected(scenario, args.allow_modify)
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0 if result.status in {"PASS", "SKIPPED", "NOT EVALUABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
