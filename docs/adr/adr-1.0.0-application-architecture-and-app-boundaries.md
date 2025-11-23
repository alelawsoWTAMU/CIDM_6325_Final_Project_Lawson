# ADR-1.0.0 Application Architecture and App Boundaries

Date: 2025-11-23  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: GitHub Copilot (Claude Sonnet 4.5)  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/prd/home_maintenance_compass_prd_v1.0.1.md#4-scope-items-and-checklist-seeds (Scope) · docs/prd/home_maintenance_compass_prd_v1.0.1.md#13-traceability (Traceability)  
Scope IDs from PRD: F-001, F-002, F-003, F-004, F-005, F-006  
Functional requirements: FR-F-001-1, FR-F-001-2, FR-F-001-3, FR-F-002-1, FR-F-002-2, FR-F-002-3, FR-F-003-1, FR-F-003-2, FR-F-003-3, FR-F-004-1, FR-F-004-2, FR-F-004-3, FR-F-004-4, FR-F-005-1, FR-F-005-2, FR-F-005-3, FR-F-006-1, FR-F-006-2  
Related issues or PRs: Initial implementation

---

## Intent and scope

Define the Django project module boundaries using multiple domain-focused apps to match business concerns (accounts, homes, maintenance, tips) and keep templates and URLs namespaced.

**In scope**: app layout, import paths, template directories, namespaced URLs, model organization  
**Out of scope**: specific model fields (covered by ADR-1.0.2), authentication implementation details (covered by ADR-1.0.3)

---

## Problem and forces

### Problem Statement
The Home Maintenance Compass application addresses multiple distinct domains: user accounts, home property management, maintenance scheduling, and community knowledge sharing. We need clear separation of concerns for maintainability, testability, and future extensibility.

### Forces
- **Clarity**: First-time homeowners need intuitive navigation matching their mental model (My Homes, My Schedule, Community Tips)
- **Maintainability**: Separate domains allow independent development and testing
- **Reusability**: Moderation workflow (tips) may extend to other user-generated content in future versions
- **Django Best Practices**: Align with Django's philosophy of "apps should do one thing and do it well"
- **Academic Context**: Clear boundaries aid comprehension for educational purposes

### Constraints
- Must use Django framework per course requirements
- Must follow Matt Layman's "Understand Django" patterns
- Must implement baseline, good, better, and best features from rubric
- Must support future scalability to v1.1 and v2.0 per PRD phasing

---

## Options considered

### Option A: Single Monolithic App
**Structure**: One `home_maintenance` app containing all models, views, forms

**Pros**:
- Minimal configuration
- Simple import paths
- Fewer files to navigate initially

**Cons**:
- Low cohesion: authentication, property management, scheduling, and community features all mixed
- Admin interface becomes cluttered with unrelated models
- URL patterns difficult to organize logically
- Testing becomes complex (can't test domains in isolation)
- Violates single responsibility principle

**PRD Alignment**: Strains F-003 and F-004 (community features mixed with personal data), complicates admin organization

**Verdict**: Rejected - insufficient separation of concerns

---

### Option B: Domain-Driven Apps (accounts, homes, maintenance, tips)
**Structure**: Four apps organized by business domain
- `accounts/`: Custom user model, registration, profiles
- `homes/`: Home properties, appliances, service providers
- `maintenance/`: Tasks, schedules, completions
- `tips/`: Community tips, comments, reports, moderation

**Pros**:
- Clear domain boundaries matching user mental model
- Each app has focused responsibility
- URL namespacing provides intuitive routes (`/homes/`, `/maintenance/`, `/tips/`)
- Admin interface organized by domain
- Testing can target specific domains
- Aligns with PRD scope items (F-001 through F-006)
- Future features naturally fit into existing apps

**Cons**:
- More boilerplate (4× models.py, views.py, urls.py, admin.py)
- Requires understanding of app configuration and URL includes
- Potential for circular imports if not carefully managed

**PRD Alignment**: Directly maps to PRD functional requirements:
- F-001, F-002, F-006 → `maintenance/`
- F-003, F-004 → `tips/`
- F-005 → `homes/`
- User authentication → `accounts/`

**Verdict**: Selected - optimal balance of clarity and Django best practices

---

### Option C: Micro-Apps by Feature
**Structure**: Very granular apps (e.g., `task_generation/`, `task_profiles/`, `tip_submission/`, `tip_moderation/`, `home_creation/`, `appliance_tracking/`)

**Pros**:
- Maximum isolation
- Extremely focused responsibilities
- Could support microservices architecture in distant future

**Cons**:
- Significant overhead (10+ apps for MVP)
- Over-engineering for project scope
- Difficult to understand for first-time Django learners
- Excessive boilerplate
- Complicates relationships (e.g., Task and Schedule naturally belong together)

**PRD Alignment**: Overkill for MVP; no PRD requirement demands this level of granularity

**Verdict**: Rejected - unnecessary complexity for project scope and timeline

---

## Decision

**We choose Option B: Domain-Driven Apps (accounts, homes, maintenance, tips)**

### Decision Drivers (Ranked)
1. **Domain Cohesion**: Each app represents a clear business domain matching user mental model
2. **PRD Alignment**: Apps map directly to PRD scope items (F-001 through F-006)
3. **Testability**: Domains can be tested in isolation
4. **Django Best Practices**: Follows "apps should do one thing and do it well" philosophy
5. **Academic Context**: Clear structure aids learning and explanation
6. **Scalability**: Structure supports v1.1 and v2.0 feature additions per PRD roadmap

### Rationale
The four-app structure balances simplicity with proper separation of concerns. Each app has a clear purpose:
- **accounts**: "Who is the user?" (authentication, profiles, homeowner status)
- **homes**: "What property are we maintaining?" (homes, appliances, service providers)
- **maintenance**: "What work needs to be done?" (tasks, schedules, completions)
- **tips**: "What can the community teach us?" (tips, comments, moderation)

This structure directly supports the PRD's phased rollout (§12) and traceability requirements (§13).

---

## Consequences

### Positive

**Improved Maintainability**:
- Each domain can be modified independently
- Bug fixes and features are localized to relevant app
- Code reviews can focus on single domain

**Enhanced Testability**:
- Unit tests target specific apps
- Integration tests verify app interactions
- Can achieve >80% code coverage per rubric requirement

**Clear URL Structure**:
```python
/accounts/register/          # accounts:register
/homes/                      # homes:home_list
/homes/5/                    # homes:home_detail
/maintenance/tasks/          # maintenance:task_list
/maintenance/schedule/       # maintenance:schedule_list
/tips/                       # tips:tip_list
/tips/submit/                # tips:tip_create
```

**Intuitive Admin Organization**:
- User management in "Accounts" section
- Home data in "Homes" section
- Maintenance content in "Maintenance" section
- Community moderation in "Tips" section

**Future Extensibility**:
- v1.1 email notifications naturally extend `maintenance/` app
- v1.2 service provider ratings naturally extend `homes/` app
- v2.0 analytics dashboard can add new `analytics/` app without disrupting existing structure

### Negative and Risks

**More Configuration**:
- Must register 4 apps in `INSTALLED_APPS`
- Must include 4 URL patterns in root `urls.py`
- Must configure 4 template directories (if app-specific templates used)

**Potential Import Complexity**:
- Cross-app imports require careful management (e.g., `maintenance.models.Schedule` references `homes.models.Home`)
- Risk of circular imports if not structured properly

**Learning Curve**:
- Students must understand app boundaries and URL namespacing
- More files to navigate initially

### Mitigations

**Configuration Management**:
- Document app configuration in README.md (completed)
- Provide PROJECT_SUMMARY.md with app responsibilities (completed)
- Use consistent naming conventions (models.py, views.py, urls.py, admin.py in each app)

**Import Strategy**:
```python
# Avoid circular imports by importing at function level when needed
# Or ensure imports flow in one direction: accounts ← homes ← maintenance ← tips

# Good: maintenance imports homes
from homes.models import Home

class Schedule(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

# Avoid: homes importing maintenance (creates circular dependency)
```

**Documentation**:
- Create app layout guide in README.md (completed)
- Provide consistent app scaffolds
- Document URL namespacing with examples

---

## Implementation notes

### App Configuration
Each app requires an `apps.py` with proper configuration:

```python
# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
```

### URL Namespacing
Each app provides namespaced URLs:

```python
# accounts/urls.py
app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

# home_maintenance_compass/urls.py
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('homes/', include('homes.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('tips/', include('tips.urls')),
]
```

### Template Organization
Templates follow app structure:

```
templates/
├── base.html                    # Shared base template
├── home.html                    # Landing page
├── accounts/
│   ├── register.html
│   └── profile.html
├── homes/
│   ├── home_list.html
│   └── home_detail.html
├── maintenance/
│   ├── task_list.html
│   └── schedule_list.html
└── tips/
    ├── tip_list.html
    └── tip_detail.html
```

### Admin Organization
Each app registers its models in its own `admin.py`:

```python
# homes/admin.py
from django.contrib import admin
from .models import Home, Appliance, ServiceProvider

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'year_built')
```

---

## Related decisions

- ADR-1.0.1: Custom User Model Implementation (defines accounts app models)
- ADR-1.0.2: Core Data Models (defines relationships between apps)
- ADR-1.0.3: Authentication and Authorization (defines security within app boundaries)
- ADR-1.0.4: URL Design and Routing (details URL namespacing strategy)

---

## References

- Matt Layman, "Understand Django" Chapter 8: Anatomy of an Application
- Django Documentation: Applications (https://docs.djangoproject.com/en/5.0/ref/applications/)
- Django Documentation: URL dispatcher (https://docs.djangoproject.com/en/5.0/topics/http/urls/)
- Two Scoops of Django: App Design
- PRD Section 4 (Scope Items) and Section 13 (Traceability)

---

## Revision history

- 2025-11-23: v1.0 Initial version - accepted
