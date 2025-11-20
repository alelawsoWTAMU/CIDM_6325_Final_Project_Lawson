# BRIEF: Build Blog View Page slice

## Goal

- Implement blog view page functionality addressing ADR-0001 (Simple Blog Functionality).
- Create a complete blog post listing and detail view system using Django's MVT pattern.

## Scope (single PR)

### Files to touch:
- `myblog/models.py` - Create `Post` model with title, content, author, created_at, updated_at
- `myblog/views.py` - Add `post_list` and `post_detail` function-based views
- `myblog/urls.py` - Create URL patterns for blog views
- `blog_project/urls.py` - Include myblog URLs
- `myblog/templates/myblog/base.html` - Base template with common structure
- `myblog/templates/myblog/post_list.html` - Template for listing all posts
- `myblog/templates/myblog/post_detail.html` - Template for individual post display
- `myblog/admin.py` - Register Post model in Django admin
- `myblog/migrations/` - Generate migration for Post model

### Non-goals:
- User authentication or authorization
- Comment system
- Rich text editor integration
- Image uploads or media handling
- Pagination (can be added later)
- Search functionality
- Categories or tags
- Frontend CSS framework (use minimal inline styles)

## Standards

- **Commits**: conventional style (feat/fix/docs/refactor/chore).
  - `feat(myblog): add Post model and migrations`
  - `feat(myblog): create blog list and detail views`
  - `feat(myblog): add templates for blog pages`
  - `feat(myblog): configure URLs and admin`
- **No secrets**; env via settings.
- **Django tests**: use unittest/Django TestCase (no pytest).
- Follow PEP 8 style guidelines.
- Use Django best practices (Model Meta, verbose_name, ordering).

## Acceptance

### User flow:
1. User navigates to `/blog/` and sees a list of all blog posts ordered by creation date (newest first)
2. Each post in the list shows title, author, creation date, and content preview (first 200 chars)
3. User clicks on a post title to view full post at `/blog/<id>/`
4. Detail page displays full post content with title, author, timestamps
5. Admin can create/edit/delete posts via Django admin at `/admin/`

### Include migration?
- **Yes** - Create and apply migration for Post model

### Update docs & PR checklist:
- [ ] Model created with proper fields and Meta class
- [ ] Views implement list and detail functionality
- [ ] Templates extend base template and display data correctly
- [ ] URLs configured and included in project URLconf
- [ ] Admin interface registered and functional
- [ ] Migration created and applied successfully
- [ ] Manual testing completed for all user flows
- [ ] Code passes Django system checks (`python manage.py check`)
- [ ] Update README.md with setup instructions

## Prompts for Copilot

1. "Create a Django Post model in myblog/models.py with fields: title (CharField, max 200), content (TextField), author (CharField, max 100), created_at (DateTimeField auto_now_add), updated_at (DateTimeField auto_now). Add Meta class with ordering by -created_at and verbose_name_plural."

2. "Generate function-based views in myblog/views.py: post_list that queries all Post objects and renders post_list.html, and post_detail that takes post_id, gets post or 404, and renders post_detail.html."

3. "Create myblog/urls.py with URL patterns: empty path '' maps to post_list view with name 'post_list', and '<int:post_id>/' maps to post_detail view with name 'post_detail'. Use app_name = 'myblog' for namespacing."

4. "Generate Django templates: base.html with basic HTML structure and {% block content %}, post_list.html extending base showing all posts with links to detail, post_detail.html showing full post with back link to list."

5. "Register Post model in myblog/admin.py with list_display showing title, author, created_at, and list_filter for created_at. Add search_fields for title and content."

6. "Explain all changes made and propose commit messages following conventional commit style."

7. "Show me how to run makemigrations, migrate, and create a superuser for testing."
