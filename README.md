# Django Blog Project Module 3 RETRY - Alexander Lawson

## Description
A Django blog application featuring Class-Based Views (CBVs) for CRUD operations, user authentication with role-based permissions, HTMX-powered live search, multi-model architecture (Posts and Comments), comprehensive form validation, and WCAG 2.2 accessibility compliance. Module 4 refactored all CRUD operations from Function-Based Views to CBVs while maintaining 100% feature parity with Module 3.

## Project Structure

```
Module 3/
├── Alexander-Lawson/          # Django project root
│   ├── blog_project/          # Project configuration
│   │   ├── settings.py        # HTMX middleware, auth configs
│   │   ├── urls.py            # Login/logout routes
│   │   └── wsgi.py
│   ├── myblog/                # Blog app
│   │   ├── models.py          # Post and Comment models (ForeignKey relationships)
│   │   ├── views.py           # CBVs: ListView, CreateView, UpdateView, DeleteView
│   │   ├── urls.py            # URL patterns with .as_view()
│   │   ├── forms.py           # PostForm and CommentForm with custom validation
│   │   ├── admin.py           # Admin configuration for Post and Comment
│   │   ├── templates/
│   │   │   └── myblog/
│   │   │       ├── base.html          # HTMX CDN, auth-aware navbar
│   │   │       ├── post_list.html     # Live search with HTMX
│   │   │       └── post_detail.html   # Post content + comments
│   │   └── migrations/
│   │       ├── 0001_initial.py        # Post model
│   │       └── 0002_comment.py        # Comment model
│   ├── templates/
│   │   ├── blog/                      # Additional templates
│   │   │   ├── post_form.html         # Create/edit form
│   │   │   ├── post_confirm_delete.html
│   │   │   └── partials/
│   │   │       └── post_list_content.html  # HTMX partial
│   │   └── registration/
│   │       └── login.html             # Custom login template
│   ├── docs/
│   │   ├── ADR/
│   │   │   ├── ADR-001 (Basic Blog FBV)
│   │   │   ├── ADR-003 (Auth, HTMX, Multi-Model)
│   │   │   └── ADR-004 (CBV Refactoring)
│   │   ├── briefs/
│   │   │   ├── COPILOT-BRIEF-module3_11202025.md
│   │   │   └── COPILOT-BRIEF-module4_11202025.md
│   │   ├── prd/
│   │   │   └── blog_site_prd_1.MD     # Updated with Module 4 requirements
│   │   ├── Module 3/
│   │   │   ├── DATABASE_SCHEMA.md
│   │   │   ├── ACCESSIBILITY.md
│   │   │   └── AI_REFLECTION.md
│   │   └── Module 4/
│   │       ├── Part A FBV vs CBV Tradeoffs.md
│   │       ├── Part B Application Architecture Critique.md
│   │       ├── Part C Peer Review.md
│   │       ├── Part D Discussion.md
│   │       ├── Part D Responses.md
│   │       ├── Part E TravelMathLite Critique.md
│   │       └── AI_REFLECTION.md
│   ├── manage.py
│   └── db.sqlite3
└── .venv/                     # Virtual environment
```

## Features

### Module 4 - CBV Architecture
- **Class-Based Views**: All CRUD operations using generic CBVs (ListView, CreateView, UpdateView, DeleteView)
- **Declarative Permissions**: LoginRequiredMixin for authentication, UserPassesTestMixin for authorization
- **Author-Only Editing**: Users can only edit/delete their own posts (superuser override)
- **Hybrid Approach**: search_posts remains FBV for custom HTMX logic

### Module 3 - Feature Set
- **Authentication System**: Django built-in LoginView/LogoutView with custom templates
- **Role-Based Permissions**: LoginRequired and author-only restrictions via mixins
- **Multi-Model Architecture**: Post model with Comment model (ForeignKey relationships)
- **HTMX Live Search**: Real-time post filtering by title, content, or author (500ms debounce)
- **Form Validation**: 
  - Title length validation (5-200 chars)
  - Content minimum length (20 chars)
  - Duplicate title detection
  - All-caps spam detection
  - Cross-field validation (title repetition check)
- **Comment System**: Authenticated users can leave comments on posts
- **WCAG 2.2 Compliance**: ARIA attributes, semantic HTML, keyboard navigation, 4.5:1 contrast ratio

### Core Functionality
- **Blog Post Model**: Title, author (FK to User), content, timestamps
- **Comment Model**: Post (FK to Post), author (FK to User), content, timestamps
- **Django Admin**: Full CRUD capabilities for posts and comments
- **Responsive Design**: Bootstrap 5.3 styling with mobile-first approach

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry.git
cd CIDM_6325_Lawson_Retry
git checkout Module_4
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**
```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django django-htmx
```

Or use requirements.txt if available:
```bash
pip install -r requirements.txt
```

### 4. Navigate to Project Directory

```bash
cd Alexander-Lawson
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database with Post and Comment tables.

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

**Default Test Credentials:**
- Username: `admin`
- Email: `admin@wtamu.edu`
- Password: `admin` (change in production!)

### 7. Run Development Server

```bash
python manage.py runserver
```

Server starts at: http://127.0.0.1:8000/

## Usage

### Access the Application

- **Homepage**: http://127.0.0.1:8000/ (redirects to blog)
- **Blog List**: http://127.0.0.1:8000/blog/ or http://127.0.0.1:8000/blog/posts/
- **Post Detail**: http://127.0.0.1:8000/blog/post/1/ (replace 1 with post ID)
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Login Page**: http://127.0.0.1:8000/login/
- **Logout**: http://127.0.0.1:8000/logout/

### User Workflows

#### 1. Browse Posts (Unauthenticated)
1. Navigate to http://127.0.0.1:8000/blog/
2. View list of all posts with title, author, and date
3. Click on any post title to view full content
4. Use search box to filter posts in real-time (HTMX)

#### 2. Create Blog Post (Authenticated)
1. Click "Login" in navbar
2. Enter credentials (admin/admin for test account)
3. Click "New Post" button in navbar
4. Fill in title (5-200 chars) and content (20+ chars)
5. Submit form
6. Redirects to post list with new post visible

#### 3. Edit Your Post (Author Only)
1. Navigate to your post detail page
2. Click "Edit" button (only visible to author/superuser)
3. Modify title or content
4. Submit form
5. Changes saved and displayed

#### 4. Delete Your Post (Author Only)
1. Navigate to your post detail page
2. Click "Delete" button (only visible to author/superuser)
3. Confirm deletion on confirmation page
4. Post removed from database

#### 5. Use Live Search
1. On blog list page, type in search box
2. Results filter automatically after 500ms
3. Searches title, content, and author username
4. No page reload required (HTMX)

#### 6. Leave Comments (Authenticated)
1. Navigate to post detail page
2. Scroll to comment form (login required)
3. Enter comment text (3-1000 chars)
4. Submit form
5. Comment appears with your username and timestamp

## Development Notes

### Architecture Evolution
- **Module 1-2**: Initial FBV implementation with basic CRUD
- **Module 3**: Added authentication, HTMX, comments, validation, accessibility
- **Module 4**: Refactored to CBVs (37% code reduction while maintaining feature parity)

### Technology Stack
- **Framework**: Django 5.2.7
- **Python**: 3.12.3
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5.3 (CDN), HTMX 2.0.3
- **Middleware**: django-htmx for request detection

### Key Design Decisions (ADRs)
- **ADR-001**: Function-Based Views for initial implementation
- **ADR-003**: Authentication, HTMX, and Multi-Model Architecture
- **ADR-004**: Class-Based Views Refactoring (Module 4)

### CBV Implementation Details

**PostListView (ListView):**
- Displays all posts ordered by `-date_created`
- No authentication required (public view)
- Uses `post_list.html` template

**PostCreateView (LoginRequiredMixin, CreateView):**
- Requires authentication via `LoginRequiredMixin`
- Automatically sets `author = request.user` in `form_valid()`
- Uses `PostForm` with custom validation

**PostUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):**
- `test_func()` checks if `request.user == post.author` or `is_superuser`
- Returns 403 Forbidden if test fails
- Same template as CreateView (`post_form.html`)

**PostDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):**
- Same permission logic as UpdateView
- Displays confirmation page before deletion
- Redirects to post list after successful delete

**search_posts (FBV - Hybrid Approach):**
- Remains as function-based view for custom Q object filtering
- HTMX partial template rendering
- Filters by title, content, or author username

### Form Validation (Clean Methods)

**PostForm.clean_title():**
- Length validation (5-200 characters)
- Duplicate title detection (excludes current instance on edit)

**PostForm.clean_content():**
- Minimum 20 characters
- All-caps spam detection (rejects if >90% uppercase)

**PostForm.clean():**
- Cross-field validation
- Checks if title appears >3 times in content (spam indicator)

**CommentForm.clean_content():**
- Length validation (3-1000 characters)

## Testing

### System Checks
```bash
python manage.py check
```
Expected: `System check identified no issues (0 silenced).`

### Run Test Suite
```bash
python manage.py test myblog
```

### Manual Testing Checklist

**Authentication:**
- [ ] Unauthenticated user redirected to login when accessing `/blog/post/new/`
- [ ] Login successful with valid credentials
- [ ] Logout removes authentication

**Authorization:**
- [ ] Non-author receives 403 when attempting to edit another user's post
- [ ] Superuser can edit any post
- [ ] Delete button only visible to post author and superuser

**HTMX Search:**
- [ ] Typing in search box filters results after 500ms
- [ ] Search works for title, content, and author username
- [ ] Results update without page reload
- [ ] Empty search shows all posts

**Form Validation:**
- [ ] Title <5 chars rejected with error message
- [ ] Content <20 chars rejected
- [ ] Duplicate title rejected (except on edit of same post)
- [ ] All-caps content rejected

**WCAG Accessibility:**
- [ ] All form fields have aria-label or aria-labelledby
- [ ] Error messages have role="alert"
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Color contrast ratio ≥4.5:1 for text

### Performance Testing
```bash
python manage.py runserver
# Open browser dev tools
# Check Network tab for HTMX requests
# Verify <500ms response time for search queries
```

## Module 4 Deliverables

### Code Implementation (60 points)
✅ All CRUD operations refactored to CBVs  
✅ LoginRequiredMixin applied to create/update/delete views  
✅ UserPassesTestMixin with test_func() for author-only permissions  
✅ Superuser override in test_func()  
✅ Hybrid approach: search_posts remains FBV  

### Documentation (40 points)
✅ **Part A (10 pts)**: FBV vs CBV Tradeoffs analysis with decision matrix  
✅ **Part B (10 pts)**: Application Architecture Critique (2-3 pages)  
✅ **Part C (10 pts)**: Peer Review template with evaluation criteria  
✅ **Part D (10 pts)**: Discussion post + two substantive responses (150+ words each)  
✅ **Part E (10 pts)**: TravelMathLite Critique (modularity and scalability)  

### Supporting Documentation
✅ ADR-004: CBV Refactoring Decision Record  
✅ COPILOT-BRIEF-module4: Implementation guide  
✅ AI_REFLECTION: 587-word reflection on CBV refactoring  
✅ Updated PRD with Module 4 requirements  

## Future Enhancements

### Short Term
- Add unit tests for all views and forms (target: 85% coverage)
- Implement comment threading/nesting
- Add rich text editor (TinyMCE or CKEditor)
- Pagination for post list (25 posts per page)

### Medium Term
- REST API with Django REST Framework
- Category/tag system for posts
- Comment moderation workflow
- User profile pages
- Email notifications for comments

### Long Term
- Service layer for business logic
- Async views for improved performance
- Redis caching for frequently accessed posts
- Full-text search with PostgreSQL
- CI/CD pipeline with GitHub Actions
- Production deployment (Gunicorn + Nginx + PostgreSQL)

## Documentation

### Architecture Decision Records (ADRs)
- `docs/ADR/ADR-basic_blog 101525.md` - Initial FBV implementation
- `docs/ADR/ADR-auth-htmx-multimodel_11202025.md` - Module 3 features
- `docs/ADR/ADR-cbv-refactoring_11202025.md` - Module 4 CBV refactoring

### Copilot Briefs
- `docs/briefs/COPILOT-BRIEF-module3_11202025.md` - Module 3 implementation
- `docs/briefs/COPILOT-BRIEF-module4_11202025.md` - Module 4 refactoring

### Product Requirements
- `docs/prd/blog_site_prd_1.MD` - Comprehensive PRD (updated for Module 4)

### Module 3 Documentation
- `docs/Module 3/DATABASE_SCHEMA.md` - ERD and migration notes
- `docs/Module 3/ACCESSIBILITY.md` - WCAG 2.2 compliance checklist
- `docs/Module 3/AI_REFLECTION.md` - 498-word AI reflection

### Module 4 Documentation
- `docs/Module 4/Part A FBV vs CBV Tradeoffs.md` - Architectural analysis
- `docs/Module 4/Part B Application Architecture Critique.md` - Peer review
- `docs/Module 4/Part C Peer Review.md` - Review template
- `docs/Module 4/Part D Discussion.md` - Discussion post
- `docs/Module 4/Part D Responses.md` - Two peer responses
- `docs/Module 4/Part E TravelMathLite Critique.md` - Instructor code evaluation
- `docs/Module 4/AI_REFLECTION.md` - 587-word CBV reflection

## Contributing

This is an academic project for CIDM 6325 at West Texas A&M University. 

**Course**: Advanced Web Application Development  
**Instructor**: Dr. Jeff Babb  
**Student**: Alexander Lawson  
**Semester**: Fall 2025  

## License

Academic project - not licensed for commercial use.

## Contact

**Student**: Alexander Lawson  
**Email**: alawson1@wtamu.edu  
**GitHub**: [alelawsoWTAMU](https://github.com/alelawsoWTAMU)  
**Repository**: [CIDM_6325_Lawson_Retry](https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry)

## Acknowledgments

- **Django Documentation**: https://docs.djangoproject.com/
- **HTMX**: https://htmx.org/
- **Bootstrap**: https://getbootstrap.com/
- **GitHub Copilot**: AI pair programming assistant
- **Dr. Jeff Babb**: Course instruction and guidance

