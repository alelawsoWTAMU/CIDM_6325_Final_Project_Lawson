# Product Requirements Document

## 1. Document information

- Product or feature name: Homestead Compass
- Author(s): Alexander J Lawson
- Date created: 2025-09-21
- Last updated: 2025-11-23
- Version: 1.0.1

---

## 2. Overview

- **Summary**: Homestead Compass is a web application designed to assist first-time homeowners in creating personalized preventative maintenance schedules while providing access to verified, localized knowledge from nearby experts. The application empowers new homeowners to adopt a proactive approach to home maintenance, reducing stress and costly repairs through organized planning and community-driven resources.

- **Problem statement**: New homeowners, particularly Millennials and Gen Z first-time buyers, face two critical challenges: (1) they are overwhelmed by home maintenance responsibilities, leading to reactive "whack-a-mole" crisis management, and (2) they receive generic advice from internet strangers that is not tailored to their specific situations, home characteristics, or local climate conditions.

- **Goals and objectives**:
  - Empower first-time homeowners to adopt a proactive approach to home maintenance
  - Provide methodical, personalized maintenance schedules based on specific home circumstances
  - Create a community-driven knowledge base for localized tips and advice
  - Reduce the likelihood of costly and stressful home repairs caused by neglect
  - Lower insurance claims volume related to maintenance neglect

- **Non-goals**: The initial version (MVP) will not include automated parts ordering or e-commerce integration, appliance replacement recommendations based on environmental factors, professional contractor bidding or scheduling services, smart home device integration, or AI-driven diagnostics for maintenance issues.

---

## 3. Context and background

- **Business context**: This product aligns with the goal of fostering preventative home maintenance culture, with the additional benefit of reducing insurance claims related to neglect. This initiative would lower the volume of potential claims for both customers and insurance providers, creating a win-win scenario.

- **Market or customer insights**: 
  - **Target Persona**: First-time homeowners, particularly Millennials and Gen Z generations (digitally savvy, practical home maintenance knowledge gap)
  - **2022 Thumbtack Survey**: 80% of millennial homeowners and 81% of first-time buyers felt overwhelmed or stressed about home upkeep
  - **May 2025 Kin Insurance Report**: 72% of Gen-Z and millennial first-time homebuyers encountered unexpected issues after moving in, at an average cost of over $5,000
  - **Key Pain Points**: 
    - Feelings of being blindsided by practical realities of home maintenance
    - Anxiety about financial solvency if something breaks
    - Concern about appearing incompetent when pursuing repairs
    - Lack of mentorship in "Homeownership 101"
    - Scattered and unverified information sources

- **Competitive or benchmark references**: While general home maintenance apps exist (HomeZada, BrightNest), they lack personalized scheduling algorithms based on home characteristics and localized community-driven knowledge bases. This product differentiates through hyper-personalization and community verification.

---

## 4. Scope items and checklist seeds

- [ ] **F-001 Personalized Maintenance Schedule Generator**  
  **User story**: As a new homeowner, I want a personalized maintenance schedule generated from my home's specific characteristics, so that I know what tasks I need to do and when to do them.  
  **Acceptance notes**:
  - AC1: System accepts user inputs (home age, construction type, climate zone, appliance details, features like basement/attic/HVAC)
  - AC2: Algorithm generates a schedule with weekly, monthly, seasonal, and annual tasks within 3 seconds
  - AC3: Schedule is filterable by frequency, category, and priority
  - AC4: Schedule adapts based on home-specific features (e.g., no gutter cleaning for homes without gutters)
  **Artifacts**: `maintenance/views.py` (GenerateScheduleView), `maintenance/models.py` (Schedule, MaintenanceTask), templates in `templates/maintenance/`  
  **Owner**: Development Team  
  **Target version**: MVP 1.0

- [ ] **F-002 Maintenance Task Profiles with Guides**  
  **User story**: As a DIY enthusiast, I want step-by-step guides for common tasks with tool lists and time estimates, so that I can confidently complete them myself.  
  **Acceptance notes**:
  - AC1: Each maintenance task includes detailed description, step-by-step instructions, required tools list, estimated time, difficulty level, and safety notes
  - AC2: Task profiles cover 10-15 common maintenance items at MVP launch (HVAC filter changes, gutter cleaning, smoke detector testing, etc.)
  - AC3: Tasks are searchable and browsable by category, difficulty, and season
  - AC4: System admits limitations when unable to provide confident guidance for obscure scenarios
  **Artifacts**: `maintenance/models.py` (MaintenanceTask model with all required fields), `maintenance/admin.py` (content management), seed data in `maintenance/management/commands/seed_tasks.py`  
  **Owner**: Development Team + Content Team  
  **Target version**: MVP 1.0

- [ ] **F-003 Localized Community Tips Module**  
  **User story**: As a local community member, I want to submit and upvote useful tips tied to my geographic area, so that I can share my knowledge and benefit from others' experiences.  
  **Acceptance notes**:
  - AC1: Users can submit tips with title, content, category, and location (city/region)
  - AC2: Tips support upvoting/downvoting functionality
  - AC3: Tips are filterable by location, category, and popularity
  - AC4: Tip detail pages show view count, author, submission date, and user comments
  **Artifacts**: `tips/models.py` (LocalTip, TipComment models), `tips/views.py` (CRUD views + upvote functionality), `tips/forms.py`  
  **Owner**: Development Team  
  **Target version**: MVP 1.0

- [ ] **F-004 Content Moderation System**  
  **User story**: As a content moderator, I want tools to review, approve, reject, and flag community-submitted tips, so that users receive quality advice and avoid liability issues.  
  **Acceptance notes**:
  - AC1: All submitted tips enter "pending" status and require moderator approval
  - AC2: Moderators can approve, reject, or flag tips for further review
  - AC3: Admin interface provides bulk actions for moderation workflow
  - AC4: Users can report tips for review (TipReport model)
  - AC5: System displays prominent disclaimer on all crowd-sourced content advising professional consultation
  **Artifacts**: `tips/models.py` (TipReport model, status fields), `tips/admin.py` (bulk actions), disclaimer in `templates/tips/`  
  **Owner**: Development Team  
  **Target version**: MVP 1.0

- [ ] **F-005 Home Information Database**  
  **User story**: As a homeowner, I want a simple digital interface to log and retrieve key home information and trusted service provider contacts, so that I have everything organized in one place.  
  **Acceptance notes**:
  - AC1: Users can create multiple home profiles with detailed information (address, year built, construction type, climate zone, square footage, features)
  - AC2: Each home supports adding multiple appliances (type, manufacturer, model, installation year, warranty expiration)
  - AC3: Each home supports adding multiple service providers (name, company, specialty, phone, email, notes)
  - AC4: Interface provides simple CRUD operations for homes, appliances, and service providers
  **Artifacts**: `homes/models.py` (Home, Appliance, ServiceProvider models), `homes/views.py` (CBVs for CRUD), `homes/admin.py` (with inlines)  
  **Owner**: Development Team  
  **Target version**: MVP 1.0

- [ ] **F-006 Task Completion Tracking**  
  **User story**: As a homeowner, I want to mark scheduled tasks as complete and log notes about the work performed, so that I maintain a history of maintenance activities.  
  **Acceptance notes**:
  - AC1: Users can mark scheduled tasks as complete from their schedule view
  - AC2: Completion form captures date completed, notes, cost, time spent, and satisfaction rating
  - AC3: Completed tasks display in maintenance history with filters by date range and task type
  - AC4: Completion history is tied to specific home profiles
  **Artifacts**: `maintenance/models.py` (TaskCompletion model), `maintenance/views.py` (completion views), `maintenance/forms.py`  
  **Owner**: Development Team  
  **Target version**: MVP 1.0

**Out of scope**:
- Automated ordering of products, parts, or services
- E-commerce integration or affiliate marketing
- Professional contractor bidding platform
- Appointment scheduling with service providers
- Smart home device integration or IoT connectivity
- AI-driven diagnostics beyond rule-based schedule generation
- Mobile native applications (web-responsive only for MVP)

---

## 5. Functional requirements bound to scope

### Schedule Generation (F-001)

- **FR-F-001-1**: System must accept user inputs for home age (year built), construction type (wood frame, brick, concrete, manufactured), climate zone (Northeast, Southeast, Midwest, Southwest, Northwest, Alaska, Hawaii, Tropical), and home features (basement, attic, garage, HVAC system, fireplace, swimming pool, well water, septic system).  
  **Rationale**: These parameters are the minimum required to generate meaningful, personalized schedules.  
  **Trace**: F-001

- **FR-F-001-2**: System must filter maintenance tasks based on applicability rules (e.g., minimum home age requirements, required features) and generate Schedule instances linked to the user's Home.  
  **Rationale**: Prevents irrelevant tasks from cluttering user schedules (e.g., no septic maintenance for homes on city sewer).  
  **Trace**: F-001

- **FR-F-001-3**: System must calculate next scheduled date for each task based on frequency (weekly, monthly, quarterly, seasonal, annual) starting from generation date.  
  **Rationale**: Provides actionable timeline for users to follow.  
  **Trace**: F-001

### Task Profiles (F-002)

- **FR-F-002-1**: MaintenanceTask model must include fields for title, description, detailed instructions, category (HVAC, plumbing, electrical, exterior, interior, appliances, safety, seasonal), frequency, estimated time, difficulty level, required tools list, safety notes, and applicability rules (minimum home age, required features).  
  **Rationale**: Comprehensive task information empowers users to perform maintenance confidently.  
  **Trace**: F-002

- **FR-F-002-2**: System must provide at minimum 10 pre-seeded maintenance tasks covering common home systems at MVP launch.  
  **Rationale**: Provides immediate value to users without requiring community contribution buildup.  
  **Trace**: F-002

- **FR-F-002-3**: Admin interface must allow content administrators to create, update, deactivate, and manage maintenance tasks with full field editing.  
  **Rationale**: Enables ongoing content expansion and quality control.  
  **Trace**: F-002

### Community Tips (F-003)

- **FR-F-003-1**: LocalTip model must include fields for title, content, category, location (city/region), author, status (pending/approved/rejected), publication date, view count, and ManyToMany relationship for upvotes.  
  **Rationale**: Supports rich community-driven knowledge base with engagement metrics.  
  **Trace**: F-003

- **FR-F-003-2**: System must provide upvote functionality that increments upvote count and prevents duplicate votes from same user.  
  **Rationale**: Surfaces high-quality tips through community validation.  
  **Trace**: F-003

- **FR-F-003-3**: System must support commenting on tips with TipComment model (author, content, timestamp).  
  **Rationale**: Enables community discussion and elaboration on tips.  
  **Trace**: F-003

### Content Moderation (F-004)

- **FR-F-004-1**: All newly submitted LocalTips must default to "pending" status and not be visible to public until moderator approval.  
  **Rationale**: Prevents bad advice from reaching users and mitigates liability.  
  **Trace**: F-004

- **FR-F-004-2**: Admin interface must provide bulk actions for moderators to approve, reject, or flag multiple tips simultaneously.  
  **Rationale**: Streamlines moderation workflow for efficiency.  
  **Trace**: F-004

- **FR-F-004-3**: System must provide TipReport model allowing users to flag tips for moderator review with reason field.  
  **Rationale**: Crowd-sources quality control by empowering users to identify problematic content.  
  **Trace**: F-004

- **FR-F-004-4**: All tip display templates must prominently show disclaimer text: "Tips are user-generated content. Always consult a licensed professional before performing home repairs or maintenance tasks."  
  **Rationale**: Legal liability protection through clear user expectations.  
  **Trace**: F-004

### Home Database (F-005)

- **FR-F-005-1**: Home model must support fields for name, address, year built, construction type, climate zone, square footage, number of bedrooms/bathrooms, and boolean flags for features (has_basement, has_attic, has_garage, has_hvac, has_fireplace, has_pool, has_well, has_septic).  
  **Rationale**: Captures home characteristics needed for schedule personalization.  
  **Trace**: F-005

- **FR-F-005-2**: Appliance model must support fields for home (FK), appliance type, manufacturer, model number, year installed, warranty expiration date, and purchase price.  
  **Rationale**: Tracks appliance lifecycle for maintenance and replacement planning.  
  **Trace**: F-005

- **FR-F-005-3**: ServiceProvider model must support fields for home (FK), name, company, specialty, phone, email, website, address, and notes.  
  **Rationale**: Centralizes trusted contractor contact information.  
  **Trace**: F-005

### Task Completion (F-006)

- **FR-F-006-1**: TaskCompletion model must include fields for schedule (FK), completed date, notes, cost, time spent, completed by (FK to User), and satisfaction rating (1-5 stars).  
  **Rationale**: Creates comprehensive maintenance history for homeowner records.  
  **Trace**: F-006

- **FR-F-006-2**: Schedule model must include `is_completed` boolean flag that updates when TaskCompletion record is created.  
  **Rationale**: Prevents duplicate completions and tracks schedule progress.  
  **Trace**: F-006

---

## 6. Checklist to be generated from scope

At PRD sign-off, generate a checklist including:
- Completion boxes for F-001 through F-006
- User story statements
- Acceptance criteria lists
- Links to code artifacts (models.py, views.py, forms.py, admin.py, templates)
- Test status flags and dates

Save as: `docs/checklists/home_maintenance_compass_feature_checklist.md`

---

## 7. Non functional requirements

- **NF-001 Performance**: Target response time of ≤3 seconds for schedule generation from user input submission to schedule display. Verified through load testing with sample datasets of 100+ tasks and automated response time monitoring.

- **NF-002 Scalability**: Architecture must support 1,000 concurrent users at MVP launch with capacity to scale to 10,000+ users. Database queries must use indexing on frequently filtered fields (home, scheduled_date, status). Verified through load testing with Django Debug Toolbar and database query analysis.

- **NF-003 Accessibility**: Application must achieve WCAG 2.1 Level AA compliance for web accessibility. Verified through automated testing (axe DevTools, Lighthouse) and manual keyboard navigation testing.

- **NF-004 Security**: 
  - All user inputs must be validated and sanitized to prevent SQL injection, XSS, and CSRF attacks
  - Django's built-in security features must be enabled (CSRF tokens, password hashing, SQL parameterization)
  - User authentication required for all data modification operations
  - Sensitive data (emails, addresses) must be protected with appropriate access controls
  - Verified through security audit and penetration testing

- **NF-005 Reliability**: Application must maintain 99% uptime during business hours (6 AM - 10 PM local time). Database backups must occur daily. Error handling must gracefully manage failures and provide user-friendly error messages. Verified through uptime monitoring and error logging analysis.

- **NF-006 Usability**: Application must achieve >80% Task Completion Rate (users marking scheduled tasks complete within defined timeframe). Navigation must be intuitive with ≤3 clicks to reach any feature. Verified through user acceptance testing and analytics tracking.

---

## 8. Dependencies

- **Internal system dependencies**:
  - Django 5.x web framework for application architecture
  - SQLite database for MVP (PostgreSQL for production)
  - Django ORM for data access layer
  - Django authentication system for user management
  - Django admin for content management interface

- **External APIs or third party services**:
  - None required for MVP
  - Future consideration: Google Maps API for location services, weather APIs for climate-specific scheduling

- **Cross team deliverables**:
  - Content team: Initial 10-15 maintenance task guides with instructions, tools, and safety notes
  - Legal team: Review of disclaimer language for liability protection
  - Design team: UI/UX wireframes and responsive design assets

---

## 9. Risks and assumptions

**Risks**:

- **Risk 1**: Schedule generation algorithm becomes too complex or produces ineffective schedules.  
  **Mitigation**: Start with simple rule-based filtering for MVP. Use common home characteristics (age ranges: <5 years, 5-15 years, 15-30 years, >30 years). Implement dynamic, flexible design allowing future complexity. Conduct user testing with diverse home profiles to validate schedule quality.

- **Risk 2**: Lackluster community participation results in low-quality or low-volume localized tips.  
  **Mitigation**: Seed database with 20-30 high-quality tips gathered from trusted sources (This Old House, Bob Vila, local extension offices). Incentivize early adopters through gamification (badges, leaderboards). Partner with local home improvement stores or real estate agents to promote community contribution.

- **Risk 3**: Legal liability if a user attempts DIY task based on tip and causes damage or injury.  
  **Mitigation**: Implement prominent, clear disclaimer on all crowd-sourced content. Require users to acknowledge disclaimer before viewing tips. Include "Consult a professional" advisory on all task guides. Moderate all content before publication. Secure appropriate liability insurance. Consult legal counsel on terms of service.

- **Risk 4**: User privacy concerns related to storing detailed home information and location data.  
  **Mitigation**: Implement strong data encryption for sensitive fields. Provide clear privacy policy explaining data usage. Allow users to control data sharing settings. Comply with GDPR/CCPA regulations. Conduct regular security audits.

**Assumptions**:

- Users will be willing to provide detailed information about their homes (age, construction type, features) to generate personalized schedules
- A community of experienced homeowners and contractors will contribute tips to the localized knowledge base
- Users prefer web-based access over native mobile apps for MVP
- Basic rule-based filtering is sufficient for MVP schedule generation (vs. machine learning)
- Homeowners value proactive maintenance education over reactive crisis management tools

---

## 10. Acceptance criteria

The MVP will be accepted when:

- **AC-1**: A user can register an account, log in, create a home profile with detailed characteristics, and generate a personalized maintenance schedule based on those inputs within 3 seconds (FR-F-001-1, FR-F-001-2, FR-F-001-3)

- **AC-2**: The generated schedule includes at least 8-12 tasks appropriate to the home's characteristics, with irrelevant tasks filtered out (e.g., no septic maintenance for homes on city sewer) (FR-F-001-2)

- **AC-3**: Each maintenance task profile contains detailed instructions, required tools list, estimated time, difficulty level, and safety notes (FR-F-002-1)

- **AC-4**: At least 10 pre-seeded maintenance tasks are available in the system covering common categories: HVAC, plumbing, electrical, exterior, interior, appliances, safety, and seasonal (FR-F-002-2)

- **AC-5**: Users can submit tips with title, content, category, and location. Submitted tips enter "pending" status and require moderator approval before public visibility (FR-F-003-1, FR-F-004-1)

- **AC-6**: Users can upvote tips, and the system prevents duplicate votes from the same user. Tips display upvote count and view count (FR-F-003-2)

- **AC-7**: Admin interface provides bulk actions for moderators to approve, reject, or flag multiple tips simultaneously (FR-F-004-2)

- **AC-8**: All tip display pages show prominent disclaimer: "Tips are user-generated content. Always consult a licensed professional before performing home repairs or maintenance tasks." (FR-F-004-4)

- **AC-9**: Users can add multiple appliances and service providers to each home profile with full CRUD functionality (FR-F-005-2, FR-F-005-3)

- **AC-10**: Users can mark scheduled tasks as complete with optional notes, cost, time spent, and satisfaction rating. Completed tasks display in maintenance history (FR-F-006-1, FR-F-006-2)

- **AC-11**: Application achieves <3 second response time for schedule generation and task browsing (NF-001)

- **AC-12**: Application passes automated accessibility testing with WCAG 2.1 Level AA compliance (NF-003)

---

## 11. Success metrics

- **Task Completion Rate**: Target ≥60% of users mark scheduled maintenance tasks as "complete" within defined timeframe (e.g., within 7 days of scheduled date for weekly tasks). Measured through TaskCompletion model analytics and user engagement tracking.

- **Knowledge Acquisition**: Target average session duration ≥5 minutes viewing task profiles and localized tips. Measured through view count increments and analytics tracking.

- **Community Engagement**: Target ≥50 unique tips submitted within first 3 months post-launch, with ≥100 total upvotes across all tips. Measured through LocalTip and upvote tracking.

- **User Retention**: Target ≥40% of registered users return to the application within 30 days of initial registration. Target ≥20% Monthly Active Users (MAU) ratio. Measured through login tracking and cohort analysis.

- **Schedule Generation Adoption**: Target ≥80% of registered users generate at least one maintenance schedule within 7 days of account creation. Measured through Schedule model creation tracking.

- **User Satisfaction**: Target ≥4.0 average satisfaction rating (out of 5 stars) on completed task feedback. Measured through TaskCompletion.satisfaction_rating aggregation.

---

## 12. Rollout and release plan

**Phasing**:

- **MVP 1.0** (Target: Current Development Cycle):
  - F-001: Personalized maintenance schedule generator
  - F-002: Maintenance task profiles (minimum 10-15 tasks)
  - F-003: Localized community tips module with upvoting
  - F-004: Content moderation system
  - F-005: Home information database (homes, appliances, service providers)
  - F-006: Task completion tracking
  - User authentication and profile management
  - Responsive web interface with Bootstrap 5
  - SQLite database for development

- **Version 1.1** (Target: 3 months post-MVP):
  - Expand maintenance task library to 30-50 tasks
  - Email notifications for upcoming scheduled tasks
  - Enhanced filtering and search for tasks and tips
  - User dashboard with maintenance calendar view
  - PostgreSQL migration for production scalability

- **Version 1.2** (Target: 6 months post-MVP):
  - Weather API integration for seasonal task scheduling
  - Photo upload for task completion documentation
  - Appliance maintenance history and lifecycle tracking
  - Service provider ratings and reviews
  - Mobile-responsive enhancements

- **Version 2.0** (Target: 12 months post-MVP):
  - Native mobile applications (iOS, Android)
  - Smart home integration (thermostat data, security systems)
  - Predictive maintenance scheduling based on usage patterns
  - Marketplace for recommended products and services
  - Advanced analytics dashboard for homeowners

**Release channels**:
- **Alpha**: Internal development team testing (Current)
- **Beta**: Invite-only early adopter program (50-100 users for 4-6 weeks)
- **Staged Rollout**: Gradual public availability by geographic region
- **General Availability**: Full public launch after successful staged rollout

**Training and documentation**:
- Internal documentation: Developer README, API documentation, deployment guides
- User documentation: In-app help tooltips, FAQ page, video tutorials for common tasks
- Support resources: Email support address, community forum for user questions
- Moderator training: Content moderation guidelines, admin interface training materials

---

## 13. Traceability

| Scope Item | Functional Requirements | Code Artifacts | Test Coverage |
|------------|------------------------|----------------|---------------|
| F-001 Schedule Generation | FR-F-001-1, FR-F-001-2, FR-F-001-3 | `maintenance/views.py` (GenerateScheduleView), `maintenance/models.py` (Schedule, MaintenanceTask), `templates/maintenance/generate_schedule.html` | T-001a (input validation), T-001b (schedule generation logic), T-001c (applicability filtering) |
| F-002 Task Profiles | FR-F-002-1, FR-F-002-2, FR-F-002-3 | `maintenance/models.py` (MaintenanceTask with all fields), `maintenance/admin.py` (TaskAdmin), `maintenance/management/commands/seed_tasks.py` | T-002a (model fields), T-002b (admin CRUD), T-002c (seed data) |
| F-003 Community Tips | FR-F-003-1, FR-F-003-2, FR-F-003-3 | `tips/models.py` (LocalTip, TipComment), `tips/views.py` (CRUD + upvote views), `tips/forms.py` | T-003a (tip submission), T-003b (upvote logic), T-003c (comment threading) |
| F-004 Content Moderation | FR-F-004-1, FR-F-004-2, FR-F-004-3, FR-F-004-4 | `tips/models.py` (TipReport, status workflow), `tips/admin.py` (bulk actions), disclaimer in templates | T-004a (moderation workflow), T-004b (bulk actions), T-004c (reporting) |
| F-005 Home Database | FR-F-005-1, FR-F-005-2, FR-F-005-3 | `homes/models.py` (Home, Appliance, ServiceProvider), `homes/views.py` (CRUD CBVs), `homes/admin.py` (with inlines) | T-005a (home CRUD), T-005b (appliance tracking), T-005c (service provider management) |
| F-006 Task Completion | FR-F-006-1, FR-F-006-2 | `maintenance/models.py` (TaskCompletion), `maintenance/views.py` (MarkCompleteView), `maintenance/forms.py` | T-006a (completion recording), T-006b (history display) |

---

## 14. Open questions

- **Q1**: Should the system send email or SMS notifications for upcoming scheduled tasks, or rely on users checking the application?  
  **Status**: Deferred to v1.1. MVP will not include notifications; users must check schedule manually.

- **Q2**: What is the appropriate frequency for moderators to review pending tips (real-time, daily, weekly)?  
  **Status**: Under review. Recommendation: Daily review during beta, adjusted based on submission volume.

- **Q3**: Should appliance warranty tracking trigger automated reminders for warranty expiration?  
  **Status**: Deferred to v1.2. MVP includes warranty expiration date field but no automated reminders.

- **Q4**: How should the system handle multi-family properties (duplexes, apartments with shared maintenance)?  
  **Status**: Out of scope for MVP. Single-family homes only. Multi-family support deferred to v2.0.

- **Q5**: Should service provider contacts be shareable across users in the same geographic area?  
  **Status**: Out of scope for MVP. Service providers are private to each home. Community sharing deferred to v1.2.

---

## 15. References

- [Original PRD (Module 2 - PRD.md)](../Module%202%20-%20PRD.md)
- [Final Project Rubric](../FinalProjectRubric.MD)
- [Project Summary](../../PROJECT_SUMMARY.md)
- [README.md](../../README.md)
- **External Research**:
  - Thumbtack 2022 Survey: Millennial Homeowner Stress and Maintenance Overwhelm
  - Kin Insurance May 2025 Report: First-Time Homebuyer Unexpected Costs
  - Matt Layman's "Understand Django": <https://www.mattlayman.com/understand-django/>
- **Competitive Analysis**:
  - HomeZada: Home management platform (lacks personalization)
  - BrightNest: Home maintenance tips (lacks scheduling automation)
  - Centriq: Home manual organization (lacks community features)
