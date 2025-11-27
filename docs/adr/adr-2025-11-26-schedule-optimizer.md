# ADR-2025-11-26 Schedule Optimizer for Intelligent PM Scheduling

Date: 2025-11-26  
Status: Accepted and Implemented  
Version: 1.1 (Updated with instruction seeding and calendar simplification)  
Authors: Alexander J Lawson  
Reviewers: Project Instructor

---

## Links and traceability

PRD link: docs/prd/Module 2 - PRD.md (F-009)  
Scope IDs from PRD: F-009, NF-001, DOC-002  
Functional requirements: FR-F-009-1 (seasonal awareness), FR-F-009-2 (climate multipliers), FR-F-009-3 (priority scoring), FR-F-009-4 (annual generation)  
Related issues or PRs: #schedule-optimizer, #generate-schedule-ui

---

## Intent and scope

Introduce a `ScheduleOptimizer` utility to generate intelligent maintenance schedules using seasonal priorities, climate-zone multipliers, and maintenance history based priority scoring. Provide comprehensive default instructions for all tasks with user customization capability. Simplify calendar interface by removing drag-and-drop complexity. In scope: `MaintenanceTask` seasonal field, `User` schedule preferences (JSON), optimized view/template, instruction seeding system, `ScheduleTaskCustomization` for user overrides, simplified calendar UI. Out of scope: notification delivery, ML predictions, external APIs, drag-and-drop calendar rescheduling.

---

## Problem and forces

- Static schedules lack context about season and climate, reducing relevance.  
- Tradeoffs: algorithm complexity vs. UX clarity; performance; data availability.  
- Constraints: Django ORM, current data model, Windows dev + Render prod.

---

## Options considered

- **A)** Utility class (`ScheduleOptimizer`) (chosen)  
  - Pros: Isolated logic, testable, reusable  
  - Cons: Requires view/template integration
- **B)** Inline logic in view  
  - Pros: Simpler setup  
  - Cons: Harder to test and maintain
- **C)** Third-party scheduling library  
  - Pros: Prebuilt features  
  - Cons: Overkill, dependency weight, limited customization

---

## Decision

We choose A (utility class) to encapsulate scheduling logic, improve testability, and keep views thin.

Decision drivers ranked:  
D1: Maintainability  
D2: Testability  
D3: UX impact

---

## Consequences

Positive  
- Clear separation of concerns  
- Adaptable to new rules (season, climate, history)  
- Enables annual generation and priority tiers

Negative and risks  
- Algorithm tuning required (thresholds)  
- Potential performance costs with large datasets

Mitigations  
- Cache season and climate computations per request  
- Use queryset filtering and indexing; paginate UI

---

## Requirements binding

- FR-F-009-1: Tasks prioritized by current season; 'any' season gets small bonus  
- FR-F-009-2: Climate multipliers (1.0x–1.5x) adjust due dates/frequency  
- FR-F-009-3: Priority scoring builds on history (overdue +50, never-done +15, seasonal +20, extreme climate +10)  
- FR-F-009-4: Annual schedule generation creates 12 months of tasks  
- FR-F-009-5: All 62 tasks have comprehensive 10-step default instructions via seed command
- FR-F-009-6: Users can customize both descriptions and instructions per schedule (ScheduleTaskCustomization model)
- FR-F-009-7: Calendar interface simplified without drag-and-drop; edit button and quick reschedule buttons (+1W, +1M) provided
- DOC-002: README/QUICKSTART/AI_USAGE_DISCLOSURE updated to explain features

---

## Acceptance criteria snapshot

- AC1: `/maintenance/generate/<home_pk>/` displays High/Medium/Low priority sections with scores ✓
- AC2: Annual preview table renders with due dates and badges ✓
- AC3: "Auto-Generate Full Year Schedule" creates schedules and confirms ✓
- AC4: All 62 tasks have comprehensive default instructions (10 steps each) ✓
- AC5: Users can customize descriptions and instructions with visual indicators ✓
- AC6: Calendar view has edit button and quick reschedule (+1W, +1M) without drag-and-drop ✓

Evidence collected  
- ✓ Screenshots of UI showing priority tiers
- ✓ Server logs showing instruction seeding (39 tasks updated in final batch)
- ✓ Migration 0007 applied successfully
- ✓ Calendar view simplified and tested

---

## Implementation outline

Plan  
- Step 1: Add `seasonal_priority` to `MaintenanceTask`; add `schedule_preferences` JSON to `User`  
Artifacts to update  
- Code paths: `maintenance/models.py`, `maintenance/utils.py`, `maintenance/views.py`, `templates/maintenance/generate_schedule.html`, `templates/maintenance/calendar_view.html`, `templates/maintenance/schedule_detail.html`, `maintenance/management/commands/seed_task_instructions.py`  
- Settings and secrets: none  
- Migrations: `maintenance/migrations/0003_*`, `maintenance/migrations/0007_scheduletaskcustomization_custom_description.py`, `accounts/migrations/0003_*`  
- Templates and static assets: updated schedule generation UI, simplified calendar UI, enhanced schedule detail UI with customization controlsgorithm directly in views

Artifacts to update  
- Code paths: `maintenance/models.py`, `maintenance/utils.py`, `maintenance/views.py`, `templates/maintenance/generate_schedule.html`  
- Settings and secrets: none  
- Migrations: `maintenance/migrations/0003_*`, `accounts/migrations/0003_*`  
- Templates and static assets: updated schedule generation UI

---

## Test plan and invariants

Invariants  
- INV-1: Priority scoring deterministic for same inputs  
- INV-2: Annual generation respects season/climate rules

Unit tests  
- tests/test_schedule_optimizer.py: scoring, season detection, climate factor, annual generation distribution

Behavioral tests (optional)  
- End-to-end schedule generation and annual creation

Performance and accessibility checks  
- Verify reasonable query counts; ensure color coding meets contrast standards

---

## Documentation updates

- ✓ README: intelligent scheduling feature details, instruction system, customization capability
- ✓ QUICKSTART: usage of annual preview and one-click generation, task customization workflow
- ✓ AI_USAGE_DISCLOSURE.md: comprehensive section on instruction seeding and customization system (section 10.4)
- ✓ TODO.md: mark feature complete
- ✓ export_data.sh: updated to include ScheduleTaskCustomization fixture
- ✓ PRD and ADR documents: updated with completion status

---

## Rollback and contingency

Rollback trigger  
- Incorrect schedule generation or performance regressions  

Rollback steps  
- git revert of optimizer PR; disable annual generation button

Data and config safety  
- Additive migrations only; no destructive changes

---

## Attestation plan

Human witness  
- Instructor to attest with screenshots and commit refs

Attestation record  
- Commit hash and brief rationale  
- Path: docs/attestations/ADR-2025-11-26-schedule-optimizer.md
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
- [x] **IMPLEMENTATION COMPLETE** (Nov 26, 2025)
- [x] Instruction seeding system deployed (62 tasks with 10-step instructions)
- [x] User customization system operational (descriptions + instructions)
- [x] Calendar UI simplified (drag-and-drop removed, edit button added)
- [x] All migrations applied (0003, 0007)
- [x] Documentation updated comprehensivelyd invariants specified  
- [x] Docs updates and changelog listed  
- [x] Rollback trigger and steps documented  
- [x] Attestation plan recorded

---

## References

- Django docs: QuerySets, CBVs  
- Bootstrap 5 docs: badges and alerts  
- Climate classification references (Köppen) for zone definitions
