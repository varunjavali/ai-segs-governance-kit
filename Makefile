.RECIPEPREFIX = >
.PHONY: verify wizard wizard-defaults render-wizard setup-check
verify:            ## run every governance check (same as CI)
> bash scripts/verify_all.sh
wizard:            ## interactive discovery wizard
> python3 scripts/wizard.py
wizard-defaults:   ## record recommended defaults as UNAPPROVED assumptions
> python3 scripts/wizard.py --defaults
render-wizard:     ## regenerate docs/wizard/WIZARD.md from questions.json
> python3 scripts/render_wizard.py
setup-check:       ## Gate 4: fails while placeholders remain
> python3 scripts/check_docs.py --strict-setup
