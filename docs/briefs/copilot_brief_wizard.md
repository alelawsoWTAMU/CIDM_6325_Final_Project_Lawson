# BRIEF: Build Home Onboarding Wizard slice

Goal

- Implement Multi-Step Home Onboarding Wizard addressing PRD §F-008.

Scope (single PR)

- Files to touch: `homes/models.py`, `homes/forms.py`, `homes/views.py`, `homes/urls.py`, `templates/homes/survey_step1.html`, `templates/homes/survey_step2.html`, `templates/homes/survey_step3.html`, `homes/migrations/0003_*.py`.
- Non-goals: Redesign of existing Home CRUD; API endpoints; mobile PWA.

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance

- User flow: Authenticated user can complete 3-step wizard (basic info → features/systems → appliances), data persists via session, submits final step to create `Home` and related `Appliance` records, redirected to schedule generation.
- Include migration? yes (new fields on `Home` and `Appliance`).
- Update docs & PR checklist.

Prompts for Copilot

- "Generate three Django ModelForms for wizard steps and a session-based CBV handling step progression."
- "Create templates with Bootstrap progress indicators and back/next controls."
- "Wire `homes/urls.py` with routes `/homes/wizard/` and `/homes/wizard/<int:step>/`."
- "Explain changes and propose commit messages."
- "Refactor into CBV while preserving behavior; show diff-ready patch."