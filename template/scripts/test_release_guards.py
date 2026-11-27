"""The day-one release guards: e2e on the built app, checked external writes, the bundle check.

Each one exists because the same mistake reached more than one project (PLAYBOOK rules 17 and 20,
section 7). The first two tests check this repo; the rest check the checkers on small fixtures.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check_bundle  # noqa: E402
import check_external_writes  # noqa: E402


def test_e2e_runs_against_the_built_app():
    configs = [p for p in pathlib.Path(".").glob("playwright.config.*")]
    assert configs, "add playwright.config.ts from the playbook template"
    text = configs[0].read_text()
    command = re.search(r"command:\s*[\"'`]([^\"'`]+)", text)
    assert command, "playwright.config needs a webServer command that serves the built app"
    assert not re.search(r"\bdev\b", command.group(1)), f"e2e points at the dev server: {command.group(1)}"


def test_every_external_write_is_checked():
    assert list(check_external_writes.problems()) == []


def test_unchecked_write_is_caught(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src/contact.ts").write_text(
        "await resend.emails.send(msg);\n"
        "const sent = checked(\n  await resend.emails.send(msg), 'email');\n"
        "await supabase.from('leads').insert(row); // external-write: handled, error read below\n"
    )
    assert [p.split(": result")[0] for p in check_external_writes.problems(tmp_path)] == ["src/contact.ts:1"]


def _build(tmp_path, admin_static, size=100):
    dist = tmp_path / "dist"
    (dist / ".vite").mkdir(parents=True)
    (dist / "assets").mkdir()
    for name in ("main.js", "admin.js"):
        (dist / "assets" / name).write_bytes(b"x" * size)
    manifest = {
        "index.html": {"file": "assets/main.js", "src": "index.html", "isEntry": True,
                       "imports": ["src/pages/admin/Admin.tsx"] if admin_static else [],
                       "dynamicImports": [] if admin_static else ["src/pages/admin/Admin.tsx"]},
        "src/pages/admin/Admin.tsx": {"file": "assets/admin.js", "src": "src/pages/admin/Admin.tsx"},
    }
    (dist / ".vite/manifest.json").write_text(json.dumps(manifest))
    cfg = tmp_path / "bundle.json"
    cfg.write_text(json.dumps({"manifest": str(dist / ".vite/manifest.json"), "publicEntries": ["index.html"],
                               "privateSources": ["src/pages/admin/"], "budgetKiB": 1}))
    return str(cfg)


def test_bundle_passes_when_private_code_is_lazy(tmp_path):
    assert check_bundle.problems(_build(tmp_path, admin_static=False)) == []


def test_bundle_catches_private_code_and_budget(tmp_path):
    found = check_bundle.problems(_build(tmp_path, admin_static=True, size=600))
    assert any("private code" in p for p in found)
    assert any("budget" in p for p in found)


def test_bundle_fails_without_config(tmp_path):
    assert "missing" in check_bundle.problems(str(tmp_path / "nope.json"))[0]
