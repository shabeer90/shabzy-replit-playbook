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


def prd(status="approved", undo="Switch off FLAG_X; sent emails can't be recalled."):
    """A reader holding one PRD at the PR head, as check_lane.at() reads it from git."""
    text = f"# X\nStatus: {status}\n\n## Undo\n<!-- hint -->\n{undo}\n\n## Review\n"
    return "docs/prd/x.md", lambda path: text if path == "docs/prd/x.md" else ""


def test_small_fix_passes():
    assert check_lane.problems(body("fix"), [("src/Footer.tsx", 12)], CONFIG) == []


def test_missing_lane_fails():
    assert check_lane.problems("Fixes the footer", [("src/Footer.tsx", 1)], CONFIG)


def test_one_way_path_forces_a_bet():
    found = check_lane.problems(body("fix"), [("src/lib/auth/session.ts", 3)], CONFIG)
    assert any("Bet" in p and "src/lib/auth/session.ts" in p for p in found)


def test_big_fix_must_be_a_feature():
    found = check_lane.problems(body("fix"), [("src/Page.tsx", 90), ("pnpm-lock.yaml", 900), ("src/Card.tsx", 20)], CONFIG)
    assert any("110 lines added" in p for p in found)


def test_door_can_name_its_criterion():
    assert check_lane.problems(body("fix", door="two-way (copy only)"), [("src/Footer.tsx", 3)], CONFIG) == []


def test_docs_never_force_a_bet():
    assert check_lane.problems(body("fix"), [("docs/notes/email-ideas.md", 3)], CONFIG) == []


def test_door_must_match_lane():
    assert check_lane.problems(body("feature", door="one-way", prd="x"), [], CONFIG)


def test_feature_needs_an_approved_prd():
    path, read = prd(status="draft")
    assert check_lane.problems(body("feature", prd=path), [("src/Search.tsx", 300)], CONFIG, read)
    assert check_lane.problems(body("feature", prd="docs/prd/missing.md"), [], CONFIG, read)


def test_approved_feature_passes():
    path, read = prd()
    assert check_lane.problems(body("feature", prd=path), [("src/Search.tsx", 300)], CONFIG, read) == []


def test_bet_needs_an_undo_plan():
    path, read = prd(undo="")
    found = check_lane.problems(body("bet", door="one-way", prd=path), [("supabase/schema.sql", 5)], CONFIG, read)
    assert any("Undo" in p for p in found)


def test_bet_with_undo_passes():
    path, read = prd()
    assert check_lane.problems(body("bet", door="one-way", prd=path), [("supabase/schema.sql", 5)], CONFIG, read) == []


def test_component_names_count_whatever_their_case():
    for path in ["src/components/PaymentForm.tsx", "src/components/AuthProvider.tsx", "app/CheckoutButton.tsx"]:
        assert check_lane.problems(body("fix"), [(path, 3)], CONFIG), path


def test_author_pages_are_not_auth():
    assert check_lane.problems(body("fix"), [("content/authors.json", 3), ("src/AuthorBio.tsx", 3)], CONFIG) == []
    assert check_lane.problems(body("fix"), [("src/lib/authorize.ts", 3)], CONFIG)


def test_the_rails_are_one_way():
    for path in ["scripts/write_version.sh", "scripts/check_live_drift.py", ".github/workflows/pr-lane.yml"]:
        assert check_lane.problems(body("fix"), [(path, 1)], CONFIG), path


def test_reads_the_prd_and_diff_from_the_pr_head(tmp_path, monkeypatch):
    """Base is checked out (pull_request_target); the PR's files exist only as git objects."""
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    (tmp_path / "old.ts").write_text("x\n" * 150)
    run("add", "."); run("commit", "-q", "-m", "base")
    run("checkout", "-q", "-b", "pr")
    (tmp_path / "old.ts").unlink()
    (tmp_path / "docs/prd").mkdir(parents=True)
    (tmp_path / "docs/prd/x.md").write_text("Status: approved\n")
    run("add", "-A"); run("commit", "-q", "-m", "pr")
    head = run("rev-parse", "HEAD")
    run("checkout", "-q", "main")
    monkeypatch.chdir(tmp_path)
    assert ("old.ts", 0) in check_lane.changed("main", head)  # 150 lines deleted count as 0 added
    assert check_lane.at(head)("docs/prd/x.md") == "Status: approved\n"
    assert check_lane.at(head)("docs/prd/missing.md") == ""


def _repo(tmp_path, monkeypatch):
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    run("commit", "-q", "--allow-empty", "-m", "one")
    first = run("rev-parse", "HEAD")
    (tmp_path / "app.ts").write_text("two")  # a site change: empty or docs-only merges don't need a republish
    run("add", "."); run("commit", "-q", "-m", "two")
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


def test_docs_only_merges_dont_need_a_republish(tmp_path, monkeypatch):
    first, head, _ = _repo(tmp_path, monkeypatch)
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/notes.md").write_text("x")
    (tmp_path / "README.md").write_text("x")
    run("add", "."); run("commit", "-q", "-m", "docs only")
    live = run("rev-parse", "HEAD")
    (tmp_path / "content").mkdir()
    (tmp_path / "content/post.md").write_text("a published page")
    run("add", "."); run("commit", "-q", "-m", "site change")
    assert check_live_drift.problems(head, main="main", now=9e9) and "1 merge(s)" in check_live_drift.problems(head, main="main", now=9e9)[0]
    assert check_live_drift.problems(live, main="main", now=9e9)  # content/post.md is the site
    run("reset", "-q", "--hard", live)
    assert check_live_drift.problems(head, main="main", now=9e9) == []  # only docs waiting


def test_lockfile_rewrites_dont_make_a_build_dirty(tmp_path):
    def run(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "app.ts").write_text("1")
    run("add", "."); run("commit", "-q", "-m", "one")
    script = pathlib.Path(__file__).parent / "write_version.sh"
    def version():
        subprocess.run(["bash", str(script), "out/version.txt"], cwd=tmp_path, check=True)
        return (tmp_path / "out/version.txt").read_text().strip()
    (tmp_path / "package-lock.json").write_text('{"changed": 1}')
    assert not version().endswith("-dirty")
    (tmp_path / "app.ts").write_text("2")
    assert version().endswith("-dirty")
