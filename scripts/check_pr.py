#!/usr/bin/env python3
"""PR structure, evidence, changed paths and canonical approval metadata.
Recorded metadata does not authenticate a human approval.
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path, PurePosixPath
import check_feature_register as freg
import check_task_prompt as task

REF = re.compile(r'\b(?:FEAT|BUG|CHG|TASK|DEBT)-\d+\b')
TRIVIAL = re.compile(r'^\s*Trivial-change:\s*yes\s*$', re.I | re.M)
SECTIONS = ['Linked item','What and why','Scope check','Author checklist',
            'Verification evidence','AI handoff report (if AI-assisted)']
CHECKS = ['Scope','Register','Governance','Stack','Tests','Integrity',
          'Architecture','Security','Accessibility/performance','Rollback']

def substantive(value, minimum=12):
    return len(value.strip()) >= minimum and not re.search(r'\b(?:TBD|TODO|FIXME)\b|<[^>]+>|\{\{',value,re.I)

def trivial_path(name):
    p=PurePosixPath(name.replace('\\','/'))
    if p.is_absolute() or '..' in p.parts or p.suffix.lower() != '.md': return False
    if str(p) in {'README.md','tests/README.md','src/README.md'}: return True
    return len(p.parts)>1 and p.parts[0]=='docs' and p.parts[1] not in {
        'security','architecture','governance','deployment','operations','decisions',
        'requirements','roadmap','api','design-system','wizard','team','testing','registers'}

def canonical_errors(root, item):
    errs=[]; files=[]
    for p in (root/'prompts/tasks').glob('*.md'):
        text=p.read_text(encoding='utf-8')
        if re.search(r'^Task-ID:\s*'+re.escape(item)+r'\s*$',text,re.M): files.append((p,text))
    if len(files)!=1:
        return [f'{item}: require exactly one canonical task in prompts/tasks (examples are not approvals)']
    p,text=files[0]
    errs += [f'{item}: {e}' for e in task.check_text(text)]
    if re.search(r'\b(?:EXAMPLE|fictional|illustrative)\b',text,re.I): errs.append(f'{item}: demonstration approval is not canonical')
    if not re.search(r'^Tier:\s*T[123]\s*$',text,re.M): errs.append(f'{item}: task needs Tier T1/T2/T3')
    approval=re.search(r'^Gate-5-approval:\s*Approved by\s+(.+?)\s+(\d{4}-\d{2}-\d{2})\s*$',text,re.M)
    if not approval or re.search(r'<|>|\b(?:AI|Codex|Claude|example|name|pending)\b',approval.group(1),re.I):
        errs.append(f'{item}: require named human approval metadata with date')
    else:
        from datetime import date
        try: date.fromisoformat(approval.group(2))
        except ValueError: errs.append(f'{item}: invalid approval date')
    if item.startswith('FEAT-'):
        register=root/'docs/roadmap/feature-register.md'
        if not register.is_file(): return errs+['canonical feature register missing']
        data=register.read_text(encoding='utf-8')
        errs += [f'feature register: {e}' for e in freg.check_text(data)]
        rows=[]
        for line in data.splitlines():
            cells=[c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells)==len(freg.COLS) and cells[0]==item: rows.append(dict(zip(freg.COLS,cells)))
        if len(rows)!=1 or rows[0]['Approval']!='Approved' or rows[0]['Status'] not in freg.NEEDS_APPROVAL:
            errs.append(f'{item}: canonical feature must be approved and active, with evidence')
    return errs

def check_text(body, root=None, changed_files=None):
    body=re.sub(r'<!--.*?-->','',body or '',flags=re.S)
    errs=[]; sections={}
    heads=list(re.finditer(r'^##\s+(.+?)\s*$',body,re.M))
    for i,h in enumerate(heads):
        title=h.group(1)
        if title in sections: errs.append('duplicate section: '+title)
        sections[title]=body[h.end():heads[i+1].start() if i+1<len(heads) else len(body)].strip()
    for title in SECTIONS:
        if title not in sections or not substantive(sections[title]): errs.append('missing/empty section: '+title)
    checks={}
    for line in body.splitlines():
        m=re.match(r'^\s*[-*]\s+\[([ xX])\]\s+([^:]+):\s*(.*)$',line)
        if m:
            label=m.group(2).strip(); value=m.group(3).strip()
            if label in checks: errs.append('duplicate checklist item: '+label)
            checks[label]=True
            na=re.match(r'N/A\s*:\s*(.*)',value,re.I)
            if m.group(1)==' ' and not na: errs.append('unchecked checklist item: '+label)
            if not substantive(na.group(1) if na else value): errs.append('meaningful result or N/A reason required: '+label)
            if na and label in {'Scope','Register','Governance','Integrity','Architecture'}:
                errs.append('required control cannot be N/A: '+label)
        elif re.match(r'^\s*[-*]\s+\[[ xX]\]',line): errs.append('checklist items need label: result or N/A: reason')
    for label in CHECKS:
        if label not in checks: errs.append('required checklist item: '+label)
    evidence=sections.get('Verification evidence','')
    if not re.search(r'^Command:[ \t]*\S.{10,}$',evidence,re.M): errs.append('verification needs exact Command')
    if not re.search(r'^Exit-code:[ \t]*\d+[ \t]*$',evidence,re.M): errs.append('verification needs numeric Exit-code')
    outcome=re.search(r'^Outcome:[ \t]*(.+)$',evidence,re.M)
    if not outcome or not substantive(outcome.group(1),20): errs.append('verification needs substantive Outcome')
    commands=re.findall(r'^Command:[ \t]*(.*)$',evidence,re.M)
    codes=re.findall(r'^Exit-code:[ \t]*(.*)$',evidence,re.M)
    outcomes=re.findall(r'^Outcome:[ \t]*(.*)$',evidence,re.M)
    if len(commands)!=len(codes) or len(codes)!=len(outcomes): errs.append('each command needs exit code and outcome')
    if any(not substantive(c,12) for c in commands) or any(not substantive(o,20) for o in outcomes):
        errs.append('each verification group must be substantive')
    if any(c.strip()!='0' for c in codes): errs.append('required verification commands must pass; document not-run checks separately')
    refs=set(REF.findall(sections.get('Linked item','')))
    trivial=bool(TRIVIAL.search(sections.get('Linked item','')))
    if not refs and not trivial: errs.append('PR must link a canonical work item or declare Trivial-change: yes')
    if changed_files is None or not changed_files: errs.append('changed-file input required from actual diff')
    if trivial:
        if refs: errs.append('choose work-item controls or trivial declaration, not both')
        for path in changed_files or []:
            if not trivial_path(path): errs.append('trivial exception forbidden for changed path: '+path)
    elif root is None: errs.append('canonical repository root required')
    else:
        for item in sorted(refs): errs += canonical_errors(Path(root),item)
    return errs

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    g=ap.add_mutually_exclusive_group(required=True); g.add_argument('--env');g.add_argument('--body-file')
    ap.add_argument('--root',default='.')
    f=ap.add_mutually_exclusive_group(required=True);f.add_argument('--changed-files');f.add_argument('--base')
    ap.add_argument('--head',default='HEAD');a=ap.parse_args(argv)
    try:
        body=os.environ.get(a.env,'') if a.env else Path(a.body_file).read_text(encoding='utf-8')
        if a.changed_files:
            files=json.loads(Path(a.changed_files).read_text(encoding='utf-8'))
            if not isinstance(files,list) or not all(isinstance(p,str) for p in files): raise ValueError('changed files must be JSON string array')
        else:
            for ref in (a.base,a.head):
                if not re.fullmatch(r'[0-9a-fA-F]{40}',ref): raise ValueError('base/head must be full commit SHA inputs')
            result=subprocess.run(['git','diff','--name-only','--no-renames','-z',a.base,a.head,'--'],
                                  check=True,capture_output=True,cwd=a.root)
            files=[p for p in result.stdout.decode('utf-8').split('\0') if p]
        errs=check_text(body,Path(a.root),files)
    except (OSError,ValueError,subprocess.CalledProcessError) as e: print('PR input error:',e);return 2
    for e in errs: print('PR:',e)
    if errs: print('PR metadata check FAILED');return 1
    print('PR metadata check passed (recorded metadata only; human approval still required)');return 0

if __name__=='__main__': sys.exit(main())
