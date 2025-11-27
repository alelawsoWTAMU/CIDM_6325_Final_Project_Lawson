# Quick Start Guide - Homestead Compass

## Prerequisites
- Python 3.8 or higher installed
- Basic command line knowledge

## Installation & Setup (5 minutes)

### Step 1: Verify Django Installation
```bash
py -m django --version
```
If Django is not installed:
```bash
pip install django
```

### Step 2: Navigate to Project Directory
```bash
cd "C:\Users\a13152\OneDrive - Cleveland-Cliffs Inc\Desktop\Final_Project"
```

### Step 3: Verify Database (Already Created)
The database migrations have already been applied. To verify:
```bash
py manage.py showmigrations
```
You should see all migrations marked with [X].

### Step 4: Create Admin User
```bash
py manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 5: Load Sample Data (Optional)
```bash
py manage.py seed_tasks
```
This loads 62 comprehensive maintenance tasks into the database.

### Step 6: Start the Development Server
```bash
py manage.py runserver
```

### Step 7: Access the Application
Open your browser and go to:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Home Wizard**: http://127.0.0.1:8000/homes/wizard/ (after login)
- **Blog Posts**: http://127.0.0.1:8000/tips/blog/ (community articles)

## First Steps in the Application

### For Regular Users:

1. **Register an Account**
   - Click "Register" in the navigation
   - Fill out the form with username, email, password
   - Optionally indicate you're a first-time homeowner

2. **Add Your First Home (Enhanced Wizard Available)**
   
   **Option A: Quick Add** (traditional)
   - After logging in, click "My Homes"
   - Click "Add a New Home"
   - Enter basic details in one form
   
   **Option B: Comprehensive Wizard** (recommended)
   - Navigate to http://127.0.0.1:8000/homes/wizard/
   - Complete 3-step guided process:
     * Step 1: Basic info (address, year built, construction type, climate zone)
     * Step 2: Home features (roof type/age, HVAC type/age, siding, basement, attic)
     * Step 3: Appliance inventory (add multiple appliances with serial numbers, energy ratings)
   - Auto-generates personalized schedule upon completion

3. **Generate Your Maintenance Schedule (Intelligent)**
   - From your home detail page, click "Generate Schedule"
   - View smart recommendations with priority scoring:
     * **High Priority** (80+): Overdue, seasonal matches, extreme climate tasks
     * **Medium Priority** (60-79): Important but less urgent
     * **Low Priority** (<60): Optional maintenance
   - See current season and climate factor
   - Use "Auto-Generate Full Year Schedule" for one-click annual planning
   - Preview annual schedule with due dates and priorities

4. **Explore Maintenance Tasks (62 Total)**
   - Click "Tasks" in the navigation
   - Browse 62 comprehensive maintenance tasks
   - Filter by category and seasonal priority
   - View detailed instructions, tools needed, estimated time, difficulty
   - See which tasks apply to your home's features

5. **Check Out Community Tips & Expert Blog Posts**
   - **Community Tips**: Browse tips from experts and questions from homeowners
     * Filter by post type (tips/questions)
     * Upvote helpful content
     * Comment and discuss
     * Submit your own tips or ask questions
   - **Expert Blog Posts**: Read long-form articles
     * Rich text content with images
     * Filter by category
     * Sort by popular/recent/most viewed
     * Upvote and comment on posts

### For Administrators:

1. **Access Admin Interface**
   - Go to http://127.0.0.1:8000/admin/
   - Log in with your superuser credentials

2. **Manage Maintenance Tasks (62 Total)**
   - Navigate to "Maintenance tasks"
   - Add, edit, or deactivate tasks
   - Set applicability rules (home age, features required)
   - Set seasonal priority (spring/summer/fall/winter/any)
   - Configure frequency and difficulty levels

3. **Moderate Community Content**
   - **Tips**: Review pending tips, use bulk actions (approve/reject/flag)
   - **Blog Posts**: Approve expert articles, manage featured posts
   - **Comments**: Monitor discussions on tips and blog posts
   - **Reports**: Review user-reported problematic content

4. **Manage Expert Accounts**
   - Navigate to "Expert profiles"
   - Review expert applications with trade/location/experience
   - Use bulk actions to approve or revoke expert status
   - Verified experts can post tips and write blog articles

5. **View User Data & Analytics**
   - Navigate to "Users" to see registered users (13 models total)
   - Check "Homes" with enhanced fields (roof, HVAC, siding details)
   - Review "Schedules" with priority scoring
   - Monitor engagement via upvotes, comments, views

## Common Tasks

### Add an Appliance to Your Home
1. Go to "My Homes"
2. Click on your home
3. Scroll to the Appliances section
4. Click "Add Appliance"
5. Fill in details (type, manufacturer, model, year installed)

### Add a Service Provider
1. Go to "My Homes"
2. Click on your home
3. Scroll to the Service Providers section
4. Click "Add Service Provider"
5. Fill in contact details

### Mark a Task as Complete
1. Go to "My Schedule"
2. Find the task you completed
3. Click "Mark Complete"
4. Optionally add notes about cost, time spent, and feedback

### Use the Home Onboarding Wizard (NEW)
1. Click "My Homes" → "Onboarding Wizard" or navigate to `/homes/wizard/`
2. Step 1: Enter basic home details (address, year built, construction, climate)
3. Step 2: Add features (roof type/age, HVAC type/age, siding, basement, attic)
4. Step 3: Add appliances (repeatable - add as many as needed)
5. Click "Complete & Generate Schedule" to finish
6. System auto-generates personalized schedule based on all details

### Generate Intelligent Annual Schedule (NEW)
1. Go to "My Schedule" for a specific home
2. Click "Generate Schedule"
3. Review priority-grouped tasks (High/Medium/Low)
4. See current season and climate factor
5. Click "Auto-Generate Full Year Schedule" for one-click annual planning
6. Or click "Preview Annual Schedule" to see full year distribution
7. Tasks are automatically prioritized by seasonal relevance and climate

### Submit a Community Tip or Question
1. Go to "Community Tips"
2. Click "Share a Tip"
3. Fill in title, category, content, and location
4. Submit (will be pending moderator approval)

## Troubleshooting

### Server Won't Start
```bash
# Check for port conflicts
netstat -ano | findstr :8000

# Try a different port
py manage.py runserver 8080
```

### Forgot Admin Password
```bash
py manage.py changepassword <username>
```

### Reset Database (Caution: Deletes All Data)
```bash
# Delete database file
del db.sqlite3

# Delete migrations (except __init__.py)
# Then recreate
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py seed_tasks
```

### Clear Sample Tasks
```bash
py manage.py seed_tasks --clear
```

## Project Structure Reference

```
Final_Project/
├── accounts/           # User authentication
├── homes/             # Home & property management
├── maintenance/       # Tasks & schedules
├── tips/              # Community tips
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── manage.py          # Django CLI
└── db.sqlite3         # Database
```

## Next Steps

1. **Create test homes** with different characteristics to see how the schedule generator adapts
2. **Add maintenance tasks** through the admin interface
3. **Submit sample tips** to test the moderation workflow
4. **Customize templates** in the `templates/` directory
5. **Add more management commands** in `maintenance/management/commands/`

## Need Help?

- Check `README.md` for comprehensive documentation
- Review `PROJECT_SUMMARY.md` for implementation details
- Consult Django documentation: https://docs.djangoproject.com/
- Review Matt Layman's "Understand Django": https://www.mattlayman.com/understand-django/

## Stopping the Server

Press `CTRL+C` in the terminal where the server is running.

---

**Note**: This is a development setup. See the Production Readiness Checklist in `PROJECT_SUMMARY.md` before deploying to production.
