# Product Requirements Document (PRD)

## 1. Document Information

- Product/Feature Name: Blog Application with CBV Architecture
- Author(s): Alexander Lawson
- Date Created: 2025-10-15
- Last Updated: 2025-11-20
- Version: 1.1 (Module 4 Update - CBV Refactoring)

---

## 2. Overview

- **Summary**: Django-based blog application enabling authenticated users to create, read, update, and delete blog posts with comment functionality. Module 4 refactored all CRUD operations to use Class-Based Views (CBVs) for improved maintainability and code reusability.

- **Problem Statement**: 
  - Initial implementation used Function-Based Views (FBVs) which resulted in code duplication across CRUD operations
  - Repetitive permission checking and form handling logic reduced maintainability
  - Need for standardized view patterns to support team scalability and onboarding

- **Goals & Objectives**:
  - Refactor all blog CRUD operations to use Django generic CBVs (ListView, CreateView, UpdateView, DeleteView)
  - Implement declarative permission control using LoginRequiredMixin and UserPassesTestMixin
  - Maintain 100% feature parity with FBV implementation (authentication, HTMX search, comments, validation)
  - Document architectural tradeoffs between FBV and CBV approaches
  - Evaluate peer implementations for code quality and maintainability

- **Non-Goals**:
  - Building REST API endpoints (future consideration)
  - Implementing async views or database operations
  - Adding comment threading/nesting (remains flat structure)
  - Social authentication integration (Django built-in auth only)

---

## 3. Context & Background

- **Business Context**: 
  - Module 4 educational objective: Compare FBV vs CBV architectural patterns
  - Focus on code maintainability, readability, and Django best practices
  - Peer review component emphasizes collaborative learning and code critique skills

- **Market/Customer Insights**:
  - **Primary Users**: Blog authors and readers in academic/educational context
  - **Pain Points**: Simple, distraction-free blogging with authentication
  - **User Personas**:
    - Content Creator: Writes posts, needs easy CRUD interface
    - Reader: Browses posts, searches content, leaves comments
    - Administrator: Manages users and content via Django admin

- **Competitive/Benchmark References**:
  - Django official tutorial (polls app) uses FBVs
  - Django documentation recommends CBVs for standard CRUD patterns
  - Industry standard: CBVs for repetitive patterns, FBVs for unique logic

---

## 4. Scope

- **In Scope (Module 4 Iteration)**:
  - Refactor PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView to CBVs
  - Implement LoginRequiredMixin for authentication on create/update/delete views
  - Implement UserPassesTestMixin for author-only edit/delete authorization
  - Maintain HTMX live search functionality (hybrid FBV approach for custom logic)
  - Document FBV vs CBV tradeoffs with decision matrix
  - Conduct peer review of another student's CBV implementation
  - Participate in discussion forum with substantive responses
  - Critique instructor's TravelMathLite repository architecture

- **Out of Scope**:
  - Converting search_posts to CBV (custom logic better suited for FBV)
  - API serializers or DRF integration
  - Frontend framework integration (React, Vue)
  - Advanced caching strategies
  - Microservices architecture
  - Comment moderation workflow

---

## 5. User Stories & Use Cases

- **Primary User Persona(s)**: Blog authors (authenticated), blog readers (any), system administrators

- **User Stories**:
  - As a **blog author**, I want to create posts with title and content, so that I can share my thoughts with readers
  - As a **blog author**, I want to edit only my own posts, so that my content remains under my control
  - As a **blog author**, I want to delete my posts, so that I can remove outdated or unwanted content
  - As a **reader**, I want to search posts by title/content/author, so that I can find relevant articles quickly
  - As a **reader**, I want to leave comments on posts, so that I can engage with content and authors
  - As an **administrator**, I want to edit any post, so that I can moderate inappropriate content

- **Use Case Scenarios**:

  **Happy Path - Create Post**:
  1. Authenticated user navigates to /blog/post/new/
  2. Fills in title and content with valid data
  3. Submits form
  4. PostCreateView validates data, sets author to request.user
  5. Redirects to post list with success message

  **Edge Case - Unauthorized Edit Attempt**:
  1. User A creates a post
  2. User B discovers post edit URL (/blog/post/1/edit/)
  3. User B attempts to access URL directly
  4. UserPassesTestMixin.test_func() checks if request.user == post.author
  5. Returns 403 Forbidden since User B is not the author

  **Edge Case - Live Search with No Results**:
  1. User types "nonexistent query" in search box
  2. HTMX triggers GET request after 500ms debounce
  3. search_posts view returns empty queryset
  4. Partial template renders "No posts found" message

---

## 6. Functional Requirements

- **FR-001**: System shall use Django generic CBVs (ListView, CreateView, UpdateView, DeleteView) for all Post CRUD operations
- **FR-002**: PostCreateView shall require authentication via LoginRequiredMixin and automatically set author to request.user
- **FR-003**: PostUpdateView and PostDeleteView shall restrict access to post author using UserPassesTestMixin.test_func()
- **FR-004**: Superusers shall bypass author restrictions and edit/delete any post
- **FR-005**: PostListView shall display all posts ordered by date_created (newest first)
- **FR-006**: PostDetailView shall display full post content and associated comments
- **FR-007**: Live search shall filter posts by title, content, or author username using Q objects
- **FR-008**: HTMX search shall debounce keystrokes (500ms) and update results without page reload
- **FR-009**: Forms shall validate title length (5-200 chars), content length (20+ chars), and detect duplicate titles
- **FR-010**: All forms shall include ARIA attributes for WCAG 2.2 Level AA compliance

---

## 7. Non-Functional Requirements

- **Performance**: 
  - p95 page load time under 500ms on local development server
  - HTMX search debounce prevents server overload (500ms delay)
  - Database queries optimized with select_related() for author foreign keys

- **Scalability**: 
  - CBV architecture supports horizontal scaling via stateless views
  - Session data stored server-side (Django default), requires sticky sessions or Redis for multi-server
  - Anticipated load: 100-500 concurrent users (academic project scale)

- **Accessibility**: 
  - WCAG 2.2 Level AA compliance
  - Keyboard navigation for all interactive elements
  - ARIA labels on form fields, error messages with role="alert"
  - Color contrast ratio 4.5:1 minimum for text

- **Security/Compliance**: 
  - CSRF protection on all POST requests (Django default)
  - XSS protection via template auto-escaping
  - SQL injection prevention via ORM parameterized queries
  - Authentication required for create/update/delete operations
  - Authorization enforced at view level (LoginRequiredMixin, UserPassesTestMixin)

- **Reliability/Availability**: 
  - No SLO defined (educational project)
  - Django development server for local testing only
  - Production deployment would require WSGI server (Gunicorn/uWSGI)

---

## 8. Dependencies

- **Internal Dependencies**:
  - Django 5.2.7 framework
  - Python 3.12.3 runtime
  - SQLite database (db.sqlite3)
  - Virtual environment (.venv)

- **External Libraries**:
  - django-htmx (HTMX middleware and request detection)
  - Bootstrap 5.3 (CSS framework via CDN)
  - HTMX 2.0.3 (progressive enhancement library via CDN)

- **Cross-Module Dependencies**:
  - Module 3: Authentication, HTMX, Comment model, form validation (prerequisites)
  - Module 4: CBV refactoring builds on Module 3 FBV foundation

---

## 9. Risks & Assumptions

- **Risks**:
  - **Risk 1 - CBV Learning Curve**: Team unfamiliar with method resolution order (MRO) and mixin composition
    - *Mitigation*: Document mixin ordering rules, provide training examples
  - **Risk 2 - Over-Abstraction**: Generic CBVs may obscure custom logic
    - *Mitigation*: Use FBVs for complex/unique operations (e.g., HTMX search)
  - **Risk 3 - Permission Testing**: test_func() logic can become complex
    - *Mitigation*: Write comprehensive unit tests for UserPassesTestMixin subclasses

- **Assumptions**:
  - Users access application via modern browsers with JavaScript enabled
  - Django ORM sufficient for query complexity (no raw SQL needed)
  - Single-server deployment adequate for academic project scale
  - Bootstrap CDN availability reliable for styling
  - All developers have Python 3.12+ and can create virtual environments

---

## 10. Acceptance Criteria

- **AC-001**: PostListView displays all posts when accessed at /blog/
- **AC-002**: PostCreateView redirects unauthenticated users to login page
- **AC-003**: PostUpdateView returns 403 when non-author attempts to edit post
- **AC-004**: Superuser can edit any post regardless of authorship
- **AC-005**: HTMX search returns filtered results within 1 second
- **AC-006**: Form validation prevents titles shorter than 5 characters
- **AC-007**: Form validation detects duplicate post titles
- **AC-008**: All forms pass WAVE accessibility checker with 0 errors
- **AC-009**: `python manage.py check` passes with 0 issues
- **AC-010**: Documentation includes FBV vs CBV tradeoffs with code examples

---

## 11. Success Metrics

- **Code Quality**: Reduced lines of code in views.py by 30% through CBV adoption
- **Maintainability**: New developer can understand view structure within 30 minutes
- **Test Coverage**: 85%+ code coverage for views and models
- **Performance**: No regression in page load times after CBV refactoring
- **Accessibility**: WCAG 2.2 Level AA compliance score of 100% via axe DevTools
- **Educational Outcomes**: 
  - Complete Module 4 requirements (100/100 points)
  - Document architectural decisions in ADR format
  - Provide substantive peer code reviews (150+ words each)
  - Demonstrate understanding of CBV patterns in critique documents

---

## 12. Rollout & Release Plan

- **Phasing**:
  - **Phase 1 (Module 3)**: Authentication, HTMX, comments, validation (FBV implementation)
  - **Phase 2 (Module 4)**: CBV refactoring, architectural documentation, peer review
  - **Future**: Service layer, REST API, async views, production deployment

- **Release Channels**:
  - Local development only (Django runserver)
  - GitHub repository for version control and collaboration
  - No production deployment planned for academic project

- **Training/Documentation Needs**:
  - README with setup instructions (virtualenv, migrations, superuser)
  - ADR documents for architectural decisions
  - Copilot briefs documenting AI-assisted development process
  - AI reflection on prompt engineering and tool usage
  - Inline code comments for complex logic (test_func(), clean methods)

---

## 13. Open Questions

- **Q1**: Should search_posts remain as FBV or refactor to FilterView CBV?
  - *Current Decision*: Keep as FBV due to custom HTMX logic and Q object filtering
- **Q2**: Should we implement Django REST Framework for API endpoints?
  - *Status*: Out of scope for Module 4; consider for future iteration
- **Q3**: How to handle comment pagination on post detail page?
  - *Status*: Not implemented; flat list acceptable for current scale
- **Q4**: Should we add role-based permissions (Editor, Moderator) beyond Author/Admin?
  - *Status*: Deferred; current binary permission model sufficient for requirements

---

## 14. References

- **ADR-001**: Basic Blog CRUD Implementation (FBV approach)
- **ADR-003**: Authentication, HTMX, and Multi-Model Architecture
- **ADR-004**: CBV Refactoring and Architecture Patterns (2025-11-20)
- **COPILOT-BRIEF-module3**: Module 3 Implementation Brief (2025-11-20)
- **COPILOT-BRIEF-module4**: Module 4 CBV Refactoring Brief (2025-11-20)
- **Part A FBV vs CBV Tradeoffs**: Architectural analysis document
- **Part B Application Architecture Critique**: Peer architecture review
- **Part E TravelMathLite Critique**: Instructor code evaluation
- Django Documentation: <https://docs.djangoproject.com/en/5.2/>
- Class-Based Views Reference: <https://docs.djangoproject.com/en/5.2/topics/class-based-views/>
- WCAG 2.2 Guidelines: <https://www.w3.org/WAI/WCAG22/quickref/>