# BRIEF: Build Intelligent PM Schedule Generation slice

Goal

- Implement Intelligent, seasonal and climate-aware schedule generation addressing PRD §F-009.

Scope (single PR)

- Files to touch: `maintenance/models.py`, `maintenance/utils.py`, `maintenance/views.py`, `templates/maintenance/generate_schedule.html`, `templates/maintenance/calendar_view.html`, `templates/maintenance/schedule_detail.html`, `accounts/models.py`, `maintenance/migrations/0003_*.py`, `maintenance/migrations/0007_*.py`, `accounts/migrations/0003_*.py`, `maintenance/management/commands/seed_task_instructions.py`.
- Non-goals: Notifications system; full settings UI for user preferences; API endpoints; drag-and-drop calendar functionality (removed for simplicity).

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance

- User flow: From a home, user visits Generate Schedule, sees priority-grouped task recommendations (High/Medium/Low), current season and climate factor are displayed, can preview annual distribution and optionally auto-generate the full year. All tasks have comprehensive 10-step instructions. Users can view calendar and reschedule using edit button or quick reschedule buttons (+1W, +1M). Users can customize both descriptions and instructions per schedule.
- Include migration? yes (seasonal_priority on `MaintenanceTask`; schedule_preferences on `User`; custom_description on `ScheduleTaskCustomization`).
- Update docs & PR checklist. ✓ COMPLETED

Prompts for Copilot

- "Create `ScheduleOptimizer` with climate multipliers, seasonal mapping, priority scoring, and annual generation methods." ✓
- "Refactor `GenerateScheduleView` to use optimizer and render priority tiers in the template." ✓
- "Add seasonal_priority to `MaintenanceTask` and schedule_preferences (JSONField) to `User`." ✓
- "Create management command to seed comprehensive 10-step instructions for all 62 maintenance tasks." ✓
- "Add custom_description field to ScheduleTaskCustomization model for user customization." ✓
- "Update schedule_detail.html to support editing both descriptions and instructions." ✓
- "Simplify calendar_view.html by removing drag-and-drop, add edit button for manual date changes." ✓
- "Explain changes and propose commit messages." ✓
- "Refactor into CBV while preserving behavior; show diff-ready patch." ✓