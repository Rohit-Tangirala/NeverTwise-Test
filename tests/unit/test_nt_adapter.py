from scripts.nt_adapter import invoke, supported_commands


def test_missing_nt_is_reported_without_claiming_detection(monkeypatch):
    monkeypatch.setattr("scripts.nt_adapter.shutil.which", lambda _: None)
    result = invoke(["check"])
    assert result.available is False
    assert result.verdict is None
    assert supported_commands()["check"] is False
