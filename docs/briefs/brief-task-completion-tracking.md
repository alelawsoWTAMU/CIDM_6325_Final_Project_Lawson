# BRIEF: Build Task Completion Tracking

## Goal

- Implement task completion tracking and maintenance history addressing PRD §4 F-006 and FR-F-006-1 through FR-F-006-2.

## Scope (single PR)

- **Files to touch**:
  - `maintenance/models.py`: TaskCompletion model with completion metadata
  - `maintenance/views.py`: MarkCompleteView (CBV), CompletionHistoryView (ListView)
  - `maintenance/forms.py`: TaskCompletionForm with optional fields
  - `templates/maintenance/`: Mark complete form, completion history list
  - Schedule model: Add `is_completed` boolean flag and update logic

- **Non-goals**: 
  - Photo uploads for completion documentation (deferred to v1.2)
  - Completion notifications to other household members (deferred to v2.0)
  - Cost tracking with budget alerts (deferred to v1.2)
  - Analytics dashboard for completion trends (deferred to v1.1)

## Standards

- **Commits**: Conventional style (feat/fix/docs/refactor/chore)
  - Example: `feat(maintenance): add TaskCompletion model with metadata`
  - Example: `feat(maintenance): implement mark complete view and form`
  - Example: `feat(maintenance): add completion history list view`
- **No secrets**: All configuration via `settings.py` or environment variables
- **Django tests**: Use unittest/Django TestCase (no pytest)
  - Test task completion creates TaskCompletion record
  - Test schedule is_completed flag updates correctly
  - Test duplicate completions are prevented
  - Test completion history displays for correct user/home
  - Test satisfaction rating validation (1-5 range)

## Acceptance

- **User flow for marking task complete**:
  1. Authenticated user navigates to "My Schedule"
  2. User sees list of scheduled tasks (incomplete only)
  3. User clicks "Mark Complete" button on a task
  4. System displays completion form with optional fields: notes, cost, time spent, satisfaction rating (1-5 stars)
  5. User fills form (all fields optional except completed date, which defaults to today)
  6. User submits form
  7. System creates TaskCompletion record linked to schedule and user
  8. System updates schedule.is_completed = True
  9. User redirects to schedule list with success message
  10. Completed task no longer appears in incomplete list

- **User flow for viewing completion history**:
  1. User navigates to "Maintenance History" from navigation menu
  2. System displays list of all completed tasks with completion date, task title, notes preview, cost, time spent
  3. User can filter by date range, task category, or home (if multiple homes)
  4. User can click on completion to view full details including all notes and satisfaction rating

- **Include migration?**: Yes
  - Migration for TaskCompletion model
  - Migration to add is_completed field to Schedule model

- **Update docs & PR checklist**:
  - Update README.md with task completion feature description
  - Add to PROJECT_SUMMARY.md completion checklist
  - Document metadata field purposes (cost for budgeting, time for planning, satisfaction for quality tracking)

## Prompts for Copilot

- "Generate Django model for TaskCompletion with fields: schedule (FK), completed_date (auto_now_add), completed_by (FK to User), notes (TextField, optional), cost (DecimalField, optional), time_spent (DurationField, optional), satisfaction_rating (IntegerField 1-5, optional). Include validation for satisfaction_rating range."

- "Generate Django view for marking a scheduled task as complete. Use UpdateView pattern with TaskCompletionForm. After successful completion, update the related Schedule instance to set is_completed=True. Redirect to schedule list with success message."

- "Create Django ListView for maintenance completion history. Filter TaskCompletion objects by current user's homes. Display as table with columns: completion date, task title, home, cost, time spent, satisfaction rating. Add date range filter functionality."

- "Explain the completion tracking workflow: How does marking a task complete affect the schedule? Why store completion metadata separately from Schedule model? How does this support future analytics features?"

- "Refactor the mark complete logic into a method on Schedule model (e.g., mark_complete(user, notes, cost, time_spent, satisfaction_rating)) that creates TaskCompletion and updates is_completed flag. Show diff-ready patch."

---

**Related ADR**: None (functionality driven directly by PRD)  
**PRD Reference**: §4 F-006; §5 FR-F-006-1 through FR-F-006-2
