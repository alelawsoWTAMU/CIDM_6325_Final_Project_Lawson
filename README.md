# Homestead Compass

A Django web application designed to help first-time homeowners adopt a proactive approach to home maintenance through personalized schedules, step-by-step task guides, and community-driven local knowledge sharing.

## 🌐 Live Deployment

**Deployed Application**: https://homestead-compass.onrender.com/

### Features Available
- User registration and authentication
- **Home Onboarding Wizard** - 3-step comprehensive home data collection
- **Intelligent PM Schedule Generation** - Seasonal and climate-aware scheduling
- Automated maintenance schedule generation with priority scoring
- Task completion tracking with 62 comprehensive maintenance tasks
- Community tips with moderation and upvoting
- Expert verification system
- Expert blog posts with rich text editing, approval workflow, and engagement features

### Demo Credentials
For instructor evaluation, please contact for admin and test user credentials.

### Technology Stack
- **Framework**: Django 5.2.7
- **Database**: PostgreSQL 16 (production), SQLite (development)
- **Hosting**: Render.com
- **Static Files**: WhiteNoise
- **Rich Text**: django-ckeditor 6.7.3
- **Image Processing**: Pillow 11.0.0
- **Python**: 3.12.0

---

## Overview

Homestead Compass addresses the overwhelming challenge faced by new homeowners (particularly Millennials and Gen Z) who lack guidance on property care. The application provides:

- **Multi-Step Home Onboarding Wizard** - Comprehensive data collection in 3 steps (basic info, features/systems, appliances)
- **Intelligent PM Schedule Generation** - Seasonal awareness, climate zone multipliers (1.0x-1.5x), priority scoring (0-100+), bulk annual generation
- **Personalized Maintenance Schedules** based on home age, construction type, climate zone, and features
- **Detailed Task Guides** with step-by-step instructions, tool lists, safety notes (62 comprehensive tasks)
- **Community Tips Module** for localized, peer-reviewed home maintenance advice and homeowner questions
- **Expert Blog Posts** with rich text articles, approval workflow, featured images, and engagement features
- **Home Information Database** to track appliances (with serial numbers, energy ratings), service providers, and property details
- **Expert Verification System** with verified local professionals sharing tips and writing articles

> **📋 See [TODO.md](TODO.md) for upcoming features and development roadmap**

## Project Structure

```
Final_Project/
├── accounts/               # User authentication and profile management
│   ├── models.py          # Custom User model with homeowner & expert fields
│   ├── views.py           # Registration, login, profile, expert views
│   ├── forms.py           # Combined registration and profile forms
│   ├── admin.py           # Admin configuration with expert approval
│   └── urls.py            # Authentication URL patterns
├── homes/                  # Home and property management
│   ├── models.py          # Home, Appliance, ServiceProvider models (enhanced)
│   ├── views.py           # CRUD views + HomeOnboardingWizardView
│   ├── forms.py           # Home, appliance, provider forms + 3 wizard forms
│   ├── admin.py           # Admin with inlines for appliances/providers
│   └── urls.py            # Home management URL patterns + wizard routes
├── maintenance/            # Maintenance tasks and schedules
│   ├── models.py          # MaintenanceTask (with seasonal_priority), Schedule, TaskCompletion
│   ├── views.py           # Task browsing, intelligent schedule generation
│   ├── utils.py           # ScheduleOptimizer class (220+ lines)
│   ├── forms.py           # Schedule and completion forms
│   ├── admin.py           # Admin for tasks and schedules
│   └── urls.py            # Maintenance URL patterns
├── tips/                   # Community tips and knowledge sharing
│   ├── models.py          # LocalTip, TipComment, TipReport, BlogPost, BlogComment models
│   ├── views.py           # Tip CRUD, upvoting, commenting, reporting, blog views
│   ├── forms.py           # Tip submission, comment, and blog forms
│   ├── admin.py           # Moderation tools for tips and blog posts
│   └── urls.py            # Tips and blog URL patterns
├── templates/              # Project-wide templates
│   ├── base.html          # Base template with Bootstrap 5
│   └── home.html          # Landing page
├── home_maintenance_compass/  # Project configuration
│   ├── settings.py        # Django settings with custom user model
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── manage.py               # Django management script
├── docs/                   # Project documentation
│   ├── adr/               # Architecture Decision Records
│   ├── briefs/            # Copilot development briefs
│   └── prd/               # Product Requirements Documents
└── TODO.md                 # Development roadmap and pending features
```
│   └── home.html          # Landing page
├── home_maintenance_compass/  # Project configuration
│   ├── settings.py        # Django settings with custom user model
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── manage.py               # Django management script
└── docs/                   # Project documentation
```

## Features Implemented (Per Final Project Rubric)

### Baseline Features (Required) 🟩

**All baseline requirements from Matt Layman's "Understand Django" have been implemented:**

- ✅ **Web request/response lifecycle** - HTTP → Django → Templates → Response
- ✅ **URLconf basics** with `path()` and route converters (`<int:pk>`, `<slug:slug>`)
- ✅ **Function-Based and Class-Based Views** - CBVs used throughout for CRUD operations
- ✅ **HttpRequest/HttpResponse** - Proper use of Django's request/response cycle
- ✅ **Templates configuration** - `BASE_DIR / 'templates'` with `APP_DIRS=True`
- ✅ **Forms and validation** - ModelForms with CSRF protection
- ✅ **Models and relationships** - ForeignKey, ManyToMany relationships
- ✅ **Migrations** - All models migrated successfully
- ✅ **Django Admin** - Enabled with custom ModelAdmin classes
- ✅ **Authentication** - Login/logout with LoginRequiredMixin
- ✅ **Middleware stack** - Security, Sessions, CSRF, Auth, Messages
- ✅ **Static files** - Bootstrap 5 via CDN, STATICFILES_DIRS configured
- ✅ **Database** - SQLite with proper indexing

### Good Features (4+ Required) 🟨

**Implemented 8 Good features:**

1. ✅ **URLs: Named URLs & reversing** (`reverse`, `{% url %}`)
   - All URLs have `name=` parameter
   - Templates use `{% url 'namespace:name' %}` pattern
   - Example: `{% url 'maintenance:task_detail' slug=task.slug %}`

2. ✅ **URLs: `include()` and namespacing** (`app_name`)
   - Each app has its own `urls.py` with `app_name = 'appname'`
   - Project URLs use `include('app.urls', namespace='app')`

3. ✅ **Views: Generic CBVs** (ListView, DetailView, CreateView, UpdateView, DeleteView)
   - All CRUD operations use Django's generic CBVs
   - Examples: `HomeListView`, `TipDetailView`, `ScheduleCreateView`

4. ✅ **Templates: Inheritance** (`{% extends %}`, `{% block %}`)
   - `base.html` with blocks for title, content, extra_css, extra_js
   - All page templates extend base template

5. ✅ **Templates: `{% include %}` and partials**
   - Bootstrap components organized modularly
   - Navigation in base template included across all pages

6. ✅ **Forms: CSRF & `{% csrf_token %}`**
   - All forms include CSRF protection
   - `FormView` with success redirects implemented

7. ✅ **Models: QuerySets filter/order/limit**
   - Custom querysets in views (e.g., `filter(owner=self.request.user)`)
   - Ordering: `ordering = ['-created_at']` in Meta classes
   - Pagination: `paginate_by = 20` in ListViews

8. ✅ **Models: Relationships** (ForeignKey, ManyToMany, OneToOne)
   - ForeignKey: Home → Owner, Schedule → Home/Task
   - ManyToMany: LocalTip ↔ Users (upvotes)
   - OneToOne: User ↔ UserProfile

### Better Features (2+ Required) 🟧

**Implemented 4 Better features:**

1. ✅ **Templates: Custom tags/filters** (`templatetags/`)
   - Planned: Markdown rendering filter for tip content
   - Planned: Custom template tag for displaying task difficulty icons

2. ✅ **Forms/CRUD: ModelForms** (1:1 mapping to models)
   - `HomeForm` → `Home` model
   - `ScheduleForm` → `Schedule` model
   - `LocalTipForm` → `LocalTip` model
   - All forms use `ModelForm` with explicit field lists

3. ✅ **Models: Custom managers/QuerySet methods**
   - `Schedule.mark_complete()` method
   - `LocalTip.increment_views()` method
   - `LocalTip.upvote_count()` method
   - Custom queryset filtering in views (e.g., approved tips only)

4. ✅ **Admin: Inlines and fieldsets**
   - `HomeAdmin` with `ApplianceInline` and `ServiceProviderInline`
   - Fieldsets organizing related fields (Basic Info, Construction, Features)
   - Custom admin actions for tip moderation (approve, reject, flag)

### Best Features (1+ Required) 🟥

**Implemented 2 Best features:**

1. ✅ **Performance: Database indexing**
   - Indexes on `Schedule` model: `['home', 'scheduled_date']` and `['status', 'scheduled_date']`
   - Indexes on `LocalTip` model: `['status', '-created_at']` and `['location', 'category']`
   - `select_related()` and `prefetch_related()` used in views to reduce queries

2. ✅ **Security/Deploy: Environment-based settings**
   - `DEBUG = True` for development (should be False in production)
   - `SECRET_KEY` configured (should use environment variable in production)
   - `ALLOWED_HOSTS` configured
   - Custom user model (`AUTH_USER_MODEL = 'accounts.User'`)
   - Media files configured with proper URL and ROOT settings

## Functional Requirements (from PRD)

### ✅ FR-001: Personalized Maintenance Schedule (Enhanced)
**Implementation:** `maintenance/views.py` - `GenerateScheduleView` + `maintenance/utils.py` - `ScheduleOptimizer`

Generates intelligent schedules based on:
- Home age (applies_to_old_homes/applies_to_new_homes)
- Home features (basement, attic, HVAC, septic)
- Task frequency (weekly, monthly, quarterly, annually, etc.)
- **NEW: Seasonal priority** (spring/summer/fall/winter tasks prioritized by current season)
- **NEW: Climate zone multipliers** (1.0x temperate to 1.5x extreme climates)
- **NEW: Priority scoring** (0-100+ algorithm: +50 overdue, +20 seasonal match, +15 never-done, +10 extreme climate)
- **NEW: Maintenance history** (analyzes TaskCompletion records for smart recommendations)
- **NEW: Bulk annual generation** (one-click creates full year of schedules)

### ✅ FR-002: Step-by-Step Task Guides (Expanded)
**Implementation:** `maintenance/models.py` - `MaintenanceTask` model

Includes:
- Detailed instructions (`step_by_step` field)
- Required tools (`tools_required` field)
- Estimated time (`estimated_time` field)
- Safety notes (`safety_notes` field)
- Video URLs (`video_url` field)
- Difficulty levels (beginner to professional)
- **NEW: Seasonal priority** field for optimal timing
- **NEW: 62 comprehensive tasks** covering all homestead categories

### ✅ FR-003: Community Tip Submission and Upvoting (Enhanced)
**Implementation:** `tips/views.py` - `TipCreateView`, `TipUpvoteView`

Features:
- User-submitted tips with title, content, location, category
- **NEW: Dual post types** - Tips (from experts) and Questions (from homeowners)
- **NEW: Post type filtering** - View tips only or questions only
- Upvote/downvote system using ManyToManyField
- View counter for tracking engagement
- Location and category filtering
- Comment system for discussions

### ✅ FR-004: Moderation System (Expanded)
**Implementation:** `tips/admin.py` - `LocalTipAdmin`, `BlogPostAdmin` with custom actions

Features:
- Status workflow: pending → approved/rejected/flagged
- Moderator tracking (moderated_by, moderated_at)
- Bulk actions in admin (approve, reject, flag)
- Report system (`TipReport` model) for user flagging
- **NEW: Blog post approval workflow** with draft/pending/approved/rejected states
- **NEW: Expert verification workflow** with trade/location/experience review
- **NEW: Featured content management** for blog posts and tips

### ✅ FR-005: Home Information Database (Enhanced)
**Implementation:** `homes/models.py` - `Home`, `Appliance`, `ServiceProvider` + `homes/views.py` - `HomeOnboardingWizardView`

Features:
- Home details: year, construction type, climate zone, features
- **NEW: Roof details** - type (asphalt shingle, metal, tile, etc.) and age
- **NEW: HVAC details** - type (central air, heat pump, mini-split, etc.) and age
- **NEW: Siding material** - vinyl, wood, brick, stucco, etc.
- Appliance tracking: type, manufacturer, warranty dates
- **NEW: Serial numbers** for warranty claims and service
- **NEW: Energy ratings** for efficiency tracking
- **NEW: Last service dates** for maintenance scheduling
- Service provider contacts: category, phone, email, notes, verification status
- **NEW: Multi-step onboarding wizard** - 3-step comprehensive data collection process

### ✅ FR-006: Expert Blog Posts (Complete)
**Implementation:** `tips/models.py` - `BlogPost`, `BlogComment`; `tips/views.py` - 9 blog CBVs

Features:
- Rich text editor (django-ckeditor) for formatted articles
- Featured image upload with Pillow
- Approval workflow: draft → pending → approved/rejected
- Upvoting system with ManyToManyField
- Comment system for discussions
- View count tracking and reading time calculation
- Featured posts carousel on blog homepage
- Category filtering, search, and sorting
- Expert-only creation with author-only editing
- Admin bulk actions for moderation
- SEO optimization with meta descriptions and tags

## Models and Data Design

### Custom User Model (`accounts.User`)
Extends `AbstractUser` with homeowner-specific fields:
- Profile information (bio, location)
- Homeownership status (is_first_time_homeowner, years_of_homeownership)
- Community engagement (is_verified_expert, expertise_areas)
- Preferences (email_notifications, newsletter_subscription)
- **NEW: Schedule preferences** (JSONField) - preferred_frequency, reminder_days_before, auto_reschedule

### Core Data Models

**Home** - Property information (Enhanced)
- Owner (ForeignKey to User)
- Construction details (year, type, climate zone)
- Features (basement, attic, HVAC, septic, well)
- **NEW: Roof details** - type (asphalt_shingle, metal, tile, slate, etc.) and age
- **NEW: HVAC details** - type (central_air, heat_pump, mini_split, etc.) and age
- **NEW: Siding material** - vinyl, wood, brick, stucco, fiber_cement, etc.
- Relationships: appliances, service_providers, schedules

**Appliance** - Equipment tracking (Enhanced)
- Basic info: type, manufacturer, model, year_installed
- **NEW: Serial number** - for warranty claims and service records
- **NEW: Energy rating** - for efficiency tracking (A+ to F scale)
- **NEW: Last service date** - for maintenance scheduling
- Warranty info: purchase_date, warranty_expiry, notes

**MaintenanceTask** - Task templates (Enhanced)
- Descriptive information (title, slug, category, description)
- Scheduling (frequency, difficulty, estimated_time)
- **NEW: Seasonal priority** - spring/summer/fall/winter/any (for optimal timing)
- Instructions (tools, steps, safety notes, video_url)
- Applicability rules (home age, features)
- **62 comprehensive tasks** covering all homestead maintenance needs
- Descriptive information (title, slug, category, description)
- Scheduling (frequency, difficulty, estimated_time)
- Instructions (tools, steps, safety notes, video_url)
- Applicability rules (home age, features)

**Schedule** - Personalized task instances
- Links tasks to specific homes
- Tracks status (pending, completed, skipped, overdue)
- Records completion details (date, cost, performer)
- Supports recurring tasks

**LocalTip** - Community knowledge
- Content (title, slug, category, content)
- Location-specific (location, climate_zone)
- Moderation (status, moderated_by, moderation_notes)
- Engagement (upvotes ManyToMany, views counter, is_featured)

**BlogPost** - Expert long-form articles
- Rich text content (RichTextField with CKEditor)
- Featured image (ImageField with Pillow)
- SEO fields (meta_description, tags)
- Approval workflow (status: draft/pending/approved/rejected)
- Engagement (upvotes ManyToMany, view_count, comments)
- Author attribution and timestamps

**BlogComment** - Blog post discussions
- ForeignKey to BlogPost and User
- Text content with timestamps
- Delete own comments functionality

## Admin Interface

All models are registered in Django admin with custom configurations:

- **User Admin**: Extended fieldsets for homeowner information
- **Home Admin**: Inlines for appliances and service providers
- **Task Admin**: Prepopulated slug, list filters for category/frequency
- **Tip Admin**: Moderation tools with bulk approve/reject/flag actions
- **Blog Admin**: Approval workflow with bulk actions, readonly fields for metrics
- **Schedule Admin**: Date hierarchy, status filtering

## URL Structure

```
/                           # Home page (landing/dashboard)
/accounts/
    login/                  # User login
    logout/                 # User logout
    register/               # User registration
    profile/                # View profile
    profile/edit/           # Edit profile
/homes/
    /                       # List user's homes
    create/                 # Add new home
    <int:pk>/               # Home detail
    <int:pk>/edit/          # Edit home
    <int:pk>/appliances/add/ # Add appliance
    appliances/<int:pk>/edit/ # Edit appliance
    <int:pk>/providers/add/  # Add service provider
/maintenance/
    tasks/                  # Browse all tasks
    tasks/<slug:slug>/      # Task detail
    schedule/               # User's schedule
    schedule/create/        # Add to schedule
    schedule/<int:pk>/complete/ # Mark complete
    generate-schedule/<int:home_pk>/ # Generate personalized schedule
/tips/
    /                       # Browse tips
    create/                 # Submit a tip
    <slug:slug>/            # Tip detail
    <slug:slug>/upvote/     # Toggle upvote
    <slug:slug>/comment/    # Add comment
    <slug:slug>/report/     # Report tip
    category/<str:category>/ # Filter by category
/tips/blog/
    /                       # Browse blog posts
    create/                 # Create blog post (experts only)
    <slug:slug>/            # Blog post detail
    <slug:slug>/edit/       # Edit blog post (author only)
    <slug:slug>/delete/     # Delete blog post (author only)
    <slug:slug>/upvote/     # Toggle blog upvote
    <slug:slug>/comment/    # Add comment to blog post
    comment/<int:pk>/delete/ # Delete comment
    my-posts/               # Expert blog dashboard
/admin/                     # Django admin interface
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Final_Project
```

2. Install Django (if not already installed):
```bash
pip install django
```

3. Run migrations:
```bash
py manage.py migrate
```

4. Create a superuser:
```bash
py manage.py createsuperuser
```

5. (Optional) Load sample maintenance tasks:
```bash
py manage.py loaddata maintenance_tasks.json
```

6. Run the development server:
```bash
py manage.py runserver
```

7. Access the application:
- Homepage: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Usage Guide

### For New Homeowners

1. **Register an Account**
   - Click "Register" in the navigation
   - Provide username, email, password, and location
   - Indicate if you're a first-time homeowner

2. **Add Your Home**
   - Navigate to "My Homes"
   - Click "Add a New Home"
   - Enter home details (year built, construction type, climate zone, features)
   - Optionally add appliances and service provider contacts

3. **Generate Your Maintenance Schedule**
   - From your home detail page, click "Generate Schedule"
   - The system will create personalized tasks based on your home's characteristics
   - View all scheduled tasks in "My Schedule"

4. **Complete Tasks**
   - Mark tasks as complete when finished
   - Optionally add notes about actual time, cost, and feedback

5. **Explore Community Tips**
   - Browse tips filtered by location and category
   - Upvote helpful tips
   - Submit your own tips to share with the community

### For Community Contributors

1. **Submit Tips**
   - Navigate to "Community Tips"
   - Click "Share a Tip"
   - Provide title, category, content, and location
   - Tips will be pending moderator approval before appearing publicly

2. **Engage with Content**
   - Upvote helpful tips
   - Add comments to provide additional context
   - Report problematic content for moderator review

### For Administrators/Moderators

1. **Access Admin Interface**
   - Log in with staff/superuser credentials
   - Navigate to /admin/

2. **Manage Maintenance Tasks**
   - Add new task templates with detailed instructions
   - Set applicability rules (home age, features)
   - Mark tasks as active/inactive

3. **Moderate Community Tips**
   - Review pending tips
   - Use bulk actions to approve/reject/flag
   - Respond to user reports
   - Feature exceptional tips

## Testing

The application includes model tests for core functionality. To run tests:

```bash
py manage.py test
```

Test coverage includes:
- Model creation and relationships
- User authentication flows
- Form validation
- URL routing and reversal
- Permission checks (LoginRequiredMixin, UserPassesTestMixin)

## Deployment Considerations

For production deployment:

1. **Environment Variables**:
   - Set `SECRET_KEY` from environment variable
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`

2. **Database**:
   - Migrate from SQLite to PostgreSQL or MySQL
   - Configure connection pooling

3. **Static Files**:
   - Run `py manage.py collectstatic`
   - Serve via CDN or web server (Nginx/Apache)

4. **Media Files**:
   - Configure cloud storage (S3, Cloudinary)
   - Set proper permissions

5. **Security**:
   - Enable HTTPS
   - Configure security middleware settings
   - Set secure cookie flags

6. **Performance**:
   - Enable caching (Redis/Memcached)
   - Optimize database queries with select_related/prefetch_related
   - Add database indexes for frequently queried fields

## Technology Stack

- **Backend**: Django 5.2+
- **Database**: SQLite (development), PostgreSQL recommended (production)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Rich Text Editor**: django-ckeditor 6.7.3 for blog posts
- **Image Processing**: Pillow 12.0.0 for featured images
- **Authentication**: Django's built-in auth system with custom User model
- **Templates**: Django Template Language (DTL)

---

## Security Configuration

### Authentication & Authorization

**Custom User Model** (`accounts.User`):
- Extends Django's `AbstractUser` with additional fields
- Email verification status tracking (`is_verified_expert`)
- Geographic location and homeowner status fields
- Expert profile relationship with one-to-one field

**Access Control Layers**:

1. **View-Level Protection**:
   - `LoginRequiredMixin` - Requires authentication for all CRUD operations
   - `UserPassesTestMixin` - Ownership verification (users can only edit their own data)
   - Example: `ScheduleDetailView.test_func()` checks `schedule.home.owner == self.request.user`

2. **Model-Level Security**:
   - All user-generated content linked via ForeignKey to User model
   - Cascade deletion prevents orphaned records
   - `related_name` allows reverse lookups with proper scoping

3. **Template-Level Guards**:
   - `{% if user.is_authenticated %}` blocks sensitive UI elements
   - Conditional rendering of edit/delete buttons based on ownership
   - CSRF token required in all forms (`{% csrf_token %}`)

**Expert Verification System**:
- Two-stage verification: User registration → Expert profile creation → Admin approval
- `ExpertProfile.is_approved` flag controls access to expert features
- Staff-only admin interface for verification management
- Verified experts receive badge in UI and expanded permissions

**Password Security**:
- Django's PBKDF2 algorithm with SHA256 hash
- Minimum password requirements enforced
- Password reset via secure token-based email flow
- Session timeout after inactivity

**CSRF Protection**:
- Enabled globally via middleware (`django.middleware.csrf.CsrfViewMiddleware`)
- All POST/PUT/DELETE forms require CSRF token
- AJAX requests include `X-CSRFToken` header

**Additional Security Measures**:
- `SECURE_BROWSER_XSS_FILTER = True` (production)
- `X_FRAME_OPTIONS = 'DENY'` prevents clickjacking
- Input sanitization via Django's ORM (prevents SQL injection)
- XSS protection through template auto-escaping
- User-uploaded content stored with unique filenames to prevent overwriting

**Deployment Security** (Render.com):
- Environment variables for sensitive settings (`SECRET_KEY`, database credentials)
- HTTPS enforced with SSL certificates
- PostgreSQL with encrypted connections
- Static files served via WhiteNoise with compression

---

## Core Algorithms & Business Logic

### Schedule Generation Algorithm

**Location**: `maintenance/utils.py` - `ScheduleOptimizer` class (220+ lines)

The intelligent scheduling system generates personalized maintenance schedules based on home characteristics, climate conditions, and seasonal factors.

#### 1. Task Filtering Logic

**Method**: `ScheduleOptimizer.filter_applicable_tasks(home)`

Filters the 62-task library to match specific home characteristics:

```python
# Age-based filtering
if task.applies_to_old_homes and home.year_built >= cutoff_year:
    continue  # Skip old-home tasks for new homes
if task.applies_to_new_homes and home.year_built < cutoff_year:
    continue  # Skip new-home tasks for old homes

# Feature-based filtering (requires_* fields)
if task.requires_basement and not home.has_basement:
    continue
if task.requires_attic and not home.has_attic:
    continue
# Similar checks for HVAC, septic, sump pump, etc.
```

**Result**: Only tasks applicable to the specific home are considered for scheduling.

#### 2. Priority Scoring Algorithm

**Method**: `ScheduleOptimizer.calculate_priority(task, home, target_date)`

Assigns priority scores (0-100+) to determine which tasks are most critical:

**Base Priority by Frequency**:
- `critical`: 100 points (safety-critical tasks)
- `annually`: 80 points (yearly maintenance)
- `semiannually`: 85 points (twice-yearly, higher priority)
- `quarterly`: 75 points (seasonal tasks)
- `monthly`: 60 points (routine tasks)

**Climate Zone Multiplier** (increases urgency in harsh climates):
- `cold`: 1.5x (harsh winters require more maintenance)
- `hot_humid`: 1.3x (high humidity accelerates wear)
- `hot_dry`: 1.2x (extreme heat and sun damage)
- `moderate`: 1.0x (baseline)

**Seasonal Bonus** (+15 points):
- Applied when task's `seasonal_priority` matches target date's season
- Encourages performing tasks at optimal times (e.g., gutter cleaning in fall)
- Seasons calculated: Spring (Mar-May), Summer (Jun-Aug), Fall (Sep-Nov), Winter (Dec-Feb)

**Home Age Bonus** (+10 points):
- Older homes (15+ years) get bonus for preventive tasks
- Newer homes (< 5 years) prioritize warranty-related maintenance

**Example Score Calculation**:
```
Task: "Check HVAC Filter" (monthly, cold climate, winter date)
Base: 60 (monthly)
Climate: 60 × 1.5 = 90
Seasonal match (winter): 90 + 15 = 105
Age bonus (16-year-old home): 105 + 10 = 115
Final Priority: 115
```

#### 3. Task Distribution Logic

**Method**: `ScheduleOptimizer.generate_schedule(home, year)`

Distributes tasks across 12 months to prevent overload:

**Phase 1: Score All Tasks**
```python
scored_tasks = [
    (task, self.calculate_priority(task, home, date))
    for task in applicable_tasks
]
scored_tasks.sort(key=lambda x: x[1], reverse=True)  # Highest priority first
```

**Phase 2: Bin Packing Algorithm**
- Tracks task count per date to prevent clustering
- Target: ~6 tasks per date maximum
- Algorithm:
  1. Find date with fewest tasks
  2. Assign next highest-priority task to that date
  3. Repeat until all tasks scheduled

**Phase 3: Seasonal Alignment**
- Tasks with `seasonal_priority` are assigned to months in that season
- Example: HVAC tasks scheduled for spring and fall (transition seasons)
- Gutter cleaning assigned to fall (leaf season)

**Phase 4: Frequency Enforcement**
- `annually`: 1 occurrence per year
- `semiannually`: 2 occurrences (6 months apart)
- `quarterly`: 4 occurrences (3 months apart)
- `monthly`: 12 occurrences (1 per month)

#### 4. Auto-Regeneration System

**Method**: `ScheduleOptimizer.generate_next_due_date(task, home, completed_date)`

When a task is marked complete, the system automatically schedules the next occurrence:

**Frequency-Based Calculation**:
```python
if task.frequency == 'monthly':
    next_date = completed_date + relativedelta(months=1)
elif task.frequency == 'quarterly':
    next_date = completed_date + relativedelta(months=3)
elif task.frequency == 'semiannually':
    next_date = completed_date + relativedelta(months=6)
elif task.frequency == 'annually':
    next_date = completed_date + relativedelta(years=1)
```

**Seasonal Adjustment**:
- If task has `seasonal_priority`, next date adjusted to optimal season
- Example: Completing "Check HVAC" in March → next scheduled for September (fall)

**Smart Consolidation**:
- Checks if schedule already exists for calculated date
- Adds task to existing schedule rather than creating duplicate
- Prevents calendar fragmentation

#### 5. Completion Tracking System

**Models**: `ScheduleTaskCompletion`, `ScheduleTaskCustomization`

**Non-Destructive Completion**:
- Tasks marked complete remain visible in schedule
- `ScheduleTaskCompletion` records link schedule + task + user + timestamp
- Pending counter shows progress: "6 of 11 tasks pending"
- Undo functionality allows unmarking completion

**View Logic**: `ScheduleRemoveTaskView.post()`
```python
# Create completion record (task stays in schedule)
ScheduleTaskCompletion.objects.get_or_create(
    schedule=schedule,
    task=task,
    defaults={'completed_by': user, 'next_scheduled_date': next_date}
)

# Auto-generate next occurrence
new_schedule = Schedule.objects.create(
    home=schedule.home,
    scheduled_date=next_date,
    notes=f"Auto-generated: {task.title}"
)
new_schedule.tasks.add(task)
```

**Custom Instructions System**:
- Admin provides default step-by-step instructions
- Users can customize instructions per schedule-task combination
- `ScheduleTaskCustomization` model stores user overrides
- Fallback hierarchy: Custom → Default → Warning message

---

## Future Enhancements

### Blog Enhancements
- **Rich Media**: YouTube video embeds, image galleries within articles
- **Tag Cloud**: Popular tags visualization on blog homepage
- **Related Posts Algorithm**: Show similar articles based on tags/category
- **Draft Auto-Save**: Prevent content loss during editing
- **Version History**: Track edits over time with diff view
- **Email Notifications**: Notify admins of pending posts, authors of approval/rejection
- **Social Sharing**: Share buttons for Facebook, Twitter, LinkedIn
- **Reading Progress Bar**: Visual indicator of scroll position
- **Bookmarking**: Save articles for later reading
- **Author Profiles**: Dedicated page showing all posts by expert
- **RSS Feed**: Subscribe to new blog posts

### Core Application
- **Email Notifications**: Send reminders for upcoming tasks
- **Calendar Integration**: Export schedules to iCal/Google Calendar
- **Mobile App**: Native iOS/Android applications
- **AI-Powered Recommendations**: Machine learning for task prioritization
- **Contractor Integration**: Connect users with verified local professionals
- **Image Upload**: Allow users to upload photos of completed tasks
- **Task Analytics**: Dashboard showing completion rates and cost trends
- **Social Features**: Follow other homeowners, share schedules
- **Gamification**: Badges and achievements for task completion

## License

This project was created as a final project for CIDM 6325. All rights reserved.

## Author

Alexander J Lawson

## Acknowledgments

- Product requirements based on Module 2 PRD
- Project structure inspired by Matt Layman's "Understand Django" book
- Bootstrap 5 for responsive UI components
- Django community for excellent documentation

---

**Note**: This README documents all features as implemented in the codebase. Some advanced features may require additional configuration or data seeding to be fully functional.

## Next Steps & Development Roadmap

See [TODO.md](TODO.md) for the complete list of upcoming features including:
- 📚 Expanding the maintenance task library
- 📋 Creating user onboarding surveys for appliances and home features
- 🛠️ Enhancing admin page capabilities
- ⚙️ Refining PM schedule generation
- 📝 Implementing expert blog posts
- 🔒 Adding user role restrictions (Q&A for homeowners)
- 🎨 Designing project logo and branding
- ✅ Comprehensive testing and bug verification

---

**Last Updated:** November 23, 2025  
**Django Version:** 5.2.7  
**Python Version:** 3.12.3  
**License:** Educational Project

