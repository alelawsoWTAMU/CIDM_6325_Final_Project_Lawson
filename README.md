# Django Blog Project Module 4 RETRY- Alexander Lawson

## Description
This is an attempt to resubmit Module 4 without any merge conflicts and receive a potential regrade in Canvas. The project is a simple blog application built with Django featuring blog post listing, detail views, and Django admin integration.

## Project Structure

```
Module 3/
├── Alexander-Lawson/          # Django project root
│   ├── blog_project/          # Project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── myblog/                # Blog app
│   │   ├── models.py          # Post model
│   │   ├── views.py           # List and detail views
│   │   ├── urls.py            # URL patterns
│   │   ├── admin.py           # Admin configuration
│   │   └── templates/myblog/  # Templates
│   │       ├── base.html
│   │       ├── post_list.html
│   │       └── post_detail.html
│   └── manage.py
└── .venv/                     # Virtual environment
```

## Features

- **Blog Post Model**: Title, content, author, timestamps
- **List View**: Display all posts ordered by creation date
- **Detail View**: Full post content with metadata
- **Django Admin**: Create, edit, and delete posts
- **Clean Templates**: Responsive design with minimal styling

## Setup Instructions

### 1. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install django
```

### 3. Navigate to Project Directory

```powershell
cd Alexander-Lawson
```

### 4. Run Migrations (Already Done)

The database migrations have been created and applied. If needed:

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (For Admin Access)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

**Default Superuser Credentials:**
- Username: `admin`
- Email: `admin@wtamu.edu`
- Password: `mDitka89` (change in production)

### 6. Run Development Server

```powershell
python manage.py runserver
```

## Usage

### Access the Blog

- **Blog List**: http://localhost:8000/blog/
- **Blog Post Detail**: http://localhost:8000/blog/1/ (replace 1 with post ID)
- **Admin Interface**: http://localhost:8000/admin/

### Create Blog Posts

1. Navigate to http://localhost:8000/admin/
2. Log in with your superuser credentials
3. Click on "Blog Posts" under the MYBLOG section
4. Click "Add Blog Post"
5. Fill in title, author, and content
6. Click "Save"

### View Blog Posts

1. Navigate to http://localhost:8000/blog/
2. Click on any post title to view full content
3. Use "Back to all posts" link to return to list

## Development Notes

- **Architecture**: Function-Based Views (FBV) per ADR-0001
- **Database**: SQLite (default Django database)
- **Django Version**: 5.2+
- **Python Version**: 3.12.3

## Testing

Run Django system checks:

```powershell
python manage.py check
```

## Next Steps

- Add pagination to post list
- Implement categories/tags
- Add comment system
- Rich text editor for content
- User authentication for post creation

## Documentation

- ADR: `docs/ADR-basic_blog.md`
- Brief: `docs/COPILOT-BRIEF-blog-view.md`

