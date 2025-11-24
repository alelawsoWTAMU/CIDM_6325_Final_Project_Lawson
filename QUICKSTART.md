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
This loads 12 sample maintenance tasks into the database.

### Step 6: Start the Development Server
```bash
py manage.py runserver
```

### Step 7: Access the Application
Open your browser and go to:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/

## First Steps in the Application

### For Regular Users:

1. **Register an Account**
   - Click "Register" in the navigation
   - Fill out the form with username, email, password
   - Optionally indicate you're a first-time homeowner

2. **Add Your First Home**
   - After logging in, click "My Homes"
   - Click "Add a New Home"
   - Enter your home's details:
     - Name (e.g., "Main House")
     - Year built
     - Construction type
     - Climate zone
     - Features (basement, attic, HVAC, etc.)

3. **Generate Your Maintenance Schedule**
   - From your home detail page, look for "Generate Schedule"
   - The system will create personalized tasks based on your home's characteristics
   - View your schedule in "My Schedule"

4. **Explore Maintenance Tasks**
   - Click "Tasks" in the navigation
   - Browse available maintenance tasks
   - View detailed instructions, tools needed, and safety notes

5. **Check Out Community Tips**
   - Click "Community Tips"
   - Browse tips from other homeowners
   - Upvote helpful tips
   - Submit your own tips to share with the community

### For Administrators:

1. **Access Admin Interface**
   - Go to http://127.0.0.1:8000/admin/
   - Log in with your superuser credentials

2. **Manage Maintenance Tasks**
   - Navigate to "Maintenance tasks"
   - Add, edit, or deactivate tasks
   - Set applicability rules (home age, features required)

3. **Moderate Community Tips**
   - Navigate to "Local tips"
   - Review pending tips
   - Use bulk actions to approve/reject/flag tips
   - Review reported tips in "Tip reports"

4. **View User Data**
   - Navigate to "Users" to see registered users
   - Navigate to "Homes" to see all properties
   - Check "Schedules" to see what tasks users have scheduled

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

### Submit a Community Tip
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
