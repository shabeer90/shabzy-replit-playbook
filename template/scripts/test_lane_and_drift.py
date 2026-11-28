"""The two checks that hold without Claude Code: the PR lane check and the live-drift check (PLAYBOOK rules 1 and 31).

Lanes: process follows the door, not the size. A PR can always raise its own lane, never lower it.
Drift: on Cogniscore the live site lagged main several times because Replit publishes its workspace,
not GitHub. Nothing noticed until someone looked.
"""
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check_lane  # noqa: E402
import check_live_drift  # noqa: E402

CONFIG = json.loads((pathlib.Path(__file__).parent.parent / "config/lanes.json").read_text())


def body(lane, door="two-way", prd="fix", blast="the contact page"):
    return f"**Lane:** {lane}\n**Door:** {door}\n**Blast radius:** {blast}\nPRD: {prd}\n"


def prd(tmp_path, status="approved", undo="Switch off FLAG_X; sent emails can't be recalled."):
    (tmp_path / "docs/prd").mkdir(parents=True)
    (tmp_path / "docs/prd/x.md").write_text(f"# X\nStatus: {status}\n\n## Undo\n<!-- hint -->\n{undo}\n\n## Review\n")
    return "docs/prd/x.md"


def test_small_fix_passes():
    assert check_lane.problems(body("fix"), [("src/Footer.tsx", 12)], CONFIG) == []


def test_missing_lane_fails():
    assert check_lane.problems("Fixes the footer", [("src/Footer.tsx", 1)], CONFIG)


def test_one_way_path_forces_a_bet():
    found = check_lane.problems(body("fix"), [("src/lib/auth/session.ts", 3)], CONFIG)
    assert any("Bet" in p and "src/lib/auth/session.ts" in p for p in found)


def test_big_fix_must_be_a_feature():
    found = check_lane.problems(body("fix"), [("src/Page.tsx", 90), ("pnpm-lock.yaml", 900), ("src/Card.tsx", 20)], CONFIG)
    assert any("110 lines" in p for p in found)


def test_door_can_name_its_criterion():
    assert check_lane.problems(body("fix", door="two-way (copy only)"), [("src/Footer.tsx", 3)], CONFIG) == []


def test_docs_never_force_a_bet():
    assert check_lane.problems(body("fix"), [("docs/notes/email-ideas.md", 3)], CONFIG) == []


def test_door_must_match_lane():
    assert check_lane.problems(body("feature", door="one-way", prd="x"), [], CONFIG)


def test_feature_needs_an_approved_prd(tmp_path):
    path = prd(tmp_path, status="draft")
    assert check_lane.problems(body("feature", prd=path), [("src/Search.tsx", 300)], CONFIG, tmp_path)
    assert check_lane.problems(body("feature", prd="docs/prd/missing.md"), [], CONFIG, tmp_path)


def test_approved_feature_passes(tmp_path):
    assert check_lane.problems(body("feature", prd=prd(tmp_path)), [("src/Search.tsx", 300)], CONFIG, tmp_path) == []


def test_bet_needs_an_undo_plan(tmp_path):
    path = prd(tmp_path, undo="")
    found = check_lane.problems(body("bet", door="one-way", prd=path), [("supabase/schema.sql", 5)], CONFIG, tmp_path)
    assert any("Undo" in p for p in found)


def test_bet_with_undo_passes(tmp_path):
    path = prd(tmp_path)
    assert check_lane.problems(body("bet", door="one-way", prd=path), [("supabase/schema.sql", 5)], CONFIG, tmp_path) == []


def _repo(tmp_path, monkeypatch):
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    run("commit", "-q", "--allow-empty", "-m", "one")
    first = run("rev-parse", "HEAD")
    run("commit", "-q", "--allow-empty", "-m", "two")
    run("checkout", "-q", "-b", "feature")
    run("commit", "-q", "--allow-empty", "-m", "unreviewed")
    branch = run("rev-parse", "HEAD")
    run("checkout", "-q", "main")
    monkeypatch.chdir(tmp_path)
    return first, run("rev-parse", "HEAD"), branch


def test_drift(tmp_path, monkeypatch):
    first, head, branch = _repo(tmp_path, monkeypatch)
    assert check_live_drift.problems(head, main="main") == []
    assert check_live_drift.problems("", main="main")
    assert "uncommitted" in check_live_drift.problems(head + "-dirty", main="main")[0]
    assert "isn't on main" in check_live_drift.problems(branch, main="main")[0]
    assert "nobody pushed" in check_live_drift.problems("ab" * 20, main="main")[0]
    assert check_live_drift.problems(first, main="main", max_hours=24) == []  # waiting, but not for a day yet
    assert "aren't live" in check_live_drift.problems(first, main="main", now=9e9)[0]
