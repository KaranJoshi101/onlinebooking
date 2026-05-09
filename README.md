# Online Booking (Flask)

Simple online hospital appointment booking system (Flask + SQLAlchemy).

This repository contains the application, migration tools, and deployment configuration. The project prefers a single `DATABASE_URL` (Supabase pooler) for production and Vercel deployment.

**Requirements**
- Python 3.11+ (use a virtual environment)
- A PostgreSQL database (Supabase pooler recommended for Vercel)

**Quick Setup (local)**

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure environment variables (preferred: `DATABASE_URL`)

Create a `.env` file (DO NOT commit this file). Example options:

Preferred (pooler connection string):

```env
DATABASE_URL=postgresql://<USER>:<PASSWORD>@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres
```

Or split values (fallback):

```env
DB_USER=postgres
DB_PASSWORD=<PASSWORD>
DB_HOST=db.<project>.supabase.co
DB_PORT=5432
DB_NAME=postgres
```

Other required values:

```env
USE_POSTGRES=True
FLASK_ENV=production
SECRET_KEY=<generate_with_python>
UPLOAD_FOLDER=./static/images
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=<your_smtp_username>
SMTP_PASSWORD=<your_smtp_app_password>
SMTP_SENDER=<your_sender_name_or_email>
SMTP_USE_SSL=True
SMTP_USE_TLS=False
```

Generate a secure `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Migrate data (SQLite → PostgreSQL / Supabase)**

1. Verify connection to Supabase (uses `DATABASE_URL` if present)

```powershell
python verify_supabase.py
```

2. Run migration

```powershell
python migrate_sqlite_to_postgres.py
```

3. Validate migration

```powershell
python consistency_check.py
```

Notes: The migration script now quotes identifiers (so reserved names like `user` work), converts SQLite boolean-like columns to real booleans, and truncates target tables before reloading so reruns are deterministic.

**Run locally**

```powershell
python main.py
# visit http://localhost:5000
```

**Vercel Deployment (recommended using pooler)**

1. In Supabase, open **Pooler / Connection pooling** and copy the **Transaction pooler** connection string (IPv4 compatible).
2. In Vercel project settings → Environment Variables, add:

- `DATABASE_URL` = the pooler connection string
- `USE_POSTGRES` = `True`
- `FLASK_ENV` = `production`
- `SECRET_KEY` = (secure value)

3. Deploy with the Vercel CLI or through the dashboard:

```bash
npm i -g vercel
vercel
vercel --prod
```

**Troubleshooting**
- If `verify_supabase.py` fails with DNS or IPv4 issues, use the Supabase pooler (the pooler is IPv4-compatible and recommended for serverless hosts).
- If you see authentication errors, confirm the `DATABASE_URL` contains the correct pooler username and password.
- If migration reports boolean or type errors, the migration script will convert common SQLite types; ensure you are using the latest `requirements.txt` and the virtualenv is activated.
- If OTP or booking emails fail, set the SMTP variables above and use an app password from your mail provider.

**Files of interest**
- `main.py` — application entry; supports `DATABASE_URL` and fallback split env vars
- `migrate_sqlite_to_postgres.py` — migration tool (uses `DATABASE_URL` if present)
- `consistency_check.py` — post-migration validation
- `requirements.txt` — pinned dependencies

**Security**
- Never commit `.env` or secrets to git. `.gitignore` excludes `.env` by default.

If you want, I can also add a `README_QUICKSTART.md` with screenshots and troubleshooting steps for your environment.

---
Updated: May 9, 2026

