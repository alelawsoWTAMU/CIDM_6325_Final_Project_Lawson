# BRIEF: Build Authentication, HTMX Search, and Comments Feature

Date: 2025-11-20
Related ADR: ADR-003

## Goal

Implement user authentication, HTMX-powered live search, Comment model with CRUD, and comprehensive form validation addressing Module 3 Requirements (Feature Set 1, Parts A & B).

## Scope (single implementation session)

### Files to touch
- `blog_project/settings.py` - Add django-htmx, LOGIN_URL configs
- `blog_project/urls.py` - Add login/logout URLs
- `myblog/models.py` - Add Comment model
- `myblog/forms.py` - Add validation to PostForm, create CommentForm
- `myblog/views.py` - Add LoginRequiredMixin, UserPassesTestMixin, search_posts view
- `myblog/urls.py` - Add search endpoint
- `myblog/admin.py` - Register Comment model
- `templates/registration/login.html` - Create login template
- `templates/blog/base.html` - Add HTMX CDN, navigation with auth status
- `templates/blog/post_list.html` - Add search input with hx-get
- `templates/blog/partials/post_list_content.html` - Create partial for search results
- `templates/blog/post_form.html` - Add ARIA attributes

### Migrations
- `myblog/migrations/0002_comment.py` - Create Comment model migration

### Non-goals
- Password reset functionality (future)
- Email verification (future)
- Comment threading/nesting (future)
- Admin comment moderation tools (future)
- API endpoints (future)
- Comment voting/reactions (future)

## Standards

### Commits
Use conventional style:
- `feat(auth): add Django login/logout views`
- `feat(htmx): implement live search for posts`
- `feat(models): add Comment model with ForeignKey relationships`
- `feat(forms): add custom validation to PostForm and CommentForm`
- `feat(permissions): add LoginRequiredMixin and UserPassesTestMixin`
- `docs: add ADR-003 and ACCESSIBILITY.md`

### Security
- No secrets in code; use environment variables for production
- CSRF tokens required on all forms
- Password fields use appropriate input types
- Authentication required for write operations

### Testing
- Django TestCase for model validation
- Form validation tests for clean methods
- Permission tests for author-only access
- Manual WCAG 2.2 accessibility testing

## Acceptance Criteria

### User Flows

**Flow 1: Authentication**
1. Anonymous user visits /blog/
2. Clicks "Login" in navbar
3. Enters credentials on /login/
4. Redirects to /blog/ with authenticated navbar (shows username, logout)
5. "New Post" button now visible

**Flow 2: Permission Control**
1. Authenticated user creates a post
2. Only author sees "Edit" button on their posts
3. Attempting to edit another user's post (via URL) returns 403
4. Superuser can edit any post

**Flow 3: Live Search**
1. User types "django" in search box
2. After 500ms debounce, HTMX sends GET to /blog/search/?search=django
3. Results update without page reload
4. Partial template renders filtered posts
5. Spinner shows during search

**Flow 4: Comment Creation**
1. Authenticated user views post detail
2. Sees comment form at bottom
3. Enters comment text (min 3 chars)
4. Submits form
5. Comment appears with author name and timestamp
6. Comment visible to all users

**Flow 5: Form Validation**
1. User attempts to create post with 2-character title
2. Form shows error: "Title must be at least 5 characters long."
3. User attempts duplicate title
4. Form shows error: "A post with this title already exists."
5. User submits ALL CAPS content
6. Form shows error: "Please avoid using all capital letters."

### Technical Requirements
- ✅ Include migration? **YES** - 0002_comment.py
- ✅ Update README with superuser credentials
- ✅ Create DATABASE_SCHEMA.md with ERD
- ✅ Create ACCESSIBILITY.md with WCAG notes
- ✅ Create AI_REFLECTION.md (500 words)

## Prompts for Copilot

### Phase 1: Authentication
```
"Add Django's built-in login/logout views to blog_project/urls.py"
"Create a login template at templates/registration/login.html with Bootstrap styling and ARIA attributes"
"Add LOGIN_URL and LOGIN_REDIRECT_URL to settings.py"
"Update base.html navbar to show login/logout based on user.is_authenticated"
```

### Phase 2: Permissions
```
"Add LoginRequiredMixin to PostCreateView"
"Add LoginRequiredMixin and UserPassesTestMixin to PostUpdateView to restrict editing to post authors"
"Add test_func method that checks if request.user == post.author or is superuser"
"Apply same pattern to PostDeleteView"
```

### Phase 3: Comment Model
```
"Create a Comment model with ForeignKey to Post and User, including content TextField and timestamps"
"Register Comment model in admin.py with list_display showing author, post, and content preview"
"Generate migration for Comment model"
"Run migration to create comments table"
```

### Phase 4: HTMX Search
```
"Install django-htmx package"
"Add django-htmx to INSTALLED_APPS and HtmxMiddleware to MIDDLEWARE"
"Add HTMX CDN script tag to base.html"
"Create search_posts view that filters Post objects by title, content, or author username using Q objects"
"Add search URL pattern to myblog/urls.py"
"Create templates/blog/partials/post_list_content.html with the post list loop"
"Add search input to post_list.html with hx-get, hx-trigger='keyup changed delay:500ms', hx-target='#post-list'"
```

### Phase 5: Form Validation
```
"Add clean_title method to PostForm to validate length and check for duplicates, excluding current instance"
"Add clean_content method to check minimum length and detect all-caps spam"
"Add clean method to PostForm to check if title appears too many times in content"
"Add Bootstrap classes and ARIA attributes to form widgets"
"Create CommentForm with clean_content validation for length limits"
```

### Phase 6: Accessibility
```
"Add aria-label, aria-required, and aria-describedby attributes to form fields"
"Add role='alert' and aria-live='polite' to error messages"
"Add role='navigation' and aria-label to navbar"
"Add role='main' and id='main-content' to main container"
"Update form template to show required field asterisks with aria-label='required'"
```

## Output Expectations

After implementation:
1. Explain authentication flow and permission checking mechanism
2. Show example HTMX request/response for search
3. Demonstrate form validation with specific examples
4. Provide git diff summary for review
5. Suggest conventional commit messages for each feature area

## Documentation Requirements

Create three documentation files in `docs/Module 3/`:
1. **DATABASE_SCHEMA.md** - ERD diagram, migration notes, business use cases
2. **ACCESSIBILITY.md** - WCAG 2.2 compliance checklist with implementation examples
3. **AI_REFLECTION.md** - 500-word reflection on AI-assisted development with prompt examples

## Validation Checklist

Before marking complete:
- [ ] `python manage.py check` passes with no errors
- [ ] All migrations applied successfully
- [ ] Superuser created for testing
- [ ] Login/logout flow tested manually
- [ ] Non-author cannot edit others' posts
- [ ] Live search returns filtered results
- [ ] Form validation shows appropriate errors
- [ ] ARIA attributes present on forms
- [ ] README updated with setup instructions
- [ ] All documentation files created
- [ ] No syntax errors in templates
- [ ] HTMX requests visible in browser dev tools
