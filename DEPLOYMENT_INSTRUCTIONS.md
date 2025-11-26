# Deployment Instructions for Render.com

## Your Project is Ready to Deploy! 🚀

**GitHub Repository**: https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry  
**Branch**: `Final_Project`

---

## Option 1: Deploy Using render.yaml (Recommended - Fastest)

Your project includes a `render.yaml` file that automates the entire deployment process!

### Quick Deploy Steps:

1. **Sign up/Log in to Render.com**: https://render.com
   - Click "Get Started for Free" or "Sign In"
   - **Sign in with GitHub** (recommended)

2. **Create New Blueprint**:
   - Click **"New +"** button in the top right
   - Select **"Blueprint"**
   - Find and select: **`CIDM_6325_Lawson_Retry`**
   - Select branch: **`Final_Project`**
   - Click **"Connect"**

3. **Render Auto-Configures Everything**:
   - ✅ Creates PostgreSQL database
   - ✅ Creates web service
   - ✅ Links database to app
   - ✅ Generates secure SECRET_KEY
   - ✅ Sets all environment variables
   - ✅ Configures Python 3.12.0

4. **Review & Deploy**:
   - Review the resources to be created
   - Click **"Apply"**
   - Wait 5-10 minutes for deployment

**That's it!** Your app will be live at: `https://home-maintenance-compass.onrender.com`

---

## Option 2: Manual Deployment (Step-by-Step)

If you prefer manual setup or need to customize:

### 1. Sign Up / Log In to Render.com

1. Go to: **https://render.com**
2. Click "Get Started for Free" or "Sign In"
3. **Sign in with GitHub** (recommended)

### 2. Create PostgreSQL Database First

1. Click **"New +"** → Select **"PostgreSQL"**
2. Configure:
   - **Name**: `home_maintenance_compass_db`
   - **Database**: `home_maintenance_compass`
   - **User**: `home_maintenance_compass` (or auto-generated)
   - **Region**: Choose closest to you (e.g., Oregon USA)
   - **PostgreSQL Version**: 16 (or latest)
   - **Instance Type**: **Free**
3. Click **"Create Database"**
4. **Save the Internal Database URL** (you'll need it)

### 3. Create Web Service

1. Click **"New +"** → Select **"Web Service"**
2. Find and select: **`CIDM_6325_Lawson_Retry`**
3. Select branch: **`Final_Project`**
4. Click **"Connect"**

### 4. Configure Your Web Service

**Basic Settings:**
- **Name**: `home-maintenance-compass` (or any name you prefer)
- **Region**: Same as database (e.g., Oregon USA)
- **Branch**: `Final_Project`
- **Runtime**: **Python 3**

**Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn home_maintenance_compass.wsgi:application`

**Instance Type:**
- Select **"Free"** (750 hours/month free)

### 5. Add Environment Variables

Click **"Advanced"** to expand, then add each variable:

**Required Variables:**

1. **DATABASE_URL**
   - Value: Paste the Internal Database URL from Step 2
   - Example: `postgresql://user:password@host/database`

2. **SECRET_KEY**
   - Generate a secure key: Use Django's secret key generator or any random 50+ character string
   - Example: `django-insecure-xyz123abc456def789...`
   - **Important**: Never commit this to GitHub!

3. **DEBUG**
   - Value: `False`

4. **PYTHON_VERSION**
   - Value: `3.12.0`

5. **ALLOWED_HOSTS**
   - Value: `.onrender.com`
   - (Or your custom domain if applicable)

### 6. Deploy!

1. Review all settings
2. Click **"Create Web Service"**
3. Monitor the build logs (5-10 minutes):
   - ✅ Installing dependencies from requirements.txt
   - ✅ Running collectstatic (WhiteNoise handles static files)
   - ✅ Running migrations (creates database tables)
   - ✅ Starting gunicorn server

### 7. Access Your Deployed App

Your app will be live at: `https://home-maintenance-compass.onrender.com`

---

## Post-Deployment Setup

### Create Superuser Account

After successful deployment:

1. In Render dashboard, go to your web service
2. Click **"Shell"** tab in left sidebar
3. Click **"Launch Shell"**
4. Run:
```bash
python manage.py createsuperuser
```
5. Follow prompts to create username, email, and password

**Note**: If you've already loaded fixtures with user accounts (see Option B below), you can skip creating a superuser and log in with your existing admin account.

### Seed Data to Production

You have three options to populate your production database:

#### Option A: Seed Just Maintenance Tasks (Quick)

For basic setup with the 12 pre-defined maintenance tasks:
```bash
python manage.py seed_tasks
```

#### Option B: Transfer All Data from Local Database (Recommended)

**If you've already pushed fixture files to GitHub**, simply run in the Render Shell:

```bash
python manage.py load_all_fixtures
```

This will load all your local data including:
- ✅ 12 users (admin, alelawso3, and 10 experts) with their passwords
- ✅ User profiles and expert profiles
- ✅ Homes, maintenance tasks, schedules
- ✅ Community tips and blog posts

**If you haven't exported your data yet**, follow these steps:

To transfer ALL data from your local development database including users, homes, schedules, tips, and blog posts:

**Step 1 - Export locally (run on your computer):**
```bash
# Export everything including users
python manage.py export_all_data

# Or export without user accounts (if you want to create those manually)
python manage.py export_all_data --exclude-users
```

This creates JSON fixture files in the `fixtures/` directory:
- `users.json` - User accounts with hashed passwords
- `accounts.json` - User profiles and expert profiles
- `homes.json` - Home profiles, appliances, service providers
- `maintenance_tasks.json` - All maintenance tasks
- `schedules.json` - Generated schedules
- `task_completions.json` - Completed tasks
- `tips.json` - Community tips, blog posts, and comments

**Step 2 - Allow fixtures in Git:**

Edit `fixtures/.gitignore` to allow the files:
```bash
# Comment out the *.json line or add specific exceptions
# fixtures/.gitignore
# *.json  <-- comment this out to include all
```

**Step 3 - Commit and push:**
```bash
git add fixtures/
git commit -m "Add production seed data"
git push origin Final_Project
```

**Step 4 - Load on Render (in Shell tab):**

Wait for auto-deploy to complete, then:
```bash
python manage.py load_all_fixtures
```

The command loads fixtures in the correct order respecting foreign key dependencies.

**Alternative - Load individual fixtures:**
```bash
# Load specific data only
python manage.py loaddata fixtures/maintenance_tasks.json
python manage.py loaddata fixtures/tips.json
python manage.py loaddata fixtures/homes.json
```

#### Option C: Manual Django Admin

Create data manually through the admin panel at `/admin/` after logging in.

---

### Data Seeding Notes

**What Gets Exported:**
- ✅ Users & authentication (passwords already hashed)
- ✅ User profiles (regular and expert)
- ✅ Home profiles with appliances and service providers
- ✅ Maintenance tasks, schedules, and completions
- ✅ Community tips with comments and reports
- ✅ Expert blog posts with comments

**Important Considerations:**
- **Passwords**: Stored as hashes in fixtures - users can log in with existing passwords
- **User Files**: Fixtures only contain database records, not uploaded images/files
- **Loading Order**: The `load_all_fixtures` command handles dependencies automatically
- **Idempotent**: Safe to run multiple times - updates existing records with same IDs
- **Conflicts**: If production has different data, consider clearing it first via admin panel

**Troubleshooting Fixtures:**

If you get errors:
```bash
# ContentType issues - run migrations first
python manage.py migrate --run-syncdb
python manage.py load_all_fixtures

# Foreign key errors - ensure correct load order
# Use load_all_fixtures instead of manual loaddata

# Duplicate key errors - data already exists
# Delete conflicting records from admin panel first
```

### Access Admin Panel

Visit: `https://your-app-name.onrender.com/admin/`

Log in with the superuser credentials you created.

---

## What the Deployment Includes

✅ **Django Web Application** - All features including:
   - User authentication & registration
   - Expert verification system
   - Home profile management
   - Maintenance schedule generation
   - Task completion tracking
   - Community tips with moderation
   - Expert blog posts (CKEditor required - see note below)

✅ **PostgreSQL Database** - Production-ready relational database

✅ **Static Files** - Served via WhiteNoise (no AWS S3 needed)

✅ **Security** - DEBUG=False, secure SECRET_KEY, proper ALLOWED_HOSTS

---

## Important Notes

### CKEditor for Rich Text Editing

The project includes `django-ckeditor==6.7.3` for rich text editing in blog posts. This is already configured in both `requirements.txt` and `settings.py`, so it will work automatically upon deployment.

**Note**: CKEditor 4 has known security issues and is no longer supported. For long-term projects, consider migrating to CKEditor 5 or another editor.

### Free Tier Limitations

- **Database**: 1GB storage, expires after 90 days
- **Web Service**: Spins down after 15 minutes of inactivity
- **First request**: Takes 30-50 seconds after spin-down
- **Build time**: Limited resources, be patient

### Static Files

WhiteNoise is configured to serve static files efficiently in production. No additional CDN or AWS S3 setup needed!

---

## Troubleshooting

### Build Fails

**Check Build Logs**: Click "Logs" tab for detailed error messages

**Common Issues**:

1. **Module not found errors**:
   - Missing dependency in `requirements.txt`
   - Add the missing package and redeploy

2. **Database connection errors**:
   - Verify `DATABASE_URL` environment variable is set
   - Check database is created and running

3. **Build timeout**:
   - Free tier has limited resources
   - Try "Clear build cache & deploy" from Manual Deploy

4. **Static files 404**:
   - WhiteNoise should handle this automatically
   - Check `STATIC_ROOT` and `STATICFILES_STORAGE` in settings.py

### Site Shows Error Page

1. Check environment variables are set correctly
2. Verify `DEBUG=False` and `ALLOWED_HOSTS` includes `.onrender.com`
3. Check logs for Python exceptions

### Database Issues

1. **Migrations fail**:
   - Run manually in Shell: `python manage.py migrate --run-syncdb`

2. **Database tables missing**:
   - Verify migrations ran during build
   - Check build logs for migration output

### Performance Issues

- **Site is slow**: Free tier spins down after 15 minutes inactive
- **First load delay**: Normal for free tier (30-50 seconds)
- **Subsequent loads**: Should be fast

### Force Redeploy

If you make changes:
1. Push to GitHub `Final_Project` branch
2. Render auto-deploys on push (if enabled)
3. Or: **"Manual Deploy"** → **"Deploy latest commit"**

To clear cache:
- **"Manual Deploy"** → **"Clear build cache & deploy"**

---

## Environment Variables Reference

| Variable | Value | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | Auto-generated | PostgreSQL connection string |
| `SECRET_KEY` | Random 50+ chars | Django cryptographic signing |
| `DEBUG` | `False` | Disable debug mode in production |
| `PYTHON_VERSION` | `3.12.0` | Python runtime version |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed hostnames for Django |

---

## Updating Your Deployed App

### Making Changes

1. Make changes locally and test
2. Commit to GitHub:
```bash
git add .
git commit -m "Update feature X"
git push origin Final_Project
```
3. Render auto-deploys (if auto-deploy enabled)
4. Or manually deploy from dashboard

### Transferring Data from Local to Production

To copy all your local database data (users, homes, tips, schedules, etc.) to production:

**Step 1: Export data locally**
```bash
python manage.py export_all_data
```

This creates JSON fixture files in `fixtures/` directory containing all your data.

**Step 2: Review and commit fixtures**
```bash
# Edit fixtures/.gitignore to allow specific files
# Remove *.json or add !users.json, !tips.json, etc.

git add fixtures/
git commit -m "Add production seed data"
git push origin Final_Project
```

**Step 3: Load fixtures on Render**

In Render's Shell tab:
```bash
python manage.py load_all_fixtures
```

**Alternative: Export specific apps only**
```bash
# Export without user accounts (if you want to create those manually)
python manage.py export_all_data --exclude-users

# Or export individual apps
python manage.py dumpdata tips --indent 2 > fixtures/tips.json
python manage.py dumpdata maintenance --indent 2 > fixtures/maintenance.json
```

### Running Management Commands

Use the Shell in Render dashboard:

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Seed tasks only
python manage.py seed_tasks

# Export all data (run locally before deploying)
python manage.py export_all_data
python manage.py export_all_data --exclude-users

# Load all fixtures (run on production after pushing)
python manage.py load_all_fixtures

# Load individual fixtures
python manage.py loaddata fixtures/tips.json
python manage.py loaddata fixtures/maintenance_tasks.json

# Collect static files
python manage.py collectstatic --no-input

# Check deployment configuration
python manage.py check --deploy
```

### Available Management Commands

| Command | Purpose | Where to Run |
|---------|---------|-------------|
| `seed_tasks` | Load 12 pre-defined maintenance tasks | Production |
| `export_all_data` | Export all database data to JSON fixtures | Local |
| `export_all_data --exclude-users` | Export data without user accounts | Local |
| `load_all_fixtures` | Load all fixtures in correct order | Production |
| `loaddata <file>` | Load specific fixture file | Production |
| `dumpdata <app>` | Export specific app data | Local |
| `createsuperuser` | Create admin account | Production |
| `migrate` | Run database migrations | Production |
| `collectstatic` | Collect static files | Production |

---

## Testing Your Deployed App

### Test Checklist

- [ ] Homepage loads successfully
- [ ] User can register new account
- [ ] User can log in
- [ ] Static files load (CSS, images)
- [ ] Admin panel accessible at `/admin/`
- [ ] Can create home profile
- [ ] Can generate maintenance schedule
- [ ] Can mark tasks complete
- [ ] Can view/post community tips
- [ ] Expert verification system works
- [ ] Blog posts accessible (if using CKEditor)

### Test Accounts

Create test accounts for instructor:
1. **Admin account**: Via shell `createsuperuser`
2. **Regular user**: Via signup page
3. **Expert account**: Promote user to expert in admin panel

---

---

## For Your README.md

After successful deployment, add this section:

```markdown
## 🌐 Live Deployment

**Deployed Application**: https://home-maintenance-compass.onrender.com

### Features Available
- User registration and authentication
- Home profile management
- Automated maintenance schedule generation
- Task completion tracking
- Community tips with moderation
- Expert verification system
- Expert blog posts

### Demo Credentials
Contact instructor for admin and test user credentials.

### Technology Stack
- **Framework**: Django 5.2.7
- **Database**: PostgreSQL 16
- **Hosting**: Render.com
- **Static Files**: WhiteNoise
- **Python**: 3.12.0
```

---

## Alternative Deployment: PythonAnywhere

If Render.com doesn't work for any reason:

### PythonAnywhere Setup

1. **Sign up**: https://www.pythonanywhere.com (Free "Beginner" account)

2. **Clone repository**:
```bash
git clone https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry.git
cd CIDM_6325_Lawson_Retry
git checkout Final_Project
```

3. **Create virtual environment**:
```bash
mkvirtualenv --python=python3.10 homecompass
pip install -r requirements.txt
```

4. **Setup database**:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_tasks
python manage.py collectstatic
```

5. **Configure web app** via PythonAnywhere dashboard:
   - WSGI file: Point to `home_maintenance_compass.wsgi`
   - Static files: `/static/` → `staticfiles/`
   - Virtual environment: Path to your virtualenv

**Note**: PythonAnywhere uses MySQL/SQLite by default. You'll need to update `settings.py` database configuration accordingly.

---

## Submission Checklist for Class

Before submitting your project:

- [ ] **Deployment URL** added to README.md
- [ ] **App is accessible** and fully functional
- [ ] **Admin account** created (provide credentials to instructor)
- [ ] **Test data** seeded (maintenance tasks)
- [ ] **All features working**: registration, home profiles, schedules, tips, blog posts
- [ ] **Static files** loading correctly
- [ ] **RUBRIC_COMPLIANCE.md** updated with deployment verification
- [ ] **Screenshot** of live site (optional but recommended)
- [ ] **Video demo** (if required by your course)

---

## Additional Resources

### Documentation
- **Render Django Guide**: https://render.com/docs/deploy-django
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- **WhiteNoise Documentation**: http://whitenoise.evans.io/

### Monitoring
- **Render Dashboard**: View logs, metrics, and shell access
- **Django Admin**: Monitor users, data, and content at `/admin/`

### Support
- **Render Community**: https://community.render.com/
- **Django Forum**: https://forum.djangoproject.com/

---

## Cost Considerations

### Free Tier Includes
- ✅ 750 hours/month web service (sufficient for one app 24/7)
- ✅ 1GB PostgreSQL database
- ✅ Automatic SSL certificates
- ✅ Automatic deployments from GitHub

### Limitations
- ⚠️ Database expires after 90 days (backup/migrate for long-term)
- ⚠️ Service spins down after 15 minutes inactivity
- ⚠️ Limited concurrent requests on free tier

### Paid Upgrades (Optional)
- **Web Service**: $7/month for always-on, no spin-down
- **Database**: $7/month for persistent database beyond 90 days

For a school project, the free tier is perfect! ✨

---

**Last Updated**: November 26, 2025  
**Django Version**: 5.2.7  
**Python Version**: 3.12.0  
**Deployment Platform**: Render.com