"""Self-tests proving the governance scripts actually detect violations (and accept valid input)."""
import contextlib, io, json, sys, tempfile, unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import check_architecture as arch  # noqa: E402
import check_feature_register as freg  # noqa: E402
import check_pr as pr  # noqa: E402
import check_task_prompt as tp  # noqa: E402
import render_wizard as rw  # noqa: E402
import scan_secrets as sec  # noqa: E402
import wizard as wz  # noqa: E402

CFG = {
    "source_root": "src/modules", "aliases": ["@modules/"],
    "public_entry_names": ["index", "__init__"], "public_dirs": ["public"],
    "modules": {
        "shared": {"allowed_dependencies": []},
        "billing": {"allowed_dependencies": ["shared"]},
        "orders": {"allowed_dependencies": ["shared", "billing"]},
    },
    "forbidden_imports": [{"pattern": "^express$", "applies_to_modules": ["shared"], "reason": "no frameworks in shared"}],
}


def tree(files, cfg=CFG):
    tmp = Path(tempfile.mkdtemp())
    for rel, text in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    (tmp / "modules.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp


def run_arch(files, cfg=CFG):
    t = tree(files, cfg)
    return arch.check(t, t / "modules.json")[0]


class ArchitectureGuardrail(unittest.TestCase):
    def test_real_repository_is_clean(self):
        v, scanned = arch.check(REPO, REPO / "docs/architecture/modules.json")
        self.assertEqual(v, [])
        self.assertGreater(scanned, 0)

    def test_allowed_public_import_passes(self):
        self.assertEqual(run_arch({"src/modules/orders/a.ts": "import {x} from '../billing';",
                                   "src/modules/billing/index.ts": "export const x=1;"}), [])

    def test_disallowed_direction_fails(self):
        v = run_arch({"src/modules/billing/a.ts": "import {o} from '../orders';",
                      "src/modules/orders/index.ts": "export const o=1;"})
        self.assertTrue(any("may not depend on 'orders'" in m for m in v))

    def test_deep_import_fails(self):
        v = run_arch({"src/modules/orders/a.ts": "import {x} from '../billing/internal/db';"})
        self.assertTrue(any("deep import" in m for m in v))

    def test_alias_import_and_public_dir(self):
        self.assertEqual(run_arch({"src/modules/orders/a.ts": "import {x} from '@modules/billing/public/api';"}), [])
        v = run_arch({"src/modules/orders/a.ts": "import {x} from '@modules/billing/repo';"})
        self.assertTrue(any("deep import" in m for m in v))

    def test_observed_cycle_detected(self):
        cfg = json.loads(json.dumps(CFG))
        cfg["modules"]["billing"]["allowed_dependencies"] = ["shared", "orders"]
        v = run_arch({"src/modules/orders/a.ts": "import 'x'; import {b} from '../billing';",
                      "src/modules/billing/a.ts": "import {o} from '../orders';"}, cfg)
        self.assertTrue(any("circular" in m for m in v))

    def test_config_cycle_detected(self):
        cfg = json.loads(json.dumps(CFG))
        cfg["modules"]["shared"]["allowed_dependencies"] = ["orders"]
        self.assertTrue(any("circular allowed_dependencies" in m for m in run_arch({}, cfg)))

    def test_unregistered_module_fails(self):
        v = run_arch({"src/modules/newthing/a.ts": "export {}"})
        self.assertTrue(any("not registered" in m for m in v))

    def test_forbidden_import_fails(self):
        v = run_arch({"src/modules/shared/a.ts": "import express from 'express';"})
        self.assertTrue(any("forbidden import" in m for m in v))

    def test_python_relative_deep_import_fails(self):
        v = run_arch({"src/modules/orders/svc.py": "from ..billing.models import Invoice\n"})
        self.assertTrue(any("deep import" in m for m in v))
        self.assertEqual(run_arch({"src/modules/orders/svc.py": "from ..billing import refund\n"}), [])


def prompt(approved=True, drop=None, body="Do the thing carefully and verify it well."):
    blocks = ["Role", "Context", "Objective", "Scope and non-goals", "Constraints", "Acceptance criteria", "Verification and handoff"]
    parts = ["Task-ID: FEAT-009"]
    if approved:
        parts.append("Gate-5-approval: Approved by Sam Lee 2026-01-05")
    for i, b in enumerate(blocks, 1):
        if b == drop:
            continue
        content = "- first observable criterion\n- second observable criterion" if b == "Acceptance criteria" else body
        parts.append(f"## {i}. {b}\n{content}\n")
    return "\n".join(parts)


class TaskPrompt(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(tp.check_text(prompt()), [])

    def test_unapproved(self):
        self.assertTrue(any("not approved" in e for e in tp.check_text(prompt(approved=False))))

    def test_missing_block(self):
        self.assertTrue(tp.check_text(prompt(drop="Constraints")))

    def test_placeholder(self):
        self.assertTrue(any("placeholder" in e for e in tp.check_text(prompt(body="{{fill this in later please}}"))))

    def test_template_is_not_valid_as_a_task(self):
        self.assertTrue(tp.check_text((REPO / "prompts/seven-block-prompt.md").read_text(encoding="utf-8")))


def reg(status, approval, evidence="-"):
    h = "| " + " | ".join(freg.COLS) + " |\n|" + "---|" * len(freg.COLS) + "\n"
    row = ["FEAT-001", "t", "v", "MVP1", "Must", "orders", "-", "-", "unit", "a", approval, status, evidence]
    return h + "| " + " | ".join(row) + " |\n"


class FeatureRegister(unittest.TestCase):
    def test_repo_register_valid(self):
        self.assertEqual(freg.check_text((REPO / "docs/roadmap/feature-register.md").read_text(encoding="utf-8")), [])

    def test_unapproved_work_rejected(self):
        self.assertTrue(freg.check_text(reg("In-Progress", "Pending")))

    def test_release_needs_evidence(self):
        self.assertTrue(freg.check_text(reg("Released", "Approved")))
        self.assertEqual(freg.check_text(reg("Released", "Approved", "PR #12, CI run 345")), [])


class PullRequest(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(pr.check_text("Item: FEAT-003\n- [x] done\n")) # incomplete metadata is now rejected

    def test_missing_reference(self):
        self.assertTrue(pr.check_text("fixes stuff\n- [x] done"))

    def test_trivial(self):
        self.assertTrue(pr.check_text("Trivial-change: yes\n")) # actual changed files and evidence required

    def test_unchecked_item(self):
        self.assertTrue(pr.check_text("FEAT-1\n- [ ] tests added\n"))
        self.assertTrue(pr.check_text("FEAT-1\n- [ ] perf check N/A: no hot path\n")) # a lone N/A cannot replace the PR

    def test_repo_template_requires_work_from_author(self):
        body = (REPO / ".github/pull_request_template.md").read_text(encoding="utf-8")
        self.assertTrue(pr.check_text(body))


class SecretScan(unittest.TestCase):
    def test_detects_and_ignores(self):
        t = Path(tempfile.mkdtemp())
        (t / "ok.txt").write_text("nothing here\n")
        self.assertEqual(sec.scan(t)[0], [])
        (t / "bad.py").write_text("key = '" + "AKIA" + "ABCDEFGHIJKLMNOP" + "'\n")
        (t / "pw.js").write_text("const password = " + '"' + "x" * 20 + '"' + ";\n")
        names = {n for _, _, n in sec.scan(t)[0]}
        self.assertIn("aws-access-key-id", names)
        self.assertIn("hardcoded-credential", names)
        (t / ".secrets-allowlist").write_text("bad.py\npw.js\n")
        self.assertEqual(sec.scan(t)[0], [])

    def test_repo_clean(self):
        self.assertEqual(sec.scan(REPO)[0], [])


class Wizard(unittest.TestCase):
    data = rw.load(REPO / "docs/wizard/questions.json")

    def test_rendered_file_in_sync(self):
        self.assertEqual((REPO / "docs/wizard/WIZARD.md").read_text(encoding="utf-8"), rw.render(self.data))

    def test_defaults_mode_flags_assumptions(self):
        rows = wz.run(self.data, use_defaults=True)
        self.assertEqual(len(rows), len(self.data["questions"]))
        text = wz.render_profile(rows)
        self.assertIn("assumed-default", text)
        self.assertIn("NOT ANSWERED", text)
        self.assertNotIn("| Approved |", text)

    def test_interactive_one_question_at_a_time(self):
        answers = iter(["A story", "Clinic staff and patients", "30 clinics in 90 days", ""])
        asked = []

        def ask(prompt):
            asked.append(prompt)
            return next(answers)  # raises StopIteration (test fails) if the wizard asks more than expected

        small = {"topics": self.data["topics"], "questions": self.data["questions"][:4]}
        with contextlib.redirect_stdout(io.StringIO()):
            rows = wz.run(small, ask=ask, say=lambda *_: None)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(asked), 4)  # exactly one prompt per question
        self.assertEqual(rows[0][1], "A story")
        self.assertEqual(rows[3][2], "default-accepted")


if __name__ == "__main__":
    unittest.main()
