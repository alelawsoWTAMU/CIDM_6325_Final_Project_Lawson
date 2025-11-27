# ADR-2025-11-26 Home Onboarding Wizard

Date: 2025-11-26  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: Project Instructor

---

## Links and traceability

PRD link: docs/prd/Module 2 - PRD.md (F-008)  
Scope IDs from PRD: F-008, DOC-001  
Functional requirements: FR-F-008-1 (multi-step intake), FR-F-008-2 (appliance capture), FR-F-008-3 (auto schedule)  
Related issues or PRs: #wizard-impl, #wizard-migrations

---

## Intent and scope

Adopt a session-based, three-step onboarding wizard to collect comprehensive home details for new homeowners and automatically create a personalized maintenance schedule. In scope: forms, views, templates, model fields, and migrations to support wizard data. Out of scope: API endpoints, mobile PWA, notification system.

---

## Problem and forces

- New homeowners need guided data entry to provide sufficient details for quality recommendations.  
- Tradeoffs: complexity of multi-step state vs. single-page forms; session serialization; validation across steps.  
- Constraints: Django 5.x, Bootstrap 5, Windows dev env, Render deployment.

---

## Options considered

- **A)** Session-based wizard (chosen)  
  - Pros: Simple, no extra deps, fits Django patterns  
  - Cons: Manual serialization, step validation logic
- **B)** Form wizard package (django-formtools)  
  - Pros: Built-in step management  
  - Cons: Extra dependency, less control over custom flow
- **C)** Single large form  
  - Pros: Simplest implementation  
  - Cons: Poor UX, error-prone, hard to track appliances

---

## Decision

We choose A (session-based wizard) because it provides control over the user flow, avoids extra dependencies, and integrates cleanly with existing forms and views.

Decision drivers ranked:  
D1: UX quality  
D2: Maintainability  
D3: Dependency minimalism

---

## Consequences

Positive  
- Guided intake improves data completeness and accuracy  
- Enables auto-generation of personalized schedules  
- Scales to multiple appliances and features

Negative and risks  
- Session serialization for Decimal/date objects  
- Step boundary validation complexity

Mitigations  
- Convert complex types to strings for session storage and back on retrieval  
- Centralize step validation in view methods

---

## Requirements binding

- FR-F-008-1: Users can complete a 3-step wizard with persisted state  
- FR-F-008-2: Users can add multiple appliances with serial/energy/service details  
- FR-F-008-3: Completing the wizard creates the home and appliances, then redirects to schedule generation  
- DOC-001: Update README/QUICKSTART with wizard docs

---

## Acceptance criteria snapshot

- AC1: `/homes/wizard/` loads step 1 and records submissions  
- AC2: Step 2 records features/systems including roof/HVAC/siding  
- AC3: Step 3 allows adding multiple appliances and finalizes  
- Evidence: URLs, screenshots, server logs showing redirects

---

## Implementation outline

Plan  
- Step 1: Add fields to `Home` and `Appliance`; create migration  
- Step 2: Build 3 ModelForms and CBV managing session and steps  
- Step 3: Create 3 templates with progress indicators; add URLs; integrate with schedule generation

Denied paths  
- Do not use external wizard packages; avoid single giant form

Artifacts to update  
- Code paths: `homes/models.py`, `homes/forms.py`, `homes/views.py`, `homes/urls.py`  
- Settings and secrets: none  
- Migrations: `homes/migrations/0003_*`  
- Templates and static assets: `templates/homes/survey_step*.html`

---

## Test plan and invariants

Invariants  
- INV-1: Wizard state persists across steps per session  
- INV-2: Finalization creates Home and Appliances atomically

Unit tests  
- tests/test_wizard.py: step transitions, session data handling, finalization behavior

Behavioral tests (optional)  
- High-level user flow across steps

Performance and accessibility checks  
- Ensure WCAG AA color contrast in progress bars

---

## Documentation updates

- README: add wizard feature and links  
- QUICKSTART: add wizard steps and usage  
- TODO.md: mark feature complete

---

## Rollback and contingency

Rollback trigger  
- Errors in session handling or data integrity  

Rollback steps  
- git revert of wizard PR; retain fields for compatibility

Data and config safety  
- No destructive migrations; new fields are additive

---

## Attestation plan

Human witness  
- Instructor to attest with screenshots and commit refs

Attestation record  
- Commit hash and brief rationale  
- Path: docs/attestations/ADR-2025-11-26-wizard.md

---

## Checklist seed

- [x] Traceability fields complete  
- [x] Decision and drivers documented  
- [x] Requirements binding lists testable behaviors  
- [x] Acceptance criteria snapshot defined  
- [x] Implementation steps and denied paths listed  
- [x] Tests named with files and invariants specified  
- [x] Docs updates and changelog listed  
- [x] Rollback trigger and steps documented  
- [x] Attestation plan recorded

---

## References

- Django docs: CBVs, sessions, ModelForms  
- Bootstrap 5 docs: progress components
