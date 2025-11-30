## Summary

A Django web application designed to help first-time homeowners adopt a proactive approach to home maintenance through personalized schedules, step-by-step task guides, and community-driven local knowledge sharing. 

## 🌐 Live Deployment

**Production URL**: https://homestead-compass.onrender.com/

**GitHub Repository**: https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry/tree/Final_Project

### Key Features
- User registration and authentication with custom User model
- **Home Onboarding Wizard** - 3-step comprehensive home data collection
- **Intelligent Schedule Generation** - Seasonal and climate-aware scheduling with priority scoring (0-100+)
- Task completion tracking with 62 comprehensive maintenance tasks
- Community tips with moderation, upvoting, and Q&A system
- Expert verification system with trade validation
- Expert blog posts with rich text editing, approval workflow, and engagement features

### Technology Stack
- **Framework**: Django 5.2.7
- **Database**: PostgreSQL 16 (production), SQLite (development)
- **Hosting**: Render.com with automatic deployments
- **Static Files**: WhiteNoise with compression
- **Rich Text**: django-ckeditor 6.7.3
- **Image Processing**: Pillow 11.0.0
- **Python**: 3.12.3

## Overview

Homestead Compass addresses the overwhelming challenge faced by new homeowners who lack guidance on property care. The application provides:

- **Multi-Step Home Onboarding Wizard** - Comprehensive data collection covering basic info, features/systems, and appliances
- **Intelligent Schedule Generation** - Seasonal awareness, climate zone multipliers (1.0x-1.5x), priority scoring algorithm
- **Comprehensive Task Library** - 62 detailed maintenance tasks with step-by-step instructions, tool lists, and safety notes
- **Community Knowledge Sharing** - Tips module with dual post types (expert tips and homeowner questions)
- **Expert Blog Platform** - Long-form articles with rich text editing, approval workflow, and engagement tracking
- **Home Information Database** - Track appliances (with serial numbers, energy ratings), service providers, and property details
- **Expert Verification System** - Validated local professionals sharing knowledge and writing articles

## Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/alelawsoWTAMU/CIDM_6325_Final_Project_Lawson.git
cd CIDM_6325_Final_Project_Lawson
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Load sample data** (optional)
```bash
bash load_all_data.sh  # On Windows: use Git Bash or load fixtures individually
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Homepage: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

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
├── docs/                   # Project documentation
│   ├── adr/               # Architecture Decision Records
│   ├── briefs/            # Development briefs
│   ├── prd/               # Product Requirements Documents
│   └── *.md               # Status reports, checklists, deployment guides
├── fixtures/               # Sample data for development/production
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── load_all_data.sh        # Fixture loading script for production
└── export_data.sh          # Fixture export script
```

## Core Features

### 1. Home Onboarding Wizard
**3-step comprehensive data collection process**
- **Step 1**: Basic home information (address, year built, construction type, climate zone)
- **Step 2**: Features and systems (basement, attic, HVAC type/age, roof type/age, siding material)
- **Step 3**: Appliances tracking (type, manufacturer, model, serial numbers, energy ratings)

### 2. Intelligent Schedule Generation
**Advanced algorithm with priority scoring (0-100+)**
- Climate zone multipliers (1.0x-1.5x for harsh conditions)
- Seasonal priority matching (spring/summer/fall/winter tasks)
- Home age and feature-based filtering
- Task frequency enforcement (weekly to annually)
- Automatic next-occurrence scheduling upon completion

### 3. Maintenance Task Library
**62 comprehensive tasks with detailed guidance**
- Step-by-step instructions with safety notes
- Required tools and estimated time
- Difficulty levels (beginner to professional)
- Video tutorial links
- Seasonal priority indicators

### 4. Community Tips & Q&A
**Dual post type system**
- **Expert Tips**: Verified professionals sharing knowledge
- **Homeowner Questions**: Community-driven Q&A
- Upvoting and comment system
- Category and location filtering
- Moderation workflow (pending/approved/rejected/flagged)

### 5. Expert Blog Platform
**Long-form article system with rich features**
- Rich text editor (CKEditor) with formatting
- Featured image uploads
- Draft/pending/approved workflow
- Upvoting and comment system
- View count and engagement tracking
- Category-based organization

### 6. Expert Verification System
**Professional validation workflow**
- Trade/specialty specification
- Location and experience documentation
- Admin approval process
- Verified badge display
- Access to blog creation

## Django Framework Implementation

### Baseline Features (All Implemented) ✅

- ✅ Web request/response lifecycle
- ✅ URLconf with `path()` and route converters
- ✅ Function-Based and Class-Based Views
- ✅ HttpRequest/HttpResponse handling
- ✅ Templates with `APP_DIRS=True`
- ✅ Forms with CSRF protection
- ✅ Models with relationships (ForeignKey, ManyToMany)
- ✅ Database migrations
- ✅ Django Admin with custom configurations
- ✅ Authentication (LoginRequiredMixin, UserPassesTestMixin)
- ✅ Middleware stack (Security, Sessions, CSRF, Auth, Messages)
- ✅ Static files configuration
- ✅ SQLite database with proper indexing

### Good Features (8 Implemented) ✅

1. ✅ Named URLs and reversing (`reverse`, `{% url %}`)
2. ✅ `include()` and URL namespacing
3. ✅ Generic CBVs (ListView, DetailView, CreateView, UpdateView, DeleteView)
4. ✅ Template inheritance (`{% extends %}`, `{% block %}`)
5. ✅ Template includes and partials
6. ✅ CSRF protection with `{% csrf_token %}`
7. ✅ QuerySet filtering, ordering, and limiting
8. ✅ Model relationships (ForeignKey, ManyToMany, OneToOne)

### Better Features (4 Implemented) ✅

1. ✅ Custom template tags and filters (`templatetags/maintenance_extras.py`)
2. ✅ ModelForms with 1:1 model mapping (HomeForm, ScheduleForm, LocalTipForm, BlogPostForm)
3. ✅ Custom model managers and QuerySet methods (`mark_complete()`, `increment_views()`)
4. ✅ Admin inlines and fieldsets (HomeAdmin with ApplianceInline, ServiceProviderInline)

### Best Features (2 Implemented) ✅

1. ✅ **Database indexing** - Indexes on Schedule and LocalTip models for performance
2. ✅ **Environment-based settings** - Production configuration with environment variables, custom user model

## Key Technical Implementations

### Schedule Generation Algorithm
**Location**: `maintenance/utils.py` - `ScheduleOptimizer` (220+ lines)

Intelligent scheduling system with:
- **Priority Scoring**: 0-100+ algorithm considering climate, season, home age
- **Climate Multipliers**: 1.0x (temperate) to 1.5x (extreme climates)
- **Seasonal Alignment**: Tasks scheduled in optimal seasons
- **Task Distribution**: Bin packing algorithm prevents clustering
- **Auto-Regeneration**: Next occurrence scheduled upon completion

### Custom User Model
**Location**: `accounts/models.py` - `User(AbstractUser)`

Extended user model with:
- Homeowner information (is_first_time_homeowner, years_of_homeownership)
- Expert verification (is_verified_expert, expertise_areas)
- Schedule preferences (JSONField for customization)
- Profile information (bio, location)

### Security Implementation
- LoginRequiredMixin and UserPassesTestMixin for view protection
- Ownership verification (users can only edit their own data)
- CSRF protection on all forms
- Password hashing with PBKDF2-SHA256
- Expert verification workflow with admin approval

## Data Models

**Home** - Property information with enhanced details
- Construction details (year, type, climate zone, roof type/age, HVAC type/age, siding material)
- Features (basement, attic, septic, well, pool)
- Relationships: appliances, service_providers, schedules

**MaintenanceTask** - Task templates (62 comprehensive tasks)
- Instructions (step-by-step, tools, safety notes, video URLs)
- Scheduling (frequency, difficulty, estimated_time, seasonal_priority)
- Applicability rules (home age, features)

**Schedule** - Personalized task instances
- Links tasks to homes with status tracking
- Records completion details and supports recurring tasks

**LocalTip** - Community knowledge sharing
- Dual post types (expert tips, homeowner questions)
- Moderation workflow with upvoting and comments

**BlogPost** - Expert long-form articles
- Rich text content with CKEditor
- Featured images, approval workflow, engagement metrics

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

## Usage Guide

### User Roles

Homestead Compass supports three distinct user roles, each with specific capabilities and permissions:

#### 🏠 Homeowners
**Core Capabilities:**
- Create and manage multiple home profiles
- Complete 3-step onboarding wizard (basic info, features/systems, appliances)
- Generate personalized maintenance schedules using intelligent algorithm
- View and complete maintenance tasks with step-by-step instructions
- Track maintenance history and completion records
- Browse community tips filtered by location and category
- Upvote helpful tips and comment on posts
- **Ask questions** to the community (post_type: 'question')
- View expert blog articles

**Restrictions:**
- Cannot create expert tips (post_type: 'tip')
- Cannot write blog posts
- Cannot access admin interface
- Can only edit their own homes, schedules, and content

#### 🔧 Verified Experts
**All Homeowner Capabilities PLUS:**
- **Share expert tips** with the community (post_type: 'tip')
- **Write long-form blog articles** with rich text editor (CKEditor)
- Upload featured images for blog posts
- Answer homeowner questions with expertise
- Display verified expert badge on profile and posts
- Build reputation through upvotes and engagement metrics

**Verification Process:**
1. Register as standard user
2. Apply for expert status via profile page
3. Provide credentials (trade/specialty, location, years of experience)
4. Admin reviews and approves/rejects application
5. Approved experts receive verified badge and expanded permissions

**Restrictions:**
- Cannot access admin interface
- Cannot moderate other users' content
- Blog posts require admin approval before publication

#### 👨‍💼 Administrators
**All Expert Capabilities PLUS:**
- Access Django admin interface at `/admin/`
- **Moderate community content:**
  - Approve/reject/flag community tips
  - Approve/reject/flag blog posts
  - Bulk actions for efficient moderation
  - View moderation history and notes
- **Manage users:**
  - Verify expert credentials (approve/reject applications)
  - Edit user profiles and permissions
  - Grant/revoke staff and superuser status
- **Manage maintenance tasks:**
  - Create/edit/delete task templates
  - Set applicability rules (home age, features)
  - Configure seasonal priorities and difficulty levels
- **Monitor system:**
  - View engagement metrics (views, upvotes, comments)
  - Feature exceptional content on homepage
  - Review user reports and flagged content
  - Export data to fixtures

**Full Permissions:**
- Create, read, update, delete all content
- Bypass approval workflows
- Access all administrative functions

### Quick Start by Role

**For Homeowners:**
1. Register and complete the 3-step home onboarding wizard
2. Generate intelligent maintenance schedule for your home
3. Browse 62 comprehensive task guides with step-by-step instructions
4. Track task completion and view maintenance history
5. Ask questions and get advice from the community

**For Experts:**
1. Complete expert verification process (trade, location, experience)
2. Share tips and answer homeowner questions
3. Write long-form blog articles with rich text editor
4. Build reputation through upvotes and engagement

**For Administrators:**
1. Access admin interface at `/admin/`
2. Moderate community tips and blog posts (approve/reject/flag)
3. Verify expert credentials and manage user permissions
4. Monitor engagement metrics and featured content

## Deployment

**Production Environment** (Render.com):
- Automatic deployments from GitHub (`Final_Project` branch)
- PostgreSQL 16 database
- WhiteNoise for static file serving
- Environment variables for `SECRET_KEY`, `DATABASE_URL`
- HTTPS enforced with SSL certificates

**Fixture Management**:
- `export_data.sh` - Export all data to JSON fixtures
- `load_all_data.sh` - Load 10 fixtures in dependency order
- Run in Render Shell after deployment to seed production database

**See [docs/DEPLOYMENT_INSTRUCTIONS.md](docs/DEPLOYMENT_INSTRUCTIONS.md) for complete deployment guide**

## Documentation

- **[PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md)** - Executive summary and feature overview
- **[DEPLOYMENT_INSTRUCTIONS.md](docs/DEPLOYMENT_INSTRUCTIONS.md)** - Production deployment guide
- **[AI_USAGE_DISCLOSURE.md](docs/AI_USAGE_DISCLOSURE.md)** - AI assistance disclosure
- **[RUBRIC_COMPLIANCE.md](docs/RUBRIC_COMPLIANCE.md)** - Django feature checklist
- **[adr/](docs/adr/)** - Architecture Decision Records
- **[prd/](docs/prd/)** - Product Requirements Documents

## Author & License

**Author**: Alexander J Lawson  
**Course**: CIDM 6325 - Web Application Development  
**Institution**: West Texas A&M University  
**Term**: Fall 2025

This project was created as a final project for CIDM 6325. All rights reserved.

## Acknowledgments

- Django community for excellent documentation and framework
- Matt Layman's "Understand Django" for project structure guidance
- Bootstrap 5 for responsive UI components
- CKEditor team for rich text editing capabilities

---

**Last Updated**: November 29, 2025  
**Django Version**: 5.2.7  
**Python Version**: 3.12.3
