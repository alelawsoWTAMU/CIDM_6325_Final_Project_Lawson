# Product Requirements Document

## 1. Document information

- Product or feature name: Intelligent PM Schedule Generation (ScheduleOptimizer)
- Author(s): Alexander J Lawson
- Date created: 2025-11-26
- Last updated: 2025-11-26
- Version: 1.0

---

## 2. Overview

- Summary: Intelligent, adaptive schedule generation using seasonal priorities, climate-zone multipliers, priority scoring, and maintenance history; includes annual bulk generation and an enhanced UI with priority tiers. Comprehensive task instructions seeded for all 62 tasks with user customization capability.
- Problem statement: Static schedules ignore season and climate context, leading to poor timing and reduced user trust. Tasks lack actionable instructions for homeowners.
- Goals and objectives:
  - Prioritize tasks by current season and home climate
  - Score tasks using history (overdue, never-done) and context
  - Provide annual preview and one-click bulk generation
  - Provide comprehensive default instructions for all maintenance tasks
  - Allow users to customize both descriptions and instructions per schedule
- Non-goals:
  - Notifications and reminders; ML predictions; external APIs; drag-and-drop calendar rescheduling

---

## 3. Context and background

- Business context: Improves relevance and adherence, increasing perceived value of the app.
- Market or customer insights: Homeowners prefer actionable, timely guidance; seasonal tasks resonate.
- Competitive or benchmark references: Many maintenance platforms lack climate-season intelligence.

---

## 4. Scope items and checklist seeds

- [x] **F-009 Intelligent Scheduling**  
  User story As a homeowner I want smart scheduling so that tasks are recommended at the right time with clear priorities and actionable instructions.  
  Acceptance notes
  - AC1 Seasonal prioritization based on current season; 'any' season receives a small bonus ✓
  - AC2 Climate-zone multipliers (1.0x–1.5x) adjust due dates/frequency ✓
  - AC3 Priority scoring 0–100+ (overdue +50, seasonal +20, never-done +15, extreme climate +10) ✓
  - AC4 Annual preview and one-click bulk generation for 12 months of tasks ✓
  - AC5 UI shows High/Medium/Low tiers with scores and badges ✓
  - AC6 All 62 tasks have comprehensive 10-step default instructions ✓
  - AC7 Users can customize both descriptions and instructions per schedule ✓
  - AC8 Calendar view simplified without drag-and-drop (edit button + quick reschedule) ✓
**Out of scope**
- Notifications, full preferences UI, drag-and-drop calendar rescheduling (removed for simplicity)ersion 1.0  Status **COMPLETED**

**Out of scope**
- Notifications, full preferences UI

---

## 5. Functional requirements bound to scope

- **FR-F-009-1** Seasonal priority filtering and bonus scoring  
  Rationale Increase time-relevance  
  Trace F-009
- **FR-F-009-2** Climate factor applied to due-date/frequency  
  Rationale Localize schedules  
  Trace F-009
- **FR-F-009-3** Priority scoring considers maintenance history  
  Rationale Nudge overdue/ignored tasks  
  Trace F-009
- **FR-F-009-4** Annual generation with preview  
  Rationale Plan a full year efficiently  
  Trace F-009
- **FR-F-009-5** Comprehensive task instructions with customization  
  Rationale Empower users with actionable guidance  
  Trace F-009
## 6. Checklist to be generated from scope

- [x] F-009 Intelligent Scheduling — AC1–AC8 satisfied — Artifacts linked — Test date: Nov 26, 2025 — Status: **COMPLETE**
  - [x] Seasonal prioritization implemented
  - [x] Climate multipliers active
  - [x] Priority scoring algorithm functional
  - [x] Annual generation working
  - [x] UI with priority tiers rendered
  - [x] 62 tasks seeded with 10-step instructions
  - [x] User customization for descriptions and instructions
  - [x] Calendar simplified (drag-and-drop removed)

---

## 6. Checklist to be generated from scope

- [ ] F-009 Intelligent Scheduling — AC1–AC5 satisfied — Artifacts linked — Test date: ____ — Status: ____

---

## 7. Non functional requirements

- **NF-001 Performance** Page renders < 600ms with 62 tasks on dev
- **NF-002 Accessibility** Color contrast for priority badges meets WCAG AA
- **NF-003 Security** Auth required; CSRF tokens; server-side validation
- **NF-004 Reliability** Annual generation idempotent and safe

---

## 10. Acceptance criteria

- ✓ High/Medium/Low tiers render with correct scores
- ✓ Annual preview shows due dates and badges
- ✓ Bulk generation creates schedules and confirms
- ✓ All 62 tasks have comprehensive default instructions (10 steps each)
- ✓ Users can customize descriptions and instructions with edit/save/reset controls
- ✓ Calendar view simplified with edit button and quick reschedule (+1W, +1M)
- ✓ Migration 0007 applied for custom_description field
---

## 9. Risks and assumptions

- Risks: Algorithm tuning; potential query load
- Assumptions: Sufficient TaskCompletion data for history weighting; climate zone available on Home

---

## 10. Acceptance criteria

- High/Medium/Low tiers render with correct scores
- Annual preview shows due dates and badges
- Bulk generation creates schedules and confirms

---

## 11. Success metrics

- Increased task completion rates in-season
## 13. Traceability

- F-009 → FR-F-009-1 FR-F-009-2 FR-F-009-3 FR-F-009-4 FR-F-009-5 FR-F-009-6 → tests `tests/test_schedule_optimizer.py` → `maintenance/utils.py`, `maintenance/views.py`, `maintenance/models.py`, `templates/maintenance/generate_schedule.html`, `templates/maintenance/calendar_view.html`, `templates/maintenance/schedule_detail.html`, `maintenance/management/commands/seed_task_instructions.py`
---

## 12. Rollout and release plan

- MVP: Seasonal/climate scoring and tiered UI
- GA: Annual generation and preview; minor UX polish

---

## 13. Traceability

- F-009 → FR-F-009-1 FR-F-009-2 FR-F-009-3 FR-F-009-4 → tests `tests/test_schedule_optimizer.py` → `maintenance/utils.py`, `maintenance/views.py`, `templates/maintenance/generate_schedule.html`

---

## 14. Open questions

- Should thresholds for High/Medium/Low be configurable per user?

---

## 15. References

- ADR: `docs/adr/adr-2025-11-26-schedule-optimizer.md`
- README & QUICKSTART sections on intelligent scheduling
