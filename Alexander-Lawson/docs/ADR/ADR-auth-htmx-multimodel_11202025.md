# ADR-003: Authentication, HTMX, and Multi-Model Architecture

Date: 2025-11-20
Status: Accepted

## Context

- PRD link: Module 3 Requirements - Build a Blog Feature Set 1 & 2
- Problem/forces: 
  - The basic blog (ADR-001) lacked user authentication and permission controls
  - No interactive features for enhanced UX
  - Single model (Post) insufficient for engagement features
  - Forms lacked comprehensive validation
  - Accessibility compliance not documented

The project needed to evolve from a basic CRUD blog to a production-ready application with authentication, role-based permissions, interactive UI elements, and a richer data model supporting user engagement through comments.

## Options

### Authentication Approach
- **A) Django built-in authentication**: Mature, battle-tested, integrated with admin
- **B) django-allauth**: More features (social auth), higher complexity
- **C) Custom auth system**: Maximum control, high maintenance burden

### Interactive UI
- **A) HTMX**: Minimal JS, progressive enhancement, Django-friendly
- **B) React/Vue**: Full SPA capabilities, requires API layer
- **C) Alpine.js**: Lightweight, limited server interaction

### Additional Model
- **A) Comment model**: Direct user engagement, simple relationship
- **B) Category/Tag expansion**: Content organization, more complex
- **C) Like/Vote system**: Engagement metrics, requires aggregation logic

### Form Validation Strategy
- **A) Django form clean methods**: Server-side, secure, verbose
- **B) Client-side JS validation**: Faster feedback, less secure
- **C) Hybrid approach**: Best UX, doubled maintenance

## Decision

We chose:
- **Authentication**: Django built-in (Option A) - Meets all requirements without added complexity
- **Interactive UI**: HTMX (Option A) - Progressive enhancement aligns with accessibility goals
- **Additional Model**: Comment (Option A) - Provides immediate user engagement value
- **Validation**: Django clean methods (Option A) - Security-first approach with comprehensive error handling

### Implementation Details

1. **Authentication System**
   - `LoginView` and `LogoutView` from `django.contrib.auth.views`
   - `LoginRequiredMixin` for view-level permissions
   - `UserPassesTestMixin` for author-only edit/delete operations
   - LOGIN_URL, LOGIN_REDIRECT_URL configuration

2. **HTMX Integration**
   - django-htmx middleware for request detection
   - Live search: `hx-get` with 500ms debounce on search input
   - Partial templates for dynamic content updates
   - Graceful degradation (works without JS)

3. **Comment Model**
   - ForeignKey to Post (one-to-many)
   - ForeignKey to User (author tracking)
   - CASCADE deletion (comments removed with parent post)
   - `related_name='comments'` for reverse lookups

4. **Form Validation**
   - `clean_title()`: Length validation, duplicate checking
   - `clean_content()`: Minimum length, spam detection (all-caps check)
   - `clean()`: Cross-field validation (title repetition in content)
   - Bootstrap styling with ARIA attributes for accessibility

## Consequences

### Positive
- **Security**: Authentication protects write operations; only authors can modify their content
- **User Engagement**: Comments enable discussion and community building
- **UX Enhancement**: HTMX live search provides instant feedback without page reloads
- **Code Quality**: Form validation prevents bad data at multiple levels
- **Accessibility**: ARIA attributes, semantic HTML, keyboard navigation support WCAG 2.2
- **Maintainability**: Django built-in tools reduce custom code and security risks
- **Performance**: HTMX reduces payload compared to full SPA frameworks

### Negative/Risks
- **HTMX Learning Curve**: Team needs to learn `hx-*` attributes and partial rendering patterns
- **Comment Moderation**: No built-in spam filtering or moderation workflow (future need)
- **Permission Granularity**: Current implementation is binary (author/non-author); no roles like "editor" or "moderator"
- **Validation UX**: Server-side validation requires round-trip; slower feedback than client-side
- **HTMX Browser Support**: Requires JS enabled; graceful degradation needed

### Technical Debt
- No comment threading/nesting (flat structure)
- No rate limiting on comment creation (spam risk)
- Search not indexed (will slow with large datasets)
- No caching layer for repeated searches
- Missing: Password reset, email verification, social auth

## Validation

### Success Metrics
- ✅ Users can register, login, logout via Django admin and custom login page
- ✅ Unauthenticated users cannot create/edit/delete posts
- ✅ Authors can only edit/delete their own posts (except superusers)
- ✅ Live search filters posts in real-time without page reload
- ✅ Comments save with author attribution and timestamps
- ✅ Forms reject invalid data with specific error messages
- ✅ WCAG 2.2 Level AA compliance verified with manual testing

### Rollback Strategy
- Authentication: Remove `LoginRequiredMixin`, revert URL patterns
- HTMX: Remove middleware, restore static templates
- Comments: Delete Comment model, run migration rollback
- Validation: Simplify forms to basic ModelForm

### Monitoring
- Django admin logs track authentication events
- Form validation errors logged for analysis
- HTMX requests identifiable via `HX-Request` header
- Comment creation rate monitored for spam patterns

## References
- Django Authentication Docs: https://docs.djangoproject.com/en/5.2/topics/auth/
- HTMX Documentation: https://htmx.org/docs/
- WCAG 2.2 Guidelines: https://www.w3.org/WAI/WCAG22/quickref/
- Related ADRs: ADR-001 (Basic Blog), ADR-002 (Templates)
