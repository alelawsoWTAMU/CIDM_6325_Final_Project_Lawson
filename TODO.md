# Homestead Compass - To Do List

## Outstanding Development Tasks

### Content & Data
- [x] **More Maintenance Tasks in Library** ✅
  - ✅ Expanded the maintenance task database with 50 comprehensive homestead tasks
  - ✅ Added diverse categories: Home Structure & Safety, Mechanical & Utility, Off-Grid Energy & Water, Mobile Equipment & Tractors, Land & Fencing, Garden & Orchard
  - ✅ Included detailed tool lists for every task
  - ✅ Added estimated time (minutes) and difficulty ratings (beginner/intermediate/advanced/professional)
  - ✅ Added frequency schedules (monthly/quarterly/seasonal/annual/biannual/as_needed)
  - **Total: 62 active maintenance tasks in database**

- [ ] **Survey for Appliances and Home Features**
  - Create comprehensive onboarding survey for new users
  - Collect detailed appliance information (brand, model, age, warranty status)
  - Gather home feature details (roof type, HVAC system, siding material)
  - Use survey data to generate highly personalized maintenance schedules

### Admin & Management
- [x] **Admin Page Enhancements** ✅ COMPLETE
  - ✅ Comprehensive filtering: date hierarchies, list_filter for all major fields
  - ✅ Search capabilities: search_fields across all models (users, tasks, tips, homes, experts)
  - ✅ Bulk actions implemented:
    * Expert approval/revocation (accounts)
    * Tip moderation (approve, reject, flag)
    * Report resolution (tips)
    * Task activation (maintenance)
    * Service provider verification (homes)
  - ✅ Enhanced expert review interface: custom list_display shows approval status, trade, location, application date
  - ✅ List editable fields for quick inline updates (status, featured, verified, active)
  - ✅ Readonly fields for audit trails (timestamps, approval records)
  - ✅ Inline editing: appliances and service providers within home records
  - ✅ Built-in analytics: Django admin provides excellent reporting via filters, search, and list views

- [ ] **PM Schedule Finessing**
  - Refine preventive maintenance schedule generation algorithm
  - Add seasonal adjustment logic for different climate zones
  - Implement smart scheduling based on historical task completion
  - Allow users to customize schedule frequency preferences

### User Roles & Permissions
- [x] **Expert Blog Posts** ✅ COMPLETE
  - ✅ Created BlogPost model with rich text content (django-ckeditor)
  - ✅ Implemented blog post approval workflow (draft, pending, approved, rejected)
  - ✅ Created dedicated blog section with list, detail, create, edit, and delete views
  - ✅ Added featured posts functionality
  - ✅ Blog post management dashboard for experts (My Posts page)
  - ✅ Comment system for blog posts
  - ✅ Upvoting system for blog posts
  - ✅ Filter and search functionality (category, search terms, sort by popular/recent/views)
  - ✅ Reading time calculation based on word count
  - ✅ View count tracking
  - ✅ Expert-only creation (verified experts can write articles)
  - ✅ Admin approval workflow with bulk actions
  - ✅ Navigation link added to main menu
  - **Implementation**: Full blog CMS with rich text editor, approval workflow, and engagement features

- [x] **Restrictions on Main Users** ✅ COMPLETE
  - ✅ Unified community feed: both experts and homeowners can post
  - ✅ Experts post "tips" (advice/guidance), homeowners post "questions"
  - ✅ Post type automatically determined by user's verified expert status
  - ✅ Filtering by post type: users can filter to see only tips or only questions
  - ✅ All posts support comments (anyone can answer/discuss)
  - ✅ Upvoting system for both tips and questions
  - ✅ Search and category filtering across all posts
  - ✅ Visual distinction: tips (blue/teal header), questions (yellow/warning header)
  - ✅ Tip reporting system for problematic content
  - ✅ Descending chronological order by default (newest first)
  - **Implementation**: Modified LocalTip model with post_type field, removed expert-only restrictions on creation

### Quality Assurance
- [ ] **Verify All Bugs Worked Out**
  - Comprehensive testing of all user workflows
  - Test expert registration and approval process
  - Verify schedule generation with various home configurations
  - Test tip submission, commenting, and moderation
  - Cross-browser compatibility testing
  - Mobile responsiveness testing
  - Performance optimization
  - Security audit (XSS, CSRF, SQL injection protection)
  - Accessibility compliance (WCAG 2.1 AA)

---

**Last Updated:** November 23, 2025  
**Priority:** High priority items marked with ⚠️  
**Status:** In Development
