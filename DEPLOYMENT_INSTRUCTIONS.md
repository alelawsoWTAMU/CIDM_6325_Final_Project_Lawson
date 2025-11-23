# Deployment Instructions for Render.com

## Your Project is Ready to Deploy! 🚀

**GitHub Repository**: https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry  
**Branch**: `Final_Project`

---

## Step-by-Step Deployment Guide

### 1. Sign Up / Log In to Render.com

1. Go to: **https://render.com**
2. Click "Get Started for Free" or "Sign In"
3. **Sign in with GitHub** (recommended - makes connecting your repo easier)

### 2. Create a New Web Service

1. Once logged in, click the **"New +"** button in the top right
2. Select **"Web Service"**
3. You'll see your GitHub repositories listed
4. Find and select: **`CIDM_6325_Lawson_Retry`**
5. Select branch: **`Final_Project`**
6. Click **"Connect"**

### 3. Configure Your Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `home-maintenance-compass` (or any name you prefer)
- **Region**: Choose closest to you (e.g., Oregon USA)
- **Branch**: `Final_Project` (should auto-select)
- **Runtime**: **Python 3**

**Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn home_maintenance_compass.wsgi:application`

**Instance Type:**
- Select **"Free"** (this gives you 750 hours/month free)

### 4. Add Environment Variables

Click **"Advanced"** to expand environment variables section, then click **"Add Environment Variable"** for each:

**Required Variables:**

1. **SECRET_KEY**
   - Value: `django-insecure-YOUR_GENERATED_KEY_HERE`
   - (Use the key generated below)

2. **DEBUG**
   - Value: `False`

3. **PYTHON_VERSION**
   - Value: `3.12.0`

4. **ALLOWED_HOSTS**
   - Value: `.onrender.com,localhost,127.0.0.1`

### 5. Add PostgreSQL Database (Required)

1. Scroll down and you'll see **"Add Database"** or Render will suggest it
2. Click **"New Database"** 
3. Configure:
   - **Name**: `home_maintenance_compass_db`
   - **Database**: `home_maintenance_compass`
   - **User**: Auto-generated
   - **Region**: Same as your web service
   - **PostgreSQL Version**: 16 (or latest)
   - **Instance Type**: **Free**
4. Click **"Create Database"**

**Important**: Render will automatically create a `DATABASE_URL` environment variable that links your web service to the database. You don't need to manually add this!

### 6. Deploy!

1. Review all settings
2. Click **"Create Web Service"** at the bottom
3. Wait for deployment (typically 5-10 minutes)
4. Watch the build logs - you should see:
   - ✅ Installing dependencies from requirements.txt
   - ✅ Running collectstatic
   - ✅ Running migrations
   - ✅ Starting gunicorn server

### 7. Access Your Deployed App

Once deployed, you'll get a URL like:
```
https://home-maintenance-compass.onrender.com
```

Click on it to see your live Django application!

---

## Post-Deployment Setup

### Create Superuser Account

After deployment, you need to create an admin account:

1. In your Render dashboard, go to your web service
2. Click on **"Shell"** tab in the left sidebar
3. Click **"Launch Shell"**
4. Run these commands:
```bash
python manage.py createsuperuser
```
5. Follow prompts to create username, email, and password

### Seed Sample Data (Optional)

To add the 12 maintenance tasks:
```bash
python manage.py seed_tasks
```

### Access Admin Panel

Visit: `https://your-app-name.onrender.com/admin/`

---

## Troubleshooting

### If Deployment Fails:

1. **Check Build Logs**: Click on "Logs" tab to see detailed error messages

2. **Common Issues**:
   - **Build timeout**: Free tier has limited resources, rebuild if needed
   - **Missing DATABASE_URL**: Make sure PostgreSQL database is linked
   - **Static files 404**: Run `python manage.py collectstatic --no-input` in shell

3. **Force Redeploy**:
   - Go to "Manual Deploy" → "Clear build cache & deploy"

### If Site is Slow:

- Free tier "spins down" after 15 minutes of inactivity
- First request after spin-down takes 30-50 seconds
- Subsequent requests are fast

---

## Update Your README

After deployment, add this to your README.md:

```markdown
## 🌐 Live Demo

**Deployed Application**: https://your-app-name.onrender.com

### Test Credentials
- **Admin**: Create via shell (see deployment docs)
- **Regular User**: Register via signup page
```

---

## Alternative: Deploy to PythonAnywhere

If Render doesn't work, try PythonAnywhere (also free):

1. Go to: https://www.pythonanywhere.com
2. Sign up for free "Beginner" account
3. Upload your code via Git: 
   ```bash
   git clone https://github.com/alelawsoWTAMU/CIDM_6325_Lawson_Retry.git
   cd CIDM_6325_Lawson_Retry
   git checkout Final_Project
   ```
4. Follow their Django deployment guide

---

## Submission for Class

Once deployed, update your project with:

1. ✅ **Deployment URL** in README.md
2. ✅ **RUBRIC_COMPLIANCE.md** showing 100/100 grade
3. ✅ **Screenshot** of live site (optional but impressive)
4. ✅ **Admin credentials** (create test account for instructor)

