# TaskFlow

TaskFlow is a server-rendered Django task manager. Users can register, manage their own tasks, track deadlines, and see a private dashboard. The app uses Django's built-in authentication and ORM, PostgreSQL on Supabase in production, and WhiteNoise for static files.

## Architecture

- `config/` contains project settings and URL/WSGI/ASGI configuration.
- `accounts/` contains registration, profile editing, login/logout routes, and Django's password change views.
- `tasks/` contains the task model, forms, owner-scoped CRUD views, dashboard, and automated tests.
- `templates/` and `static/` contain the Bootstrap-based pages and responsive styling.
- Supabase PostgreSQL is accessed through Django's PostgreSQL backend and `DATABASE_URL`; there is no Supabase client key in the application.
- Vercel detects the Django project and serves static assets through its CDN. `vercel.json` only sets the Django framework preset.

Project handoff documents: [product and architecture](docs/product-and-architecture.md), [design system](docs/design-system.md), [engineering ownership](docs/engineering-ownership.md), and [QA and operations](docs/qa-and-operations.md). GitHub Actions runs Django checks on pushes and pull requests; Vercel's GitHub integration handles preview and production deployment.

## Local setup

Requires Python 3.12 and PostgreSQL for a production-like local setup. A fresh checkout without `DATABASE_URL` uses SQLite for local development only.

1. Create and activate a virtual environment: `python -m venv .venv` then activate it for your shell.
2. Install packages: `.\.venv\Scripts\python -m pip install -r requirements.txt` (or `pip install -r requirements.txt` with the venv active).
3. Copy `.env.example` to `.env` and fill in `SECRET_KEY` and `DEBUG=True`. Leave `DATABASE_URL` unset to use SQLite for local development. The settings module automatically reads `.env` on startup, so no extra shell export step is needed.
4. Apply migrations: `python manage.py migrate`.
5. Create an admin account if needed: `python manage.py createsuperuser`.
6. Start the app: `python manage.py runserver` and open `http://127.0.0.1:8000/`.

A minimal local `.env` (with SQLite) looks like this:

```env
SECRET_KEY=a-long-random-local-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For a production-like local setup using PostgreSQL, also set `DATABASE_URL` in `.env`. Alternatively export the variables directly in PowerShell for a session-only setup:

```powershell
$env:SECRET_KEY = "a-long-random-local-secret"
$env:DEBUG = "True"
$env:ALLOWED_HOSTS = "localhost,127.0.0.1"
```

## Environment variables

| Name | Purpose |
| --- | --- |
| `SECRET_KEY` | Django signing key. Set a unique long random value outside source control. |
| `DEBUG` | Set `False` in production. |
| `ALLOWED_HOSTS` | Comma-separated hostnames, such as `taskflow.example.com,your-app.vercel.app`. Vercel's `VERCEL_URL` and `VERCEL_PROJECT_PRODUCTION_URL` are also added automatically when available. |
| `DATABASE_URL` | PostgreSQL URL from Supabase. Use the Supabase session or transaction pooler endpoint suited to your project and deployment, with `sslmode=require`. |
| `CSRF_TRUSTED_ORIGINS` | Optional comma-separated full origins, for example `https://taskflow.example.com,https://your-app.vercel.app`. |
| `SECURE_SSL_REDIRECT` | Defaults to `True` when `DEBUG=False`; set only if the hosting proxy arrangement requires otherwise. |

Use the database connection URL from Supabase's connection settings. Keep it in local environment variables and Vercel's Environment Variables settings; never commit it or use Supabase anon/service-role keys for Django ORM access. The app uses `conn_max_age=0`, appropriate for short-lived serverless requests.

## Migrations and testing

The initial Task schema is in `tasks/migrations/0001_initial.py`. Apply schema changes deliberately with `python manage.py migrate`; production migrations are not run on web requests. Run the automated suite with `python manage.py test`. The tests cover login protection, registration, CRUD behavior, user isolation, and dashboard counts.

## Static files

WhiteNoise is enabled for local and conventional WSGI deployments. `python manage.py collectstatic --noinput` verifies/builds the manifest at `STATIC_ROOT`. Vercel's current Django integration serves static files through its CDN; the project keeps WhiteNoise as a fallback and does not require an `api/index.py` compatibility shim.

## Vercel deployment

The current Vercel Python runtime supports Python 3.12; Django is recognized as a framework, and no legacy `builds` routing is needed for this layout. `vercel.json` selects the Django framework preset. See [Vercel's Python runtime documentation](https://vercel.com/docs/functions/runtimes/python) and [Django deployment announcement](https://vercel.com/changelog/zero-configuration-django-support).

1. Push this repository to GitHub and import it as a Vercel project. Choose the production branch in Vercel's Git settings to enable automatic production deployments on pushes.
2. Add `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`, and `CSRF_TRUSTED_ORIGINS` to the appropriate Vercel environments. The current Vercel deployment hostname is picked up from `VERCEL_URL`; include any custom domain in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
3. Confirm the `DATABASE_URL` is the Supabase pooler URL and includes SSL. Do not enable SQLite in production.
4. Deploy the application. Configure the Vercel build command to run `python manage.py collectstatic --noinput` if the detected Django build does not already collect static files.
5. After configuring environment variables and before serving the new schema-dependent release, run `python manage.py migrate` as a controlled release step using a trusted environment with the same production `DATABASE_URL`. Do not run migrations on each request.
6. Verify the deployed URL: register, log in/out, create and update a task, check the dashboard and due-date indicators, and confirm an unrelated account cannot open that task.

The repository is prepared for deployment, but connecting GitHub/Vercel, setting account secrets, applying Supabase migrations, and checking a live deployment require the project owner's external accounts and credentials.

## Deployment checklist

- [ ] Supabase project created; pooler `DATABASE_URL` tested and SSL enabled.
- [ ] Vercel project connected to GitHub and production branch selected; GitHub Actions checks pass.
- [ ] Production environment variables set (`SECRET_KEY`, `DEBUG=False`, hosts, CSRF origins, database URL).
- [ ] Static collection/build succeeds.
- [ ] Controlled `migrate` command applied against production database.
- [ ] Registration, login, logout, CRUD, search/filter, dashboard, and cross-user access checked on deployed URL.
- [ ] Production domain and HTTPS behavior confirmed.

## Two-minute demo script

1. Open the landing page and create an account.
2. Show the dashboard cards and the upcoming-task list.
3. Create a high-priority task due tomorrow, then show it in the list and open its details.
4. Edit its description or status and mark it complete.
5. Use search, priority/status filters, and sorting to find it again.
6. Point out the overdue badge on a past-due open task and show that completed work is excluded from overdue counts.
7. Open Profile, change the display username/email, then show the password-change page.

## Scope notes

Vercel hosting and Supabase are external services. This source package does not claim a live deployment, connected GitHub integration, or production database migration; complete those checklist steps in the owner's accounts.
