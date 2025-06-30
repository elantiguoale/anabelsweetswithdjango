# 🚀 Heroku Deployment Guide for Anabel Sweets

## Prerequisites
- Git installed
- Python 3.11+ installed
- Heroku account (free tier available)

## Step 1: Install Heroku CLI

### Windows (PowerShell)
```powershell
# Download and install from: https://devcenter.heroku.com/articles/heroku-cli
# Or use winget:
winget install --id=Heroku.HerokuCLI
```

### Alternative: Download from Website
1. Go to: https://devcenter.heroku.com/articles/heroku-cli
2. Download the Windows installer
3. Run the installer and follow the prompts

## Step 2: Login to Heroku

```bash
heroku login
```
- This will open your browser
- Click "Log in" to authorize Heroku CLI

## Step 3: Create Heroku App

```bash
# Create a new Heroku app (replace 'your-app-name' with a unique name)
heroku create your-app-name

# Example:
heroku create anabelsweets-bakery
```

**Important:** Note your app name! You'll need it for the next steps.

## Step 4: Update Django Settings

Edit `sweets/settings.py` and replace the placeholder with your actual app name:

```python
ALLOWED_HOSTS = ['127.0.0.1',
                'anabelsweets-91c553d97f87.herokuapp.com',
                'your-actual-app-name.herokuapp.com',  # Replace this
                'localhost']

CSRF_TRUSTED_ORIGINS = [
    "https://8000-elantiguoal-anabelsweet-lpiv62gd258.ws-eu116.gitpod.io",
    "https://anabelsweets-91c553d97f87.herokuapp.com/",
    "https://your-actual-app-name.herokuapp.com"  # Replace this
]
```

## Step 5: Set Environment Variables

```bash
# Set your Django secret key
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Set development flag (optional, for debugging)
heroku config:set DEVELOPMENT="True"

# Example secret key (generate your own):
heroku config:set SECRET_KEY="django-insecure-your-very-long-secret-key-here"
```

## Step 6: Add PostgreSQL Database

```bash
# Add PostgreSQL addon (free tier)
heroku addons:create heroku-postgresql:mini
```

## Step 7: Deploy Your Code

```bash
# Add all files to git
git add .

# Commit changes
git commit -m "Prepare for Heroku deployment"

# Push to Heroku
git push heroku main
```

## Step 8: Run Database Migrations

```bash
# Apply database migrations
heroku run python manage.py migrate

# Create a superuser (optional)
heroku run python manage.py createsuperuser
```

## Step 9: Test Your Deployment

```bash
# Open your app in browser
heroku open

# Or visit: https://your-app-name.herokuapp.com
```

## Step 10: Verify Everything Works

1. **Home Page**: Should load without errors
2. **Navigation**: All links should work
3. **Forms**: Test order form and registration
4. **Admin**: Visit `/admin/` and login
5. **Static Files**: Images and CSS should load

## Troubleshooting

### If you get errors:

1. **Check logs:**
   ```bash
   heroku logs --tail
   ```

2. **Common issues:**
   - **Static files not loading**: Run `heroku run python manage.py collectstatic --noinput`
   - **Database errors**: Check if migrations ran: `heroku run python manage.py migrate`
   - **App not found**: Verify your app name in settings.py

3. **Restart the app:**
   ```bash
   heroku restart
   ```

## Environment Variables Summary

Your app needs these environment variables set in Heroku:
- `SECRET_KEY`: Your Django secret key
- `DATABASE_URL`: Automatically set by PostgreSQL addon
- `DEVELOPMENT`: Set to "True" for debugging (optional)

## Final Steps

1. **Update your README** with the live URL
2. **Test all functionality** on the live site
3. **Share your deployed app** with others!

## Your Live App URL

Once deployed, your app will be available at:
**https://your-app-name.herokuapp.com**

## Need Help?

- **Heroku Documentation**: https://devcenter.heroku.com/
- **Django on Heroku**: https://devcenter.heroku.com/articles/django-app-configuration
- **Check logs**: `heroku logs --tail`

---

**Congratulations!** 🎉 Your Django bakery app is now live on the internet! 