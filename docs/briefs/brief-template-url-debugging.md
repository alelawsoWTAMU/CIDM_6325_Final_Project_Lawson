# BRIEF: Template and URL Routing Debugging Session

## Goal

- Systematically debug and fix template/view/URL mismatches preventing pages from displaying correctly
- Establish consistent naming patterns for ListView context variables
- Document pattern for future template generation

## Problem Statement

During deployment testing, multiple pages failed to display data despite database containing records:
1. Home list showed empty despite 5 homes in database
2. Task list showed empty despite 12 tasks in database
3. Tips list showed empty despite 5 approved tips in database
4. Task detail and tip detail threw NoReverseMatch errors with slug vs pk mismatch

**Root Causes Identified**:
- Views used `context_object_name = 'homes'`, `'tasks'`, `'tips'`
- Templates expected `home_list`, `task_list`, `tip_list` (Django default pattern)
- URL patterns used `<slug:slug>` parameter but templates passed `pk=object.pk`

## Scope (single debugging session)

- **Files touched**:
  - `homes/views.py`: Fixed HomeListView context_object_name
  - `maintenance/views.py`: Fixed TaskListView context_object_name
  - `tips/views.py`: Fixed TipListView context_object_name
  - `templates/maintenance/task_list.html`: Fixed URL tag to use slug
  - `templates/maintenance/schedule_detail.html`: Fixed URL tag to use slug
  - `templates/tips/tip_list.html`: Fixed URL tag to use slug

- **Non-goals**: 
  - Changing URL patterns to use pk instead of slug (kept slug for SEO benefits)
  - Modifying other views beyond ListView fixes
  - Database schema changes

## Standards

- **Commits**: Document each fix with conventional style
  - Example: `fix(homes): correct HomeListView context_object_name to match template`
  - Example: `fix(maintenance): use slug parameter in task_detail URL tags`
  - Example: `fix(tips): align TipListView context name with Django conventions`

- **Pattern Established**: 
  - All ListView subclasses should use `context_object_name = '{model}_list'` pattern
  - All detail view URL tags should check urls.py parameter name (slug vs pk) and match exactly
  - Templates should follow Django conventions: `model_list`, `model_detail`, `model_form`

## Debugging Process

### Issue 1: Home List Empty
**User Report**: "I've added 4 homes and none of them are showing"

**Investigation**:
1. Database query confirmed 5 homes exist for user
2. Template check found `{% if home_list %}`
3. View check found `context_object_name = 'homes'` ❌ MISMATCH

**Fix**:
```python
# homes/views.py
class HomeListView(LoginRequiredMixin, ListView):
    model = Home
    template_name = 'homes/home_list.html'
    context_object_name = 'home_list'  # Changed from 'homes'
```

**Validation**: User confirmed homes now display correctly

---

### Issue 2: Task List Empty
**User Report**: "Implement Tasks functionality" (page loaded but empty)

**Investigation**:
1. Database query confirmed 12 active tasks exist
2. Template check found `{% if task_list %}`
3. View check found `context_object_name = 'tasks'` ❌ MISMATCH

**Fix**:
```python
# maintenance/views.py
class TaskListView(ListView):
    model = MaintenanceTask
    template_name = 'maintenance/task_list.html'
    context_object_name = 'task_list'  # Changed from 'tasks'
    
    def get_queryset(self):
        return MaintenanceTask.objects.filter(is_active=True)
```

**Validation**: User confirmed all 12 tasks now display

---

### Issue 3: Task Detail NoReverseMatch Error
**Error**: `NoReverseMatch: Reverse for 'task_detail' with keyword arguments '{'pk': 9}' not found. 1 pattern(s) tried: ['maintenance/tasks/(?P<slug>[-a-zA-Z0-9_]+)/\\Z']`

**Investigation**:
1. Checked maintenance/urls.py: `path('tasks/<slug:slug>/', views.TaskDetailView.as_view(), name='task_detail')`
2. Checked task_list.html: `{% url 'maintenance:task_detail' pk=task.pk %}` ❌ MISMATCH
3. Verified MaintenanceTask model has slug field ✓

**Fix in 2 Templates**:
```html
<!-- templates/maintenance/task_list.html -->
<a href="{% url 'maintenance:task_detail' slug=task.slug %}">  <!-- Changed from pk=task.pk -->

<!-- templates/maintenance/schedule_detail.html -->
<a href="{% url 'maintenance:task_detail' slug=task.slug %}">  <!-- Changed from pk=task.pk -->
```

**Validation**: User confirmed task detail links work correctly

---

### Issue 4: Tips List Empty
**User Report**: "I can't see these tips" (after seeding 5 approved tips)

**Investigation**:
1. Database query confirmed 5 tips with status='approved'
2. Template check found `{% if tip_list %}`
3. View check found `context_object_name = 'tips'` ❌ MISMATCH

**Fix**:
```python
# tips/views.py
class TipListView(ListView):
    model = LocalTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tip_list'  # Changed from 'tips'
    paginate_by = 20
    
    def get_queryset(self):
        return LocalTip.objects.filter(status='approved').annotate(
            upvote_count=Count('upvotes')
        )
```

**Validation**: User confirmed 5 tips now display correctly

---

### Issue 5: Tip Detail NoReverseMatch Error
**Error**: Same pattern as Issue 3 - template used pk but URL expected slug

**Fix**:
```html
<!-- templates/tips/tip_list.html -->
<a href="{% url 'tips:tip_detail' slug=tip.slug %}">  <!-- Changed from pk=tip.pk -->
```

**Validation**: User confirmed tip detail links work correctly

---

## Pattern Established

### ListView Context Names
**Rule**: Always use `{model_name}_list` for consistency with Django conventions

**Examples**:
- `Home` model → `context_object_name = 'home_list'`
- `MaintenanceTask` model → `context_object_name = 'task_list'`
- `Schedule` model → `context_object_name = 'schedule_list'`
- `LocalTip` model → `context_object_name = 'tip_list'`

### URL Routing Parameter Consistency
**Rule**: Template URL tags must match urls.py parameter names exactly

**Check Process**:
1. Look at urls.py pattern: `path('tasks/<slug:slug>/', ...)`
2. Extract parameter name: `slug`
3. Use in template: `{% url 'app:view' slug=object.slug %}`

**Common Patterns**:
- Slug-based (SEO-friendly): `path('items/<slug:slug>/', ...)` → `{% url 'app:item_detail' slug=item.slug %}`
- PK-based (simple): `path('items/<int:pk>/', ...)` → `{% url 'app:item_detail' pk=item.pk %}`

### Why Slug vs PK?
**This Project Uses Slugs** for:
- MaintenanceTask: SEO-friendly URLs like `/maintenance/tasks/clean-dryer-vent/`
- LocalTip: SEO-friendly URLs like `/tips/prevent-frozen-pipes/`

**Models Need**:
- `slug = models.SlugField(unique=True)` field
- Auto-population in save() method or admin

**Alternative** (simpler but less SEO):
- Use `<int:pk>` in urls.py
- Use `pk=object.pk` in templates
- No slug field required

## Acceptance

- [x] HomeListView displays all user's homes
- [x] TaskListView displays all 12 active maintenance tasks
- [x] TipListView displays all 5 approved community tips
- [x] Task detail links work (no NoReverseMatch error)
- [x] Tip detail links work (no NoReverseMatch error)
- [x] Schedule detail page task links work (no NoReverseMatch error)
- [x] Server restarts automatically pick up template changes
- [x] Pattern documented for future template generation

## Lessons Learned

### Root Cause Analysis
**Why did this happen?**
1. AI generated templates using Django default pattern (`model_list`)
2. AI generated views using shortened names (`homes`, `tasks`, `tips`)
3. No systematic check for consistency across files
4. URL patterns used slug but templates copy-pasted from examples using pk

### Prevention Strategy
**For Future Development**:
1. When generating ListView, always use `{model}_list` pattern
2. When generating templates, check view's context_object_name
3. When using {% url %} tag, check urls.py parameter name first
4. Run template rendering test immediately after generation
5. Use grep/search to find all URL tags when changing URL patterns

### AI Behavior Observation
- AI correctly diagnosed each issue when given error message
- AI correctly identified root cause (context name mismatch, URL parameter mismatch)
- AI required user testing to discover issues (no static analysis)
- AI fixed issues systematically once pattern was identified

### Time Saved
- **Without AI**: Developer would need to:
  1. Read Django docs on ListView context names
  2. Manually check each view file
  3. Manually check each template file
  4. Manually check each urls.py file
  5. Test each fix individually
  - Estimated time: 2-3 hours

- **With AI**: 
  1. User reported issue
  2. AI diagnosed and fixed within minutes
  3. User validated fix
  - Actual time: 15-20 minutes per issue
  - Total session: ~1.5 hours for 5 issues

### Quality Impact
- **Positive**: All issues fixed correctly, no regressions introduced
- **Learning**: Developer now understands Django ListView conventions
- **Documentation**: Pattern established for future consistency

---

## Related Documentation

- ADR-1.0.0: Application Architecture (template organization)
- AI_USAGE_DISCLOSURE.md: Section 3.5-3.9 (detailed debugging log)
- Django ListView docs: https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/#listview

---

## Status: Complete

All 5 issues resolved, patterns established, documentation updated.
