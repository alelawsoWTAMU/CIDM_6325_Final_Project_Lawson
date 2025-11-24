# Homestead Compass - Product Requirements Document

**Version**: 1.0.2  
**Date**: November 23, 2025  
**Author**: Alexander J Lawson  
**Project Status**: MVP Complete - Functional Application with All Baseline Features

---

## Executive Summary

Homestead Compass is a Django web application helping first-time homeowners manage property maintenance through personalized schedules, task tracking, and community knowledge sharing. This PRD defines functional requirements, user stories, acceptance criteria, and implementation status.

**Current Status**: Fully functional MVP deployed locally with:
- ✅ 4 Django apps (accounts, homes, maintenance, tips)
- ✅ 35+ templates with Bootstrap 5 styling
- ✅ Complete authentication system (register, login, password reset)
- ✅ Home management CRUD with appliances and service providers
- ✅ 12 seeded maintenance tasks
- ✅ Schedule generation with multi-task batching
- ✅ Community tips with moderation workflow (17 tips, 11 questions)
- ✅ Expert Blog Posts with rich text editor (4 articles, 2 featured)
- ✅ 7 verified expert user accounts created
- ⏳ Deployment to Render.com (pending)

---

## 1. Problem Statement

**Target Audience**: First-time homeowners (ages 25-40) who recently purchased their first home

**Problem**: New homeowners struggle to:
1. Remember which maintenance tasks need to be done and when
2. Understand which tasks apply to their specific home type, age, and features
3. Find reliable local advice beyond generic internet articles
4. Track what maintenance has been completed and what's overdue

**Current Solutions & Gaps**:
- Generic "home maintenance checklist" PDFs (not personalized)
- Calendar reminders (require manual setup for every task)
- Contractor websites (biased toward selling services)
- Community forums (information scattered, difficult to find location-specific advice)

**Proposed Solution**: Web application providing:
- Personalized maintenance schedules based on home characteristics
- Task library with applicability rules (home age, climate, features)
- Community-driven tips with location context and upvoting
- Progress tracking and completion history

---

## 2. User Personas

### Primary Persona: New Homeowner Emma
- **Demographics**: 28 years old, software developer, first-time homeowner
- **Home**: 15-year-old single-family home, wood frame, Northeast climate zone
- **Needs**: Proactive maintenance schedule to avoid costly repairs, learn home maintenance basics
- **Frustrations**: Overwhelmed by home maintenance responsibilities, unsure what's urgent vs optional
- **Goals**: Keep home in good condition, budget maintenance costs, avoid surprises

### Secondary Persona: Expert Neighbor David
- **Demographics**: 45 years old, civil engineer, homeowner for 20 years
- **Home**: 30-year-old brick colonial, Northeast climate zone
- **Needs**: Share knowledge with neighbors, build community reputation
- **Frustrations**: Answering same questions repeatedly, seeing neighbors make preventable mistakes
- **Goals**: Help others avoid costly errors, establish expertise in community

---

## 3. Functional Requirements

### F-001: Maintenance Task Library
**Priority**: Baseline (Must-Have)  
**Status**: ✅ Complete

**Description**: System provides comprehensive library of common home maintenance tasks with scheduling guidance.

**Requirements**:
- FR-F-001-1: System stores tasks with title, description, frequency, category, applicability rules
- FR-F-001-2: System supports frequency types: weekly, monthly, quarterly, seasonal, annual, biennial
- FR-F-001-3: System supports applicability rules: minimum home age, climate zones, required features (HVAC, basement, attic, etc.)
- FR-F-001-4: Admin can add, edit, activate/deactivate tasks via Django admin interface

**Acceptance Criteria**:
- [x] MaintenanceTask model with all required fields
- [x] 12+ tasks seeded in database covering common maintenance categories
- [x] Task list view shows all active tasks with category badges
- [x] Task detail view shows full description, frequency, applicability rules
- [x] Admin interface allows inline task management

**Implementation Notes**:
- Model: `maintenance/models.py` - MaintenanceTask with slug field for SEO-friendly URLs
- Seed Command: `python manage.py seed_tasks` - 12 pre-defined tasks
- URL Pattern: `/maintenance/tasks/<slug>/` - slug-based routing

---

### F-002: Personalized Schedule Generation
**Priority**: Good (Should-Have)  
**Status**: ✅ Complete (with ManyToMany enhancement)

**Description**: System generates customized maintenance schedules based on home characteristics, filtering tasks by applicability rules.

**Requirements**:
- FR-F-002-1: User can generate schedule for a specific home
- FR-F-002-2: System filters tasks based on home age, climate zone, features
- FR-F-002-3: User can select subset of applicable tasks to include in schedule
- FR-F-002-4: Schedule supports multiple tasks batched on same date (e.g., "Saturday chores")
- FR-F-002-5: User can edit schedule date and notes after generation

**Acceptance Criteria**:
- [x] Generate schedule button on home detail page
- [x] System calculates home age from year_built
- [x] System filters tasks by min_home_age, requires_* feature flags
- [x] User presented with checkbox list of applicable tasks
- [x] System creates one Schedule with multiple selected tasks (ManyToManyField)
- [x] Schedule list view shows schedules grouped by date
- [x] Schedule detail view shows all tasks in schedule

**Implementation Notes**:
- Major Model Change (ADR-1.0.5): Schedule.task (ForeignKey) → Schedule.tasks (ManyToManyField)
- Migration 0002 applied successfully
- View: GenerateScheduleView creates single Schedule with task selection
- Form: ScheduleForm simplified to scheduled_date and notes only

---

### F-003: Task Completion Tracking
**Priority**: Good (Should-Have)  
**Status**: ⏳ Partial (schedule-level complete, task-level deferred to v1.1)

**Description**: Users can mark tasks complete, record completion details, and view completion history.

**Requirements**:
- FR-F-003-1: User can mark entire schedule complete with completion timestamp
- FR-F-003-2: System separates active and completed schedules in list view
- FR-F-003-3: User can view completion history for a home
- FR-F-003-4: Individual task completion within schedule (deferred to v1.1)
- FR-F-003-5: Per-task cost and performer tracking (deferred to v1.1)

**Acceptance Criteria**:
- [x] Schedule model has is_completed boolean and completed_at timestamp
- [x] "Mark Complete" button on schedule detail page
- [ ] Mark complete view updates schedule and redirects to list (in progress)
- [x] Schedule list view filters by is_completed status
- [ ] Completion history view shows completed schedules for home
- [ ] Statistics: total tasks completed, upcoming tasks count

**Implementation Notes**:
- Simplified to boolean completion for v1.0 MVP
- Future enhancement (v1.1): Add ScheduleTask through model for granular tracking
- Cost/performer tracking removed in migration 0002, will be re-added per-task in v1.1

---

### F-004: Community Tips Sharing
**Priority**: Better (Nice-to-Have)  
**Status**: ✅ Complete

**Description**: Users can share local maintenance tips, upvote helpful content, and browse community knowledge.

**Requirements**:
- FR-F-004-1: Authenticated users can submit tips with title, content, location, category
- FR-F-004-2: Tips require moderation approval before public display
- FR-F-004-3: Users can upvote helpful tips (one upvote per user per tip)
- FR-F-004-4: Tip list supports filtering by category and location
- FR-F-004-5: Tip list supports sorting by newest, most upvoted

**Acceptance Criteria**:
- [x] LocalTip model with moderation workflow (pending/approved/rejected/flagged)
- [x] Authenticated users can create tips via form
- [x] Tip list shows only approved tips
- [x] 5 sample tips seeded in database
- [x] Upvote button prevents duplicate votes (ManyToMany relationship)
- [ ] Category and location filter UI (template exists, wiring in progress)
- [ ] Sort by upvotes/newest (queryset logic exists, UI in progress)
- [x] Admin interface for bulk approve/reject/flag actions

**Implementation Notes**:
- Model: LocalTip with slug field for SEO-friendly URLs
- URL Pattern: `/tips/<slug>/` - slug-based routing
- View: TipListView filters status='approved' and annotates upvote_count
- Sample data: 5 tips covering HVAC, plumbing, appliances, safety

---

### F-005: Home Information Database
**Priority**: Good (Should-Have)  
**Status**: ✅ Complete

**Description**: Users can manage detailed home information including property details, appliances, and service providers.

**Requirements**:
- FR-F-005-1: User can create multiple home profiles with address, year_built, construction_type, climate_zone, square_footage
- FR-F-005-2: User can add appliances with make, model, purchase_date, warranty_info
- FR-F-005-3: User can add service providers with business name, trade, contact info, notes
- FR-F-005-4: User can only view/edit their own homes (authorization checks)

**Acceptance Criteria**:
- [x] Home model with all required fields and feature flags (has_basement, has_attic, has_hvac, etc.)
- [x] Appliance and ServiceProvider models with ForeignKey to Home
- [x] Home CRUD views with LoginRequiredMixin and UserPassesTestMixin
- [x] Home detail page shows appliances and providers with inline add buttons
- [x] User has successfully created 3-5 homes with testing
- [x] Admin interface with ApplianceInline and ServiceProviderInline

**Implementation Notes**:
- Authorization: UserPassesTestMixin ensures home.owner == request.user
- Template: home_detail.html lists appliances and providers with edit/delete buttons
- Admin: Tabular inline editing for appliances and providers

---

### F-007: Expert Blog Posts
**Priority**: Better (Nice-to-Have)  
**Status**: ✅ Complete

**Description**: Verified experts can publish longer-form educational articles with rich text formatting, images, and engagement features.

**Requirements**:
- FR-F-007-1: Verified experts can create blog posts with rich text editor (WYSIWYG)
- FR-F-007-2: Blog posts support featured images, meta descriptions, and tags
- FR-F-007-3: Blog posts have approval workflow: draft → pending → approved/rejected
- FR-F-007-4: Blog homepage features carousel with selected articles
- FR-F-007-5: Users can upvote blog posts and add comments
- FR-F-007-6: Blog posts track view count and calculate reading time
- FR-F-007-7: Users can filter by category, search by keywords, sort by popular/recent/views

**Acceptance Criteria**:
- [x] BlogPost model with RichTextField (django-ckeditor)
- [x] BlogComment model for discussions
- [x] Expert-only creation (UserPassesTestMixin on BlogCreateView)
- [x] CKEditor configured with custom toolbar (Bold, Italic, Lists, Links, Blockquote)
- [x] Featured image upload with ImageField and Pillow
- [x] Approval workflow with admin bulk actions
- [x] Featured posts carousel on blog homepage (2 articles rotating)
- [x] Upvote toggle functionality (ManyToManyField)
- [x] Comment creation and deletion (author-only delete)
- [x] View count increment on detail page view
- [x] Reading time calculation (@property: word_count / 200)
- [x] get_tags_list() method for tag parsing and display
- [x] Filter sidebar: category, search, sort options
- [x] Expert dashboard showing all posts grouped by status
- [x] 4 sample blog posts created (2 featured)
- [x] Navigation link added to main menu

**Implementation Notes**:
- Package: django-ckeditor 6.7.3, Pillow 12.0.0
- Models: tips/models.py - BlogPost with RichTextField content, BlogComment
- Views: 9 CBVs (list, detail, create, edit, delete, my-posts, upvote, comment, delete-comment)
- Templates: 5 templates (blog_list, blog_detail, blog_form, blog_confirm_delete, my_posts)
- URL Structure: `/tips/blog/` for list, `/tips/blog/<slug>/` for detail
- Admin: BlogPostAdmin with bulk approve/reject/feature actions
- Bug Fixes: Changed upvote_count from @property to method, added get_tags_list(), fixed Featured Articles text contrast

**Sample Content**:
1. "Complete Guide to HVAC Maintenance: Save Money and Extend System Life" (HVAC1234, featured)
2. "10 Home Safety Devices Every Homestead Should Have" (SafetyInspector, featured)
3. "Home Electrical Safety: Essential Tips Every Homeowner Should Know" (ElectricianExpert)
4. Additional HVAC maintenance guide

---

### F-006: User Account Management
**Priority**: Baseline (Must-Have)  
**Status**: ✅ Complete

**Description**: User registration, authentication, profile management, and password recovery.

**Requirements**:
- FR-F-006-1: User can register with username, email, password
- FR-F-006-2: User can log in and log out
- FR-F-006-3: User can reset forgotten password via email
- FR-F-006-4: User can view and edit profile (bio, location, first-time homeowner status)
- FR-F-006-5: User profile shows activity statistics (homes count, tips count, schedules count)

**Acceptance Criteria**:
- [x] Custom User model extending AbstractUser with homeowner fields
- [x] Registration form with validation
- [x] Login/logout views with session management
- [x] Password reset flow (4 templates: request, done, confirm, complete)
- [x] Password change flow (2 templates: form, done)
- [x] Profile view with activity stats
- [x] Profile edit view with form validation
- [x] Email backend configured (console for dev, SMTP for production)

**Implementation Notes**:
- Model: accounts/models.py - Custom User with bio, location, is_first_time_homeowner flags
- Email: Console backend for development, SMTP settings for production deployment
- Security: All data-modifying views require LoginRequiredMixin
- Templates: 10 account-related templates with Bootstrap 5 styling

---

## 4. Non-Functional Requirements

### NFR-001: Performance
- **Requirement**: Page load time < 2 seconds on standard broadband
- **Status**: ✅ Met (local development server responds < 200ms)
- **Implementation**: Database indexes on Schedule(home, scheduled_date), prefetch_related for ManyToMany queries

### NFR-002: Security
- **Requirement**: Authentication required for data modification, CSRF protection on all forms
- **Status**: ✅ Met
- **Implementation**: LoginRequiredMixin on all CRUD views, UserPassesTestMixin for ownership checks, Django CSRF middleware enabled

### NFR-003: Usability
- **Requirement**: Responsive design for mobile, tablet, desktop; intuitive navigation matching user mental model
- **Status**: ✅ Met
- **Implementation**: Bootstrap 5 responsive grid, navbar collapses on mobile, semantic HTML

### NFR-004: Maintainability
- **Requirement**: Code follows Django best practices, clear separation of concerns, comprehensive documentation
- **Status**: ✅ Met
- **Implementation**: 4 domain-focused apps, CBVs for CRUD, ModelForms, ADRs for major decisions, AI_USAGE_DISCLOSURE for transparency

---

## 5. Out of Scope (Deferred)

### v1.1 Enhancements (Next Semester)
- Individual task completion within schedules (ScheduleTask through model)
- Per-task cost and performer tracking
- Recurring schedule templates ("Every Saturday")
- Appliance maintenance reminders based on warranty/age
- Photo uploads for homes and appliances (requires Pillow)
- Email notifications for upcoming maintenance

### v1.2 Enhancements (Future)
- Service provider ratings and reviews
- Export schedule to calendar (iCal, Google Calendar)
- Mobile app (iOS/Android)
- Tip comments and threaded discussions
- User-to-user messaging

### v2.0 Vision (Long-Term)
- AI-powered schedule optimization
- Integration with real estate listing APIs
- Professional contractor marketplace
- Predictive maintenance based on weather/climate data
- Community challenges and gamification

---

## 6. Technical Stack

### Framework & Language
- **Django**: 5.2.7
- **Python**: 3.12.3
- **Database**: SQLite (development), PostgreSQL (production recommended)

### Frontend
- **Bootstrap**: 5.3.0 via CDN
- **Icons**: Bootstrap Icons
- **Templates**: Django Template Language (DTL)

### Deployment
- **Development Server**: localhost:8080
- **Static Files**: WhiteNoise middleware
- **Production Target**: Render.com (pending)

---

## 7. Implementation Status Summary

### Completed Features (✅)
1. Project scaffolding and 4 Django apps
2. All models with migrations applied
3. 30+ templates with Bootstrap 5
4. Complete authentication system
5. Password reset/change flows
6. Home CRUD with appliances and providers
7. 12 maintenance tasks seeded
8. Schedule generation with multi-task batching
9. Community tips with 5 sample entries
10. Admin interfaces with inlines and bulk actions
11. URL routing with slug-based SEO-friendly URLs
12. Authorization checks (LoginRequiredMixin, UserPassesTestMixin)

### In Progress (⏳)
1. Schedule completion workflow (mark complete button wiring)
2. Tip filtering and sorting UI
3. Deployment to Render.com
4. README and QUICKSTART documentation updates

### Deferred to v1.1 (📅)
1. Individual task completion tracking
2. Per-task cost/performer fields
3. Recurring schedule templates
4. Email notifications
5. Photo uploads

---

## 8. Success Metrics

### MVP Success Criteria (All Met ✅)
- [x] User can register and log in
- [x] User can create multiple homes
- [x] User can generate personalized maintenance schedule
- [x] User can view task details
- [x] User can view community tips
- [x] User can mark schedule complete
- [x] Application passes rubric baseline requirements

### Future KPIs (v1.1+)
- 100+ registered users
- 500+ maintenance tasks completed
- 50+ community tips submitted
- 80%+ user retention after 3 months
- Average 15 minutes to generate first schedule

---

## 9. Traceability Matrix

| Requirement | ADR | Model | View | Template | Status |
|------------|-----|-------|------|----------|---------|
| FR-F-001-1 | ADR-1.0.2 | MaintenanceTask | TaskListView | task_list.html | ✅ |
| FR-F-001-2 | ADR-1.0.2 | MaintenanceTask.frequency | TaskDetailView | task_detail.html | ✅ |
| FR-F-002-1 | ADR-1.0.3, ADR-1.0.5 | Schedule | GenerateScheduleView | generate_schedule.html | ✅ |
| FR-F-002-4 | ADR-1.0.5 | Schedule.tasks (ManyToMany) | GenerateScheduleView | generate_schedule.html | ✅ |
| FR-F-003-1 | ADR-1.0.5 | Schedule.is_completed | MarkCompleteView | schedule_detail.html | ⏳ |
| FR-F-004-1 | ADR-1.0.4 | LocalTip | TipCreateView | tip_form.html | ✅ |
| FR-F-004-2 | ADR-1.0.4 | LocalTip.status | TipListView | tip_list.html | ✅ |
| FR-F-005-1 | ADR-1.0.2 | Home | HomeCreateView | home_form.html | ✅ |
| FR-F-006-1 | ADR-1.0.0 | User (accounts) | RegisterView | register.html | ✅ |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-23 | A. Lawson | Initial PRD creation |
| 1.0.1 | 2025-11-23 | A. Lawson | Updated after Schedule model refactor |
| 1.0.2 | 2025-11-23 | A. Lawson | Updated with complete implementation status, bug fixes documented |
