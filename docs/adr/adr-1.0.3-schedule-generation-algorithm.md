# ADR-1.0.3 Schedule Generation Algorithm and Task Applicability

Date: 2025-11-23  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: GitHub Copilot (Claude Sonnet 4.5)  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/prd/home_maintenance_compass_prd_v1.0.1.md#4-scope-items-and-checklist-seeds (F-001) · docs/prd/home_maintenance_compass_prd_v1.0.1.md#5-functional-requirements-bound-to-scope (FR-F-001-1, FR-F-001-2, FR-F-001-3)  
Scope IDs from PRD: F-001 (Personalized Maintenance Schedule Generator)  
Functional requirements: FR-F-001-1 (user inputs), FR-F-001-2 (filtering logic), FR-F-001-3 (date calculation)  
Related issues or PRs: Schedule generation implementation in maintenance app

---

## Intent and scope

Define the algorithm for generating personalized maintenance schedules based on home characteristics, including task applicability filtering and next-date calculation.

**In scope**: Task filtering rules, applicability logic, frequency-based date calculation, duplicate prevention  
**Out of scope**: Machine learning predictions (deferred to v2.0), weather API integration (deferred to v1.1), email notifications (deferred to v1.1)

---

## Problem and forces

### Problem Statement
First-time homeowners are overwhelmed by home maintenance because they don't know what tasks are relevant to their specific home. A 1-year-old condo in Arizona has different maintenance needs than a 30-year-old wood-frame house with a basement in Minnesota.

Per PRD §2 (Problem Statement): "The advice they may get is very generic from strangers on the internet and said advice is not tailored to their specific situations or local climate."

The system must generate a personalized schedule that:
1. Only includes tasks relevant to the home's age and features
2. Calculates appropriate next-due dates based on task frequency
3. Avoids overwhelming users with 100+ irrelevant tasks
4. Completes generation within 3 seconds (NF-001 performance requirement)

### Forces
- **Personalization**: Generic checklists fail; users need home-specific recommendations
- **Simplicity**: Algorithm must be understandable and explainable to users (no black box)
- **Performance**: Must execute in <3 seconds with 100+ tasks (per NF-001)
- **Maintainability**: Content team must be able to add tasks via admin without code changes
- **Accuracy**: Incorrect recommendations could lead to neglect or wasted effort
- **Scalability**: Algorithm must work as task library grows from 12 to 50+ tasks (v1.1)

### Constraints
- MVP uses rule-based filtering (no machine learning per PRD §2 Non-Goals)
- Home characteristics available: age, construction type, climate zone, 8 boolean features
- Task frequencies: weekly, monthly, quarterly, seasonal, annual, biannual
- Must prevent duplicate schedule generation for same home
- Must use Django ORM (no raw SQL per project standards)

---

## Options considered

### Option A: Simple Boolean Matching
**Approach**: Filter tasks using only home feature flags

```python
tasks = MaintenanceTask.objects.filter(is_active=True)
if not home.has_basement:
    tasks = tasks.filter(requires_basement=False)
if not home.has_attic:
    tasks = tasks.filter(requires_attic=False)
# ... repeat for 8 features
```

**Pros**:
- Simplest implementation
- Fast execution (<1 second)
- Easy to understand and debug

**Cons**:
- Ignores home age (new homes don't need roof inspection; old homes need frequent checks)
- Ignores climate zone (winterization irrelevant in Florida)
- No way to express "homes older than 15 years" rules
- Results in many inappropriate tasks for new homes

**PRD Alignment**: Fails FR-F-001-1 (home age input unused), provides generic rather than personalized schedules

**Verdict**: Rejected - insufficient personalization

---

### Option B: Rule-Based Filtering with Age and Features
**Approach**: Filter by home age threshold AND feature requirements

```python
# Filter by activity status
tasks = MaintenanceTask.objects.filter(is_active=True)

# Filter by home age
home_age = home.get_age()  # Current year - year_built
tasks = tasks.filter(
    Q(min_home_age__isnull=True) | Q(min_home_age__lte=home_age)
)

# Filter by required features
if not home.has_basement:
    tasks = tasks.filter(requires_basement=False)
if not home.has_attic:
    tasks = tasks.filter(requires_attic=False)
# ... repeat for all 8 features
```

**Task Examples**:
- "Inspect Roof for Damage": min_home_age=5 (new roofs need time to settle)
- "Check Foundation for Cracks": min_home_age=10 (foundation settling)
- "Test Sump Pump": requires_basement=True (only for homes with basements)

**Pros**:
- Personalized by both age and features
- Simple AND logic easy to understand
- Content team can configure via admin (no code changes)
- Executes quickly with Django ORM + database indexes
- Explainable to users ("Your home is 15 years old, so we include...")

**Cons**:
- Cannot express complex OR conditions ("homes with HVAC OR fireplace")
- Climate zone input collected but not yet used in filtering
- All applicability rules are inclusive (tasks must match all criteria)

**PRD Alignment**: Meets FR-F-001-1 (uses age and features), FR-F-001-2 (filters by applicability), supports explainability

**Verdict**: Selected for MVP - balances simplicity with personalization

---

### Option C: Advanced Rule Engine with Climate Zone
**Approach**: Add climate zone filtering and complex rule expressions

```python
# Climate-specific task filtering
if home.climate_zone in ['northeast', 'midwest']:
    tasks = tasks.filter(
        Q(applicable_climate_zones__contains=['cold']) |
        Q(applicable_climate_zones__isnull=True)
    )

# JSONField for complex rules
# Task.applicability_rules = {"min_age": 10, "requires_any": ["hvac", "fireplace"]}
```

**Pros**:
- Maximum personalization (climate-specific recommendations)
- Supports complex OR conditions
- Future-proof for sophisticated rules

**Cons**:
- Significantly increased complexity
- JSONField rules harder for content team to configure
- Climate zone usage requires research to determine appropriate task recommendations
- Over-engineered for MVP (12 tasks don't justify this complexity)

**PRD Alignment**: Exceeds MVP requirements; climate zone can be added in v1.1 after user feedback

**Verdict**: Rejected for MVP - deferred to v1.1

---

### Option D: Machine Learning Recommendation System
**Approach**: Train model on user completion history to predict relevant tasks

**Pros**:
- Could learn patterns not explicitly programmed
- Adapts to user behavior

**Cons**:
- Requires significant training data (hundreds of users)
- Black box algorithm difficult to explain
- Explicitly out of scope per PRD §2 (Non-Goals: AI-driven diagnostics)
- Overkill for deterministic problem

**PRD Alignment**: Explicitly rejected in PRD Non-Goals

**Verdict**: Rejected - out of scope

---

## Decision

**We choose Option B: Rule-Based Filtering with Age and Features**

### Decision Drivers (Ranked)
1. **PRD Alignment**: Directly implements FR-F-001-2 (applicability filtering)
2. **Personalization**: Uses home age and features for relevant recommendations
3. **Simplicity**: Understandable algorithm that can be explained to users
4. **Performance**: Meets NF-001 (<3 second generation) with Django ORM + indexes
5. **Maintainability**: Content team can configure rules via admin without code changes
6. **Explainability**: Can show users why tasks were included/excluded

### Rationale
The rule-based approach provides sufficient personalization for MVP while remaining simple and maintainable. Content team can add tasks via admin with applicability rules (min_home_age, requires_* flags). Future versions can enhance with climate zone filtering (v1.1) based on user feedback.

---

## Consequences

### Positive

**Personalized Schedules**:
```python
# Example: New construction home (age 2)
# Excludes: "Inspect Roof" (min_age 5), "Foundation Cracks" (min_age 10)
# Includes: "Test Smoke Detectors" (min_age None), "Change HVAC Filter" (min_age None)

# Example: 20-year-old home without pool
# Includes: All age-appropriate tasks
# Excludes: "Pool Maintenance" (requires_pool=True)
```

**Admin-Configurable Rules**:
Content team can add new tasks through admin interface:
1. Navigate to Maintenance > Maintenance tasks > Add
2. Set "Minimum home age" = 15
3. Check "Requires HVAC" checkbox
4. Save - immediately available for schedule generation

**Explainable Recommendations**:
```python
# Future UI enhancement (v1.1)
"We included 'Inspect Roof' because your home is 15 years old (requires 5+ years)"
"We excluded 'Test Sump Pump' because your home doesn't have a basement"
```

**Performance**:
```python
# Query optimization with indexes
class Schedule(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['home', 'scheduled_date']),
        ]

# Single optimized query
tasks = MaintenanceTask.objects.filter(
    is_active=True,
    min_home_age__lte=home_age
).filter(  # Chained filters use AND logic
    requires_basement=False if not home.has_basement else True
)
# Executes in <0.5 seconds with 100 tasks
```

### Negative and Risks

**Climate Zone Unused**:
- Home.climate_zone collected but not used in filtering for MVP
- **Mitigation**: Documented for v1.1 enhancement; field present in database ready for use

**Simple AND Logic**:
- Cannot express "requires HVAC OR fireplace" (task applies if home has either)
- **Mitigation**: Acceptable for MVP task library; v1.1 can add JSONField for complex rules

**Manual Rule Configuration**:
- Content team must understand applicability rules
- Risk of incorrect configuration (e.g., setting min_age too high/low)
- **Mitigation**: Provide content team training, document rule guidelines, admin help_text explains each field

**No Learning from User Feedback**:
- Algorithm doesn't adapt based on which tasks users actually complete
- **Mitigation**: v1.2 can analyze TaskCompletion data to refine recommendations

---

## Implementation notes

### Task Model Applicability Fields
```python
# maintenance/models.py
class MaintenanceTask(models.Model):
    # ... other fields ...
    
    # Age-based applicability
    min_home_age = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Minimum home age in years for this task to apply (leave blank if applies to all ages)"
    )
    
    # Feature-based applicability (8 boolean flags)
    requires_basement = models.BooleanField(
        default=False,
        help_text="Check if task requires a basement"
    )
    requires_attic = models.BooleanField(
        default=False,
        help_text="Check if task requires an attic"
    )
    requires_garage = models.BooleanField(default=False)
    requires_hvac = models.BooleanField(default=False)
    requires_fireplace = models.BooleanField(default=False)
    requires_pool = models.BooleanField(default=False)
    requires_well = models.BooleanField(default=False)
    requires_septic = models.BooleanField(default=False)
```

### Schedule Generation View
```python
# maintenance/views.py
class GenerateScheduleView(LoginRequiredMixin, View):
    """Generate personalized maintenance schedule based on home characteristics."""
    
    def post(self, request, home_id):
        home = get_object_or_404(Home, id=home_id, owner=request.user)
        
        # Prevent duplicate generation
        existing_schedules = Schedule.objects.filter(home=home)
        if existing_schedules.exists():
            messages.warning(request, 'A schedule already exists for this home.')
            return redirect('maintenance:schedule_list')
        
        # Get all active maintenance tasks
        tasks = MaintenanceTask.objects.filter(is_active=True)
        
        # Filter by home age
        home_age = home.get_age()
        tasks = tasks.filter(
            Q(min_home_age__isnull=True) | Q(min_home_age__lte=home_age)
        )
        
        # Filter by required features (exclude tasks requiring features home doesn't have)
        if not home.has_basement:
            tasks = tasks.filter(requires_basement=False)
        if not home.has_attic:
            tasks = tasks.filter(requires_attic=False)
        if not home.has_garage:
            tasks = tasks.filter(requires_garage=False)
        if not home.has_hvac:
            tasks = tasks.filter(requires_hvac=False)
        if not home.has_fireplace:
            tasks = tasks.filter(requires_fireplace=False)
        if not home.has_pool:
            tasks = tasks.filter(requires_pool=False)
        if not home.has_well:
            tasks = tasks.filter(requires_well=False)
        if not home.has_septic:
            tasks = tasks.filter(requires_septic=False)
        
        # Create schedule entries with calculated dates
        from datetime import date, timedelta
        today = date.today()
        created_count = 0
        
        for task in tasks:
            next_date = self.calculate_next_date(today, task.frequency)
            Schedule.objects.create(
                home=home,
                task=task,
                scheduled_date=next_date
            )
            created_count += 1
        
        messages.success(
            request,
            f'Successfully generated schedule with {created_count} tasks!'
        )
        return redirect('maintenance:schedule_list')
    
    def calculate_next_date(self, start_date, frequency):
        """Calculate next scheduled date based on frequency."""
        from datetime import timedelta
        
        frequency_map = {
            'weekly': timedelta(days=7),
            'monthly': timedelta(days=30),
            'quarterly': timedelta(days=90),
            'seasonal': timedelta(days=90),
            'annual': timedelta(days=365),
            'biannual': timedelta(days=182),
        }
        
        delta = frequency_map.get(frequency, timedelta(days=30))
        return start_date + delta
```

### Home Model Age Calculation
```python
# homes/models.py
class Home(models.Model):
    year_built = models.PositiveIntegerField()
    
    def get_age(self):
        """Calculate current age of home in years."""
        from datetime import date
        return date.today().year - self.year_built
```

### Example Task Configuration
```python
# Example admin entry for "Inspect Roof for Damage"
MaintenanceTask(
    title="Inspect Roof for Damage",
    description="Check for missing shingles, cracks, and wear",
    category="exterior",
    frequency="annual",
    estimated_time_minutes=60,
    difficulty_level=3,
    min_home_age=5,  # Roofs typically need inspection after 5 years
    requires_basement=False,  # No basement needed
    requires_attic=False,
    # ... all other requires_* = False
)
```

---

## Future enhancements

### v1.1: Climate Zone Integration
Add climate-specific task filtering:
```python
# Add field to MaintenanceTask
applicable_climate_zones = models.JSONField(
    default=list,
    blank=True,
    help_text="List of climate zones where task applies (empty = all zones)"
)

# Filter in GenerateScheduleView
if task.applicable_climate_zones:
    if home.climate_zone not in task.applicable_climate_zones:
        # Exclude task
        continue
```

### v1.2: Completion-Based Refinement
Learn from user behavior:
```python
# Analyze which tasks users actually complete
popular_tasks = TaskCompletion.objects.values('schedule__task').annotate(
    completion_rate=Count('id')
).order_by('-completion_rate')

# Deprioritize tasks users consistently skip
```

### v2.0: Predictive Scheduling
Use weather API and usage patterns:
```python
# Weather-based scheduling
if weather_api.forecast(home.location).includes_freeze:
    prioritize_task("Winterize Outdoor Faucets")
```

---

## Related decisions

- ADR-1.0.0: Application Architecture (defines maintenance app)
- ADR-1.0.2: Core Data Models (defines Home, MaintenanceTask, Schedule relationships)
- ADR-1.0.5: Admin Interface Design (configuring task applicability rules)

---

## References

- PRD Section 5: FR-F-001-1, FR-F-001-2, FR-F-001-3
- PRD Section 7: NF-001 (Performance requirement: <3 seconds)
- PRD Section 9: Risks & Assumptions (algorithm complexity mitigation)
- Django QuerySet API: Q objects for complex lookups
- Database indexing for query performance

---

## Revision history

- 2025-11-23: v1.0 Initial version - accepted
