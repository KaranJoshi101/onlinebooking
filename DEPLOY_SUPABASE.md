# 🚀 Deploy to Supabase - Complete Guide

Your Flask application is now configured to use Supabase PostgreSQL. Follow these steps to deploy.

## ✅ What's Configured

- ✓ `.env` file with Supabase credentials
- ✓ `main.py` updated for PostgreSQL support
- ✓ Migration scripts ready (SQLite → Supabase)
- ✓ Validation scripts prepared
- ✓ Connection string from Supabase loaded

---

## 🎯 Deployment Options

### Option A: Deploy to Vercel (Recommended for this project)

Your `vercel.json` is already configured. Just add Supabase environment variables.

#### Step 1: Connect to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

#### Step 2: Add Environment Variables in Vercel Dashboard

1. Go to https://vercel.com
2. Select your project
3. Settings → Environment Variables
4. Add:
   ```
   DB_USER=postgres
   DB_PASSWORD=a-g4SGTknzENbpu
   DB_HOST=db.stpowaxbrnwtwjmzpvim.supabase.co
   DB_PORT=5432
   DB_NAME=postgres
   USE_POSTGRES=True
   SECRET_KEY=your-secret-key
   ```

#### Step 3: Redeploy
```bash
vercel --prod
```

✅ **Done!** Your app is now live using Supabase PostgreSQL.

---

### Option B: Deploy to Heroku

#### Step 1: Prepare app

```bash
# Install Heroku CLI
# Create account at heroku.com

# Login
heroku login

# Create app
heroku create your-app-name
```

#### Step 2: Add Supabase Config

```bash
heroku config:set DB_USER=postgres
heroku config:set DB_PASSWORD=a-g4SGTknzENbpu
heroku config:set DB_HOST=db.stpowaxbrnwtwjmzpvim.supabase.co
heroku config:set DB_PORT=5432
heroku config:set DB_NAME=postgres
heroku config:set USE_POSTGRES=True
heroku config:set SECRET_KEY=your-secret-key
```

#### Step 3: Deploy

```bash
git push heroku main
```

---

### Option C: Deploy to Other Platforms (Railway, Fly.io, etc.)

All require the same environment variables:

```
DB_USER=postgres
DB_PASSWORD=a-g4SGTknzENbpu
DB_HOST=db.stpowaxbrnwtwjmzpvim.supabase.co
DB_PORT=5432
DB_NAME=postgres
USE_POSTGRES=True
```

---

## 🏠 Local Development with Supabase

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables (Windows PowerShell)
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "a-g4SGTknzENbpu"
$env:DB_HOST = "db.stpowaxbrnwtwjmzpvim.supabase.co"
$env:DB_PORT = "5432"
$env:DB_NAME = "postgres"
$env:USE_POSTGRES = "True"

# 3. Run app
python main.py

# 4. Visit http://localhost:5000
```

### Or use .env file

```bash
# .env is already configured, just run:
python main.py
```

---

## 📊 Supabase Dashboard

Monitor your database at: https://supabase.com

### View Data

1. Login to Supabase
2. Select your project
3. Go to Database → SQL Editor
4. Run queries:

```sql
-- View all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Count records
SELECT COUNT(*) FROM hospital;
SELECT COUNT(*) FROM doctor;
SELECT COUNT(*) FROM patient;

-- Monitor database size
SELECT pg_size_pretty(pg_database_size('postgres'));
```

### Backup Data

```bash
# Automatic backups included in Supabase Pro plan
# Manual backup:
pg_dump -U postgres -h db.stpowaxbrnwtwjmzpvim.supabase.co -d postgres > backup.sql

# Restore:
psql -U postgres -h db.stpowaxbrnwtwjmzpvim.supabase.co -d postgres < backup.sql
```

---

## 🔐 Security for Production

### Required Steps

1. **Change default password** (if not already done)
   ```sql
   ALTER USER postgres WITH PASSWORD 'new-secure-password';
   ```

2. **Update .env** with new password

3. **Enable SSL** in Supabase (default: enabled)

4. **Set up Row Level Security (RLS)** for sensitive tables

5. **Never commit credentials** to git
   - .env is in .gitignore ✓

6. **Use environment variables** on production servers
   - Don't put credentials in code ✓

---

## 🚀 Pre-Deployment Checklist

- [ ] `.env` file configured with Supabase credentials
- [ ] SQLite data migrated to Supabase (via migration script)
- [ ] Application tested locally
- [ ] `main.py` has `USE_POSTGRES=True`
- [ ] All environment variables set correctly
- [ ] Supabase connection tested
- [ ] Dependencies in `requirements.txt` complete
- [ ] `vercel.json` configured (if using Vercel)
- [ ] `.gitignore` includes `.env` ✓
- [ ] Secret keys are strong and random

---

## 🧪 Test Before Deploying

```bash
# 1. Test connection
python test_supabase_connection.py

# 2. Test application
python main.py

# 3. Test features
# Visit http://localhost:5000
# - Login
# - Create appointment
# - View data
# - All features working?
```

---

## 📈 Monitoring in Production

### Application Logs
- **Vercel**: Dashboard → Deployments → Logs
- **Heroku**: `heroku logs --tail`
- **Others**: Check platform documentation

### Database Monitoring
- Supabase Dashboard → Database → Monitoring
- View connections, queries, performance

### Set Alerts
- Supabase → Database → Alerts
- Email notifications for issues

---

## 🔄 Deployment Commands

### Vercel
```bash
vercel          # Deploy to preview
vercel --prod   # Deploy to production
vercel rollback # Rollback to previous
```

### Heroku
```bash
git push heroku main     # Deploy
heroku logs --tail       # View logs
heroku releases          # See deployment history
heroku rollback          # Rollback
```

---

## 🐛 Troubleshooting Deployment

### "Database connection failed"
1. Verify environment variables set on platform
2. Check Supabase firewall settings
3. Test local connection first

### "Application crashes on startup"
1. Check logs for errors
2. Verify all environment variables present
3. Ensure database credentials correct

### "Data not displaying"
1. Verify migration completed successfully
2. Check database has tables and data
3. Review application logs

---

## 📝 Environment Variables Reference

Required for production:

```
DB_USER=postgres
DB_PASSWORD=a-g4SGTknzENbpu
DB_HOST=db.stpowaxbrnwtwjmzpvim.supabase.co
DB_PORT=5432
DB_NAME=postgres
USE_POSTGRES=True
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
```

Optional:

```
UPLOAD_FOLDER=./static/images
```

---

## 🎯 Post-Deployment

### 1. Test Live Application
- Visit your deployed URL
- Test all features
- Verify data displays correctly

### 2. Monitor Logs
- Check for errors
- Monitor database usage
- Set up alerts

### 3. Set Up Backups
- Configure automated backups in Supabase
- Test backup restore procedure

### 4. Performance Optimization
- Monitor query performance
- Add indexes if needed
- Optimize slow queries

---

## 📚 Additional Resources

- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL on Supabase**: https://supabase.com/docs/guides/database
- **Vercel Deployment**: https://vercel.com/docs
- **Heroku Deployment**: https://devcenter.heroku.com/

---

## 🎉 You're Ready to Deploy!

Your application is fully configured for Supabase PostgreSQL deployment.

### Quick Deployment Path
1. ✅ Configure environment variables
2. ✅ Test locally
3. ✅ Deploy to your platform
4. ✅ Monitor and celebrate

---

**Created:** May 9, 2026  
**For:** Flask + Supabase PostgreSQL  
**Status:** ✅ Ready for Production Deployment
