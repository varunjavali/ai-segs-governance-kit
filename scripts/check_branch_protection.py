#!/usr/bin/env python3
"""Canonical requested protection policy and structured read-back validation."""
import argparse, json, sys


def policy(reviews=1):
    if type(reviews) is not int or not 1 <= reviews <= 6:
        raise ValueError('REVIEWS must be an integer from 1 through 6')
    return {
        'required_status_checks': {'strict': True, 'contexts': ['governance-checks','pr-metadata']},
        'enforce_admins': True,
        'required_pull_request_reviews': {'required_approving_review_count': reviews,
            'require_code_owner_reviews': True, 'dismiss_stale_reviews': True},
        'restrictions': None, 'required_linear_history': True, 'allow_force_pushes': False,
        'allow_deletions': False, 'required_conversation_resolution': True}


def check(actual, reviews=1):
    expected=policy(reviews); errs=[]
    if not isinstance(actual,dict): return ['API response must be a JSON object']
    for key, value in expected.items():
        got=actual.get(key)
        if key=='required_status_checks':
            if not isinstance(got,dict) or got.get('strict') is not True:
                errs.append('required_status_checks.strict must be true')
            contexts=got.get('contexts',[]) if isinstance(got,dict) else []
            checks=got.get('checks',[]) if isinstance(got,dict) else []
            names=set(contexts) if isinstance(contexts,list) and all(isinstance(x,str) for x in contexts) else set()
            if isinstance(checks,list): names.update(x.get('context') for x in checks if isinstance(x,dict) and isinstance(x.get('context'),str))
            for name in value['contexts']:
                if name not in names: errs.append('missing required status check: '+name)
        elif isinstance(value,dict):
            for sub, want in value.items():
                found=got.get(sub) if isinstance(got,dict) else None
                if type(found)!=type(want) or found!=want: errs.append(f'{key}.{sub} must equal {want}')
        elif key=='restrictions':
            if key not in actual or got is not None: errs.append('restrictions must be present and null')
        elif not isinstance(got,dict) or got.get('enabled') is not value:
            errs.append(f'{key}.enabled must be {value}')
    return errs


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reviews',type=int,default=1); ap.add_argument('--policy',action='store_true')
    a=ap.parse_args()
    try:
        if a.policy: print(json.dumps(policy(a.reviews))); return 0
        errs=check(json.load(sys.stdin),a.reviews)
    except (ValueError,TypeError) as e: print('protection error:',e); return 2
    for err in errs: print('FAIL',err)
    if not errs: print('all requested branch-protection settings match')
    return int(bool(errs))


if __name__=='__main__': sys.exit(main())
