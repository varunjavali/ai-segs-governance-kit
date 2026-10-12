"""Corrections: deliberate invalid inputs and legitimate controls, offline only."""
import copy, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

from test_guardrails import CFG, tree, run_arch, reg, prompt, REPO
import check_architecture as arch
import check_feature_register as freg
import check_pr as pr
import wizard as wz


def valid_pr(trivial=False):
    item = 'Trivial-change: yes' if trivial else 'Item: FEAT-001'
    labels = ['Scope', 'Register', 'Governance', 'Stack', 'Tests', 'Integrity',
              'Architecture', 'Security', 'Accessibility/performance', 'Rollback']
    checklist = '\n'.join('- [x] '+label+': verified for this change' for label in labels)
    return f'''## Linked item
{item}
## What and why
Correct the documented validation defect and preserve valid behavior.
## Scope check
{checklist}
## Author checklist
Evidence reviewed with the checks above.
## Verification evidence
Command: python -m unittest discover -s tests
Exit-code: 0
Outcome: 12 tests passed, including the regression and valid input cases.
## AI handoff report (if AI-assisted)
Changed validator and tests; no application stack selected. Local evidence only.
'''


def records():
    t = tree({})
    p = t/'docs/roadmap/feature-register.md'; p.parent.mkdir(parents=True)
    p.write_text(reg('Ready','Approved','Gate 2 signed in project gate log'))
    p = t/'prompts/tasks/FEAT-001-validation.md'; p.parent.mkdir(parents=True)
    p.write_text('Tier: T2\n'+prompt().replace('FEAT-009','FEAT-001'))
    return t


class Corrections(unittest.TestCase):
    def test_from_list_internal(self):
        self.assertTrue(run_arch({'src/modules/orders/service.py':'from ..billing import internal\n',
                                  'src/modules/billing/internal.py':'PRIVATE_DATA = {}\n'}))

    def test_multiple_aliases(self):
        self.assertTrue(run_arch({'src/modules/billing/service.py':'import os, src.modules.orders.internal\n',
                                  'src/modules/orders/internal.py':'PRIVATE_DATA = {}\n'}))

    def test_public_symbols_and_submodules(self):
        self.assertEqual(run_arch({'src/modules/orders/service.py':'from ..billing import refund\nfrom ..billing.public import api\n',
                                  'src/modules/billing/__init__.py':'def refund(): pass\n',
                                  'src/modules/billing/public/api.py':'VALUE=1\n'}), [])

    def test_absolute_from_list(self):
        self.assertTrue(run_arch({'src/modules/orders/service.py':'from src.modules import billing\nfrom src.modules.billing import internal as x\n',
                                  'src/modules/billing/internal.py':'X=1\n'}))

    def test_missing_and_empty_sources(self):
        t = tree({}); self.assertTrue(arch.check(t,t/'modules.json')[0])
        (t/'src/modules').mkdir(parents=True)
        self.assertTrue(arch.check(t,t/'modules.json')[0])
        cfg = dict(CFG,allow_empty_bootstrap=True); (t/'modules.json').write_text(json.dumps(cfg))
        self.assertEqual(arch.check(t,t/'modules.json'),([],0))

    def test_syntax_error_fails(self):
        self.assertTrue(run_arch({'src/modules/orders/service.py':'from x import (\n'}))

    def test_empty_registers(self):
        for text in ['', '# Feature Register', '| Wrong | Header |\n|---|---|']:
            with self.subTest(text=text): self.assertTrue(freg.check_text(text))

    def test_register_header_and_fields(self):
        self.assertTrue(freg.check_text(reg('Ready','Approved')+reg('Proposed','Pending')))
        self.assertTrue(freg.check_text(reg('Proposed','Pending').replace('| unit |','| - |')))
        self.assertTrue(freg.check_text(reg('Approved','Pending')))
        self.assertTrue(freg.check_text(reg('Rejected','Approved')))
        self.assertTrue(freg.check_text(reg('Proposed','Approved','Gate 2 signed in gate log')))
        self.assertTrue(freg.check_text(reg('Ready','Approved').replace('---|','oops|',1)))
        duplicate=reg('Proposed','Pending')+reg('Proposed','Pending').splitlines()[-1]+'\n'
        self.assertTrue(any('duplicate ID' in e for e in freg.check_text(duplicate)))
        self.assertTrue(freg.check_text(reg('Ready','Approved','N/A')))
        self.assertEqual(freg.check_text(reg('Rejected','Rejected')),[])

    def test_empty_bootstrap_register(self):
        header = reg('Proposed','Pending').splitlines()[:2]
        text = '\n'.join(header)
        self.assertTrue(freg.check_text(text))
        self.assertEqual(freg.check_text('Bootstrap-empty: yes\n'+text),[])

    def test_pr_id_only_and_na_only_fail(self):
        self.assertTrue(pr.check_text('FEAT-001'))
        self.assertTrue(pr.check_text('FEAT-001\n- [ ] Tests N/A'))
        self.assertTrue(pr.check_text('Trivial-change: yes'))

    def test_valid_pr_and_trivial(self):
        self.assertEqual(pr.check_text(valid_pr(), root=records(), changed_files=['scripts/check_pr.py']),[])
        self.assertEqual(pr.check_text(valid_pr(True), root=records(), changed_files=['docs/guide.md']),[])

    def test_trivial_denies_sensitive_paths(self):
        for name in ['src/a.py','docs/security/policy.md','docs/architecture/modules.json',
                     '.github/workflows/a.yml','migrations/1.sql','scripts/check_pr.py',
                     'package.json','docs/governance/workflow.md','AGENTS.md']:
            with self.subTest(name=name):
                self.assertTrue(pr.check_text(valid_pr(True),root=records(),changed_files=[name]))

    def test_pr_record_and_evidence_fail_closed(self):
        root = records()
        for body in [valid_pr().replace('FEAT-001','FEAT-999'), valid_pr().replace('Exit-code: 0','Exit-code: nope'),
                     valid_pr().replace('Outcome: 12 tests passed, including the regression and valid input cases.','Outcome: pass'),
                     valid_pr().replace('- [x] Security: verified for this change','- [ ] Security N/A: no')]:
            self.assertTrue(pr.check_text(body,root=root,changed_files=['src/a.py']))
        p=root/'docs/roadmap/feature-register.md'; p.write_text(reg('Proposed','Pending'))
        self.assertTrue(pr.check_text(valid_pr(),root=root,changed_files=['src/a.py']))

    def test_valid_na_and_required_controls(self):
        body=valid_pr(True).replace('- [x] Stack: verified for this change',
                                  '- [ ] Stack: N/A: explanatory wording only; no application files changed')
        self.assertEqual(pr.check_text(body,root=records(),changed_files=['README.md']),[])
        self.assertTrue(pr.check_text(body.replace('- [x] Governance: verified for this change',
                                                  '- [ ] Governance: N/A: wording only and no code change'),
                                      root=records(),changed_files=['README.md']))
        self.assertTrue(pr.check_text(body.replace('Exit-code: 0','Exit-code: 1'),
                                      root=records(),changed_files=['README.md']))

    def test_duplicate_unapproved_task(self):
        root=records();p=root/'prompts/tasks/FEAT-001-validation.md'
        (p.parent/'duplicate.md').write_text(p.read_text())
        self.assertTrue(pr.check_text(valid_pr(),root=root,changed_files=['src/a.py']))
        (p.parent/'duplicate.md').unlink()
        p.write_text(p.read_text().replace('Approved by Sam Lee 2026-01-05','Pending'))
        self.assertTrue(pr.check_text(valid_pr(),root=root,changed_files=['src/a.py']))

    def test_pr_cli_actual_git_diff(self):
        root=records()
        def git(*args):
            r=subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,text=True)
            return r.stdout.strip()
        git('init');git('add','.')
        git('-c','user.name=Offline test fixture','-c','user.email=fixture@example.invalid','commit','--no-gpg-sign','-m','base fixture')
        base=git('rev-parse','HEAD')
        (root/'docs/guide.md').write_text('Explanatory documentation wording')
        git('add','.');git('-c','user.name=Offline test fixture','-c','user.email=fixture@example.invalid','commit','--no-gpg-sign','-m','wording fixture')
        head=git('rev-parse','HEAD');body=root/'pr-body.txt';body.write_text(valid_pr(True))
        cmd=[sys.executable,str(REPO/'scripts/check_pr.py'),'--root',str(root),'--body-file',str(body),
             '--base',base,'--head',head]
        r=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        p=root/'src/modules/orders/service.py';p.parent.mkdir(parents=True);p.write_text('VALUE=1\n')
        git('add','.');git('-c','user.name=Offline test fixture','-c','user.email=fixture@example.invalid','commit','--no-gpg-sign','-m','application fixture')
        cmd[-1]=git('rev-parse','HEAD')
        r=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(r.returncode,1,r.stdout+r.stderr)
        cmd[-1]='--not-a-ref'
        self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)

    def test_wizard_specify_and_deferral(self):
        data={'topics':{'1':'Idea'},'questions':[
            {'id':'Q01','topic':1,'gate':0,'question':'Explain the goal','why':'Sets scope',
             'options':[{'key':'A','label':'Other (specify)','tradeoff':'Choose carefully'}],
             'default':'A','can_defer':True}]}
        replies=iter(['','Named stack proposal'])
        saved=[]
        rows=wz.run(data,ask=lambda _:next(replies),say=lambda _:None,save=lambda r:saved.append(list(r)))
        self.assertEqual(rows[0][1],'A - Other (specify): Named stack proposal')
        self.assertEqual(len(saved),1)
        rows=wz.run(data,ask=lambda _:'d',say=lambda _:None)
        self.assertEqual(rows[0][2],'deferred')

    def test_wizard_other_without_changing_question_catalog(self):
        import render_wizard as rw
        catalog=rw.load(REPO/'docs/wizard/questions.json')
        question=next(q for q in catalog['questions'] if q['id']=='Q14')
        data={'topics':catalog['topics'],'questions':[question]}
        before=json.dumps(data,sort_keys=True)
        answers=iter(['o','','o','GitHub repository and Actions; local CLI; no application hosting or database'])
        saved=[];shown=[]
        rows=wz.run(data,ask=lambda _:next(answers),say=shown.append,save=lambda r:saved.append(list(r)))
        self.assertEqual(rows[0][2],'chosen-other')
        self.assertIn('no application hosting or database',rows[0][1])
        self.assertEqual(len(saved),1)
        self.assertIn('| Pending |',wz.render_profile(rows))
        self.assertEqual(json.dumps(data,sort_keys=True),before)
        self.assertTrue(any('o)' in line for line in shown))

    def test_demo_prompt_not_canonical(self):
        root=records(); p=root/'prompts/tasks/FEAT-001-validation.md'
        text=p.read_text(); p.unlink()
        p=root/'prompts/examples/FEAT-001.md';p.parent.mkdir(parents=True);p.write_text(text)
        self.assertTrue(pr.check_text(valid_pr(),root=root,changed_files=['src/a.py']))

    def test_wizard_saves_after_interruption_and_resumes(self):
        root=Path(tempfile.mkdtemp()); (root/'docs/wizard').mkdir(parents=True)
        data={'topics':{'1':'Idea'},'questions':[
            {'id':q,'topic':1,'gate':0,'question':'Explain the goal','why':'Sets scope',
             'options':[],'default':None,'can_defer':False} for q in ['Q01','Q02']]}
        (root/'docs/wizard/questions.json').write_text(json.dumps(data))
        with patch('builtins.input',side_effect=['First proposal',EOFError()]):
            self.assertEqual(wz.main(['--root',str(root)]),1)
        state=root/'docs/decisions/wizard-progress.json'
        self.assertTrue(state.exists())
        self.assertEqual(len(json.loads(state.read_text())['answers']),1)
        with patch('builtins.input',return_value='Second proposal') as ask:
            self.assertEqual(wz.main(['--root',str(root),'--resume']),0)
            self.assertEqual(ask.call_count,1)
        profile=root/'docs/decisions/project-profile.md'
        old=profile.read_bytes()
        self.assertNotEqual(wz.main(['--root',str(root),'--defaults']),0)
        self.assertEqual(profile.read_bytes(),old)
        self.assertNotIn('| Approved |',profile.read_text())


class BranchProtection(unittest.TestCase):
    def test_reported_partial_response_is_rejected(self):
        # Independent of the new helper: this assertion fails against the original shell script.
        response={'required_pull_request_reviews':{'required_approving_review_count':1,'require_code_owner_reviews':True},
                  'enforce_admins':{'enabled':True},'allow_force_pushes':{'enabled':False},
                  'required_status_checks':{'contexts':['governance-checks']}}
        bash=r'C:\Program Files\Git\bin\bash.exe' if os.name=='nt' else 'bash'
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp);(t/'response.json').write_text(json.dumps(response,separators=(',',':')))
            (t/'gh').write_text('#!/usr/bin/env bash\ncat "$MOCK_DIR/response.json"\n');(t/'gh').chmod(0o755)
            env=dict(os.environ,MOCK_DIR=t.as_posix(),PYTHON=sys.executable.replace('\\','/'))
            cmd='export PATH="$(cygpath -u "$MOCK_DIR" 2>/dev/null || echo "$MOCK_DIR"):$PATH"; bash scripts/configure_branch_protection.sh --verify test/offline main'
            r=subprocess.run([bash,'-c',cmd],cwd=REPO,env=env,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0,r.stdout+r.stderr)

    def test_structured_policy_each_field(self):
        import check_branch_protection as bp
        policy=bp.policy(2)
        response=copy.deepcopy(policy)
        for key in ['enforce_admins','required_linear_history','allow_force_pushes','allow_deletions','required_conversation_resolution']:
            response[key]={'enabled':policy[key]}
        self.assertEqual(bp.check(response,2),[])
        self.assertTrue(bp.check(response,1))
        for key in policy:
            broken=copy.deepcopy(response); del broken[key]
            with self.subTest(key=key): self.assertTrue(bp.check(broken,2))
        for key in ['enforce_admins','required_linear_history','allow_force_pushes','allow_deletions','required_conversation_resolution']:
            broken=copy.deepcopy(response); broken[key]['enabled']=not policy[key]
            self.assertTrue(bp.check(broken,2))
        for key in ['dismiss_stale_reviews','require_code_owner_reviews','required_approving_review_count']:
            broken=copy.deepcopy(response); broken['required_pull_request_reviews'][key]=False
            self.assertTrue(bp.check(broken,2))
        for context in ['governance-checks','pr-metadata']:
            broken=copy.deepcopy(response); broken['required_status_checks']['contexts'].remove(context)
            self.assertTrue(bp.check(broken,2))
        broken=copy.deepcopy(response); broken['required_status_checks']['strict']=False
        self.assertTrue(bp.check(broken,2))
        broken=copy.deepcopy(response); broken['restrictions']={}
        self.assertTrue(bp.check(broken,2))

    def test_mock_api_shell_round_trip(self):
        import check_branch_protection as bp
        bash=os.environ.get('TEST_BASH',r'C:\Program Files\Git\bin\bash.exe') if os.name=='nt' else 'bash'
        if not Path(bash).exists() and os.name=='nt': self.fail('Git Bash required for offline shell verification')
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp); response=bp.policy(1)
            for k in ['enforce_admins','required_linear_history','allow_force_pushes','allow_deletions','required_conversation_resolution']:
                response[k]={'enabled':response[k]}
            (t/'response.json').write_text(json.dumps(response))
            gh=t/'gh';gh.write_text('#!/usr/bin/env bash\nif [[ "$*" == *"-X PUT"* ]]; then cat > "$MOCK_DIR/request.json"; fi\ncat "$MOCK_DIR/response.json"\n')
            gh.chmod(0o755)
            env=dict(os.environ,MOCK_DIR=t.as_posix(),PYTHON=sys.executable.replace('\\','/'))
            command='export PATH="$(cygpath -u "$MOCK_DIR" 2>/dev/null || echo "$MOCK_DIR"):$PATH"; bash scripts/configure_branch_protection.sh '
            for mode in ['--apply','--verify']:
                r=subprocess.run([bash,'-c',command+mode+' test/offline main'],cwd=REPO,env=env,capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertEqual(json.loads((t/'request.json').read_text()),bp.policy(1))
            response['required_status_checks']['strict']=False
            (t/'response.json').write_text(json.dumps(response))
            r=subprocess.run([bash,'-c',command+'--verify test/offline main'],cwd=REPO,env=env,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)


if __name__=='__main__': unittest.main()
