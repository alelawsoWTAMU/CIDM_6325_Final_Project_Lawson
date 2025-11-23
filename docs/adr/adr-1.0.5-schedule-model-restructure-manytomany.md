# ADR-1.0.5 Schedule Model Restructure: ManyToManyField for Tasks

Date: 2025-11-23  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: GitHub Copilot (Claude Sonnet 4.5)  
Supersedes or amends: ADR-1.0.2 (Core Data Models)

---

## Links and traceability

PRD link: docs/prd/Module 2 - PRD.md (F-001, F-002)  
Scope IDs from PRD: F-001, F-002  
Functional requirements: FR-F-001-1, FR-F-001-2, FR-F-002-1  
Related ADRs: ADR-1.0.2 (Core Data Models), ADR-1.0.3 (Schedule Generation Algorithm)  
Migration: maintenance/migrations/0002_alter_schedule_options_and_more.py

---

## Intent and scope

Restructure the Schedule model from single-task-per-schedule (ForeignKey) to multiple-tasks-per-schedule (ManyToManyField) to better match homeowner workflow patterns and reduce database overhead.

**In scope**: Schedule model field changes, migration generation, view updates, form simplification, admin interface updates  
**Out of scope**: Task completion tracking (deferred to future ADR), cost tracking per task (deferred to v1.1)

---

## Problem and forces

### Problem Statement
The original Schedule model used a ForeignKey to MaintenanceTask, meaning one Schedule instance could only contain one task. Real-world homeowner behavior shows that maintenance activities are typically batched on the same day (e.g., "Saturday morning chores list"). The one-schedule-per-task design led to:

1. Database bloat: User creating 5 tasks for same day → 5 Schedule rows
2. User confusion: "My schedule shows 5 entries for Saturday" instead of "1 schedule with 5 tasks"
3. Completion tracking complexity: Marking each task complete required 5 separate database writes
4. Poor UX: Schedule list view cluttered with duplicate dates

### Forces
- **User Mental Model**: Homeowners think "Saturday's to-do list" not "5 separate schedule entries"
- **Database Efficiency**: 1 Schedule with ManyToMany is more normalized than N Schedules with same date
- **Completion Workflow**: Users want to check off individual tasks but view/manage them as a group
- **Migration Complexity**: Existing schedules in database require data migration or deletion
- **View Logic Changes**: GenerateScheduleView, ScheduleListView, ScheduleDetailView all require updates

### Constraints
- Must maintain data integrity during migration
- Must not break existing URLs or views during development
- Must preserve task applicability filtering logic
- Must support individual task completion in future (deferred to v1.1)

---

## Options considered

### Option A: Keep Single-Task Schedule, Add Grouping Layer
**Structure**: Maintain `Schedule.task = ForeignKey`, add `ScheduleGroup` model to group schedules by date

**Pros**:
- No migration required (additive change)
- Existing data preserved
- Individual task tracking already in place

**Cons**:
- Adds complexity with extra model layer
- Requires join queries (Schedule → ScheduleGroup) for every list view
- Doesn't address database bloat
- User still sees multiple schedule instances in UI unless views are heavily modified

**PRD Alignment**: Meets functional requirements but poor UX alignment

**Verdict**: Rejected - adds unnecessary complexity without solving core UX issue

---

### Option B: ManyToManyField for Tasks (SELECTED)
**Structure**: Replace `task = ForeignKey` with `tasks = ManyToManyField`, simplify to `is_completed` boolean

**Model Changes**:
```python
class Schedule(models.Model):
    # BEFORE
    task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[...])  # pending/completed/skipped/overdue
    completed_date = models.DateField(null=True)
    cost = models.DecimalField(...)
    performed_by = models.CharField(...)
    recurs = models.BooleanField(...)
    
    # AFTER
    tasks = models.ManyToManyField(MaintenanceTask, related_name='schedules')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    # Removed: status, completed_date, cost, performed_by, recurs
```

**Migration Strategy**:
- Remove all existing schedules (acceptable for development phase)
- Add new ManyToMany field
- Simplify status tracking to boolean
- Remove cost/performer tracking (defer to v1.1 when per-task completion added)

**View Updates Required**:
```python
# GenerateScheduleView
# BEFORE: Create N schedules for N tasks
for task in applicable_tasks:
    Schedule.objects.create(home=home, task=task, scheduled_date=date)

# AFTER: Create 1 schedule with N tasks
schedule = Schedule.objects.create(home=home, scheduled_date=date)
schedule.tasks.set(selected_tasks)

# ScheduleListView
# BEFORE: queryset = Schedule.objects.filter(home__owner=user)
# AFTER: queryset = Schedule.objects.filter(home__owner=user).prefetch_related('tasks')

# ScheduleDetailView
# BEFORE: context['task'] = schedule.task
# AFTER: context['tasks'] = schedule.tasks.all()
```

**Form Simplification**:
```python
# ScheduleForm
# BEFORE: fields = ['home', 'task', 'scheduled_date', 'status', 'recurs', 'notes']
# AFTER: fields = ['scheduled_date', 'notes']  # Tasks selected in template via checkboxes
```

**Admin Updates**:
```python
class ScheduleAdmin(admin.ModelAdmin):
    filter_horizontal = ['tasks']  # Enable multi-select widget
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Number of Tasks'
    
    list_display = ['home', 'scheduled_date', 'task_count', 'is_completed', 'created_at']
```

**Pros**:
- Matches user mental model ("one schedule per day")
- Reduces database rows (1 schedule vs N schedules)
- Simpler completion workflow (mark entire schedule done)
- Clean migration path (delete-and-rebuild acceptable in dev)
- More normalized database design

**Cons**:
- Requires migration and data loss during development
- Can't track individual task completion until v1.1 enhancement
- Can't track per-task cost/performer until v1.1 enhancement
- Requires updates to 5+ views and templates

**PRD Alignment**: Better matches F-001 (Generate Schedule) and F-002 (Track Completion) user stories

**Verdict**: Selected - optimal balance of UX improvement and implementation simplicity

---

### Option C: Polymorphic Schedule (Single Task OR Multiple Tasks)
**Structure**: Use GenericForeignKey to support both single-task and multi-task schedules

**Pros**:
- Maximum flexibility
- Could support task groups, recurring patterns, etc.

**Cons**:
- Overly complex for current requirements
- Django ContentTypes framework adds query overhead
- Difficult to enforce validation (is it a task or task group?)
- Poor database integrity (can't use ForeignKey constraints)

**Verdict**: Rejected - unnecessary complexity, violates YAGNI principle

---

## Decision

**Selected Option B: ManyToManyField for Tasks**

### Rationale
1. **User-Centric Design**: Homeowners batch tasks by day; the model should reflect this workflow
2. **Database Efficiency**: 1 Schedule with 5 tasks is more normalized than 5 Schedules with duplicate dates
3. **Simplicity**: Removing status/cost/performer fields simplifies v1.0; can be re-added in v1.1 with per-task tracking
4. **Migration Feasibility**: Development phase allows data loss; production would require data migration script

### Implementation Plan
1. ✅ Update Schedule model with new fields
2. ✅ Generate and apply migration 0002
3. ✅ Update GenerateScheduleView to create single schedule with multiple tasks
4. ✅ Update ScheduleForm to remove task/home/recurs fields
5. ✅ Update schedule_detail.html template to loop through `schedule.tasks.all()`
6. ✅ Update ScheduleAdmin with filter_horizontal and task_count method
7. ⏳ Test schedule generation workflow (in progress)
8. ⏳ Test schedule completion workflow (blocked by AttributeError fix)
9. ⏳ Update schedule list view to display task count
10. ⏳ Add bulk task selection UI in generate_schedule template

### Acceptance Criteria
- [x] Migration 0002 applies without errors
- [x] User can generate schedule with multiple tasks selected via checkboxes
- [x] Schedule detail page displays all tasks in the schedule
- [x] Schedule list shows one row per schedule (not per task)
- [x] Admin interface allows selecting multiple tasks via horizontal filter
- [ ] User can mark entire schedule complete
- [ ] Completed schedules move to separate "Completed" tab
- [ ] Individual task completion tracking (deferred to ADR-1.0.6 in v1.1)

---

## Consequences

### Positive
- **Improved UX**: Schedule list matches user mental model (batched by date)
- **Better Performance**: Fewer database rows, fewer queries with prefetch_related
- **Simpler Code**: Removed complex status state machine (pending/completed/skipped/overdue)
- **Future-Proof**: ManyToMany relationship allows adding per-task metadata in v1.1 via through model

### Negative
- **Development Data Loss**: All existing schedules deleted during migration
- **Feature Regression**: Can no longer track cost, performer, or individual task completion (deferred to v1.1)
- **Increased Migration Complexity**: Production deployment will require careful data migration strategy

### Neutral
- **View Logic Changes**: Required updates to 5+ views, but changes are straightforward
- **Template Updates**: Required updates to 3+ templates, but mostly adding `.all()` calls

---

## Lessons learned

### What Went Well
- Early detection of UX mismatch during user testing prevented late-stage rework
- Migration was simple because development phase allowed data deletion
- ManyToMany relationship is more flexible than ForeignKey for future enhancements

### What Could Be Improved
- Should have considered batching pattern during initial model design (ADR-1.0.2)
- Could have prototyped UI mockups to identify workflow pattern earlier
- Documentation of user mental model would have guided initial design

### For Future Consideration
- v1.1: Add `ScheduleTask` through model for per-task completion, cost, performer tracking
- v1.2: Add recurring schedule templates (e.g., "Every Saturday" auto-generates schedules)
- v2.0: Add AI-powered schedule optimization (batch compatible tasks, estimate time/cost)

---

## Related documentation

- ADR-1.0.2: Core Data Models and Relationships (superseded for Schedule model)
- ADR-1.0.3: Schedule Generation Algorithm (updated to create single schedule)
- Brief: Schedule Generation (updated workflow diagrams)
- Migration: `maintenance/migrations/0002_alter_schedule_options_and_more.py`

---

## Approval

**Decision made by**: Alexander J Lawson (Project Lead)  
**Date**: 2025-11-23  
**Approved by**: GitHub Copilot review, user testing validation  
**Implementation status**: Complete (views updated, migration applied, testing in progress)
