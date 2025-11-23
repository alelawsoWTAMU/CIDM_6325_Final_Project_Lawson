# BRIEF: Build Personalized Maintenance Schedule Generation

## Goal

- Implement personalized maintenance schedule generation addressing PRD §4 F-001 and FR-F-001-1 through FR-F-001-3.

## Scope (single PR)

- **Files to touch**:
  - `maintenance/models.py`: MaintenanceTask and Schedule models with applicability rules
  - `maintenance/views.py`: GenerateScheduleView (CBV with POST handling)
  - `maintenance/forms.py`: Schedule generation form (if needed)
  - `templates/maintenance/generate_schedule.html`: Form and schedule display
  - `homes/models.py`: Home model with feature flags (has_basement, has_attic, etc.)

- **Non-goals**: 
  - Email notifications for scheduled tasks (deferred to v1.1)
  - Calendar view integration (deferred to v1.1)
  - Task rescheduling or deletion (MVP only generates initial schedule)

## Standards

- **Commits**: Conventional style (feat/fix/docs/refactor/chore)
  - Example: `feat(maintenance): add personalized schedule generation view`
  - Example: `feat(maintenance): implement task applicability filtering logic`
- **No secrets**: All configuration via `settings.py` or environment variables
- **Django tests**: Use unittest/Django TestCase (no pytest)
  - Test applicability filtering logic
  - Test schedule generation with various home profiles
  - Test prevention of duplicate schedule generation

## Acceptance

- **User flow**: 
  1. User navigates to "My Homes" and selects a home
  2. User clicks "Generate Schedule" button
  3. System filters MaintenanceTasks based on home characteristics (age, features)
  4. System creates Schedule instances for applicable tasks with calculated next_scheduled_date
  5. User sees generated schedule with tasks organized by frequency
  6. Schedule displays task title, category, frequency, and next scheduled date

- **Include migration?**: Yes
  - Migration for Schedule model fields
  - Migration for MaintenanceTask applicability rule fields (min_home_age, required_features JSONField)

- **Update docs & PR checklist**:
  - Update README.md with schedule generation feature description
  - Add to PROJECT_SUMMARY.md completion checklist
  - Document applicability rule format in code comments

## Prompts for Copilot

- "Generate a Django view for personalized maintenance schedule generation. The view should accept a home ID, filter MaintenanceTask objects based on applicability rules (home age, features), create Schedule instances for each applicable task, and redirect to the schedule list view."

- "Explain the schedule generation logic: How does the system determine which tasks apply to a specific home? How are next_scheduled_dates calculated based on task frequency?"

- "Refactor the schedule generation logic into a reusable service method in maintenance/services.py while preserving behavior. Show diff-ready patch."

---

**Related ADR**: None (functionality driven directly by PRD)  
**PRD Reference**: §4 F-001, §5 FR-F-001-1 through FR-F-001-3
