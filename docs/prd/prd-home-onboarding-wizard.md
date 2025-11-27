# Product Requirements Document

## 1. Document information

- Product or feature name: Home Onboarding Wizard
- Author(s): Alexander J Lawson
- Date created: 2025-11-26
- Last updated: 2025-11-26
- Version: 1.0

---

## 2. Overview

- Summary: A three-step, session-based onboarding wizard that collects comprehensive home details (basic info, features/systems, appliances) to enable personalized maintenance schedules.
- Problem statement: New homeowners lack guided intake for critical property details; single-form entry leads to incomplete data and less accurate schedules.
- Goals and objectives:
  - Collect complete home profile information in a guided, user-friendly flow
  - Capture appliance inventory and key service metadata
  - Automatically generate a personalized maintenance schedule upon completion
- Non-goals:
  - Mobile PWA, notifications, API endpoints

---

## 3. Context and background

- Business context: Improves personalization and schedule accuracy, increasing user trust and engagement.
- Market or customer insights: First-time homeowners benefit from structured guidance; multi-step forms increase completion rates.
- Competitive or benchmark references: Common in consumer onboarding flows; aligns with UX best practices.

---

## 4. Scope items and checklist seeds

- [ ] **F-008 Wizard Flow**  
  User story As a new homeowner I want a guided multi-step wizard so that I can provide complete information to get a personalized schedule.  
  Acceptance notes
  - AC1 Step 1 collects basic info (address, year built, construction, climate, size, rooms)
  - AC2 Step 2 collects features/systems (roof type/age, HVAC type/age, siding, basement, attic)
  - AC3 Step 3 collects appliances (type, manufacturer, model, serial, energy rating, last service date)
  - AC4 Data persists via session and pre-fills across steps
  - AC5 Final submission creates `Home` and `Appliance` records and redirects to schedule generation
  Artifacts `homes/forms.py`, `homes/views.py`, `templates/homes/survey_step*.html`, `homes/models.py`, `homes/urls.py`  
  Owner Alexander J Lawson  Target version 1.0

**Out of scope**
- API endpoints or external integrations

---

## 5. Functional requirements bound to scope

- **FR-F-008-1** Step-based progression with session persistence  
  Rationale Enables guided UX and robust data capture  
  Trace F-008
- **FR-F-008-2** Appliance inventory supports multiple entries with serial and energy fields  
  Rationale Better warranty/service tracking  
  Trace F-008
- **FR-F-008-3** Auto redirect to schedule generation on completion  
  Rationale Immediate value and feedback loop  
  Trace F-008

---

## 6. Checklist to be generated from scope

- [ ] F-008 Wizard Flow — Steps complete (AC1–AC5) — Artifacts linked — Test date: ____ — Status: ____

---

## 7. Non functional requirements

- **NF-001 Performance** Wizard steps load < 300ms on dev, < 600ms on prod
- **NF-002 Accessibility** Progress indicators and forms meet WCAG AA
- **NF-003 Security** Auth required; CSRF tokens present; server-side validation
- **NF-004 Reliability** Session data persists across normal navigation and back/next

---

## 8. Dependencies

- Internal: `homes` app (models/views/forms/templates), `maintenance` app for redirect
- External: None

---

## 9. Risks and assumptions

- Risks: Session serialization of Decimal/date types; user abandonment mid-wizard
- Assumptions: Authenticated users; modern browsers; Bootstrap 5

---

## 10. Acceptance criteria

- Valid submissions create `Home` and `Appliance` objects; redirect occurs
- Session state recovered after page refresh
- Evidence: URLs, server logs, screenshots

---

## 11. Success metrics

- Completion rate of wizard (>70%)
- Average number of appliances added per user
- Reduction in incomplete home profiles

---

## 12. Rollout and release plan

- MVP: Steps 1–3 and auto-schedule generation
- GA: Minor UX refinements based on feedback

---

## 13. Traceability

- F-008 → FR-F-008-1 FR-F-008-2 FR-F-008-3 → tests `tests/test_wizard.py` → `homes/views.py`, `templates/homes/survey_step*.html`

---

## 14. Open questions

- Should we add a summary review page before final submission?

---

## 15. References

- ADR: `docs/adr/adr-2025-11-26-home-onboarding-wizard.md`
- README & QUICKSTART sections on wizard
