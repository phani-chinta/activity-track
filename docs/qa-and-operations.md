# QA and operations guide

## Quality strategy

The primary safety property is tenant isolation: each signed-in user can only access their own task data. Automated Django tests cover representative user and task flows; manual checks cover responsive presentation and live Supabase/Vercel integration.

### Automated coverage

Run from the project root:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Current automated tests cover:

- Redirecting a signed-out visitor away from the dashboard.
- Registration creating and authenticating an account.
- Owner CRUD: create, edit, mark complete, and delete.
- Another user's detail/edit/delete attempts returning 404 without deleting data.
- Dashboard counts and overdue count scoped to the signed-in user.
- Combined search/priority/status filtering without exposing a second user's matching task.
- Completed past-due tasks not being classified as overdue.

Latest test run: **7 tests passed** on the local SQLite test database; Django system check passed and no model migration changes were pending. Static collection also completed. This does not verify the live Supabase or Vercel services.

### Manual acceptance / release smoke test

1. Use a fresh account; register and confirm the dashboard loads.
2. Create a task with each priority/status and a due date in the future.
3. Search a substring of its title, combine filters, and switch sort order.
4. Edit the task and check timestamps/status; mark complete.
5. Check dashboard totals, upcoming exclusions, and completed state.
6. In a separate account, try the known task URL; it must return 404.
7. Test a past-due open task and a past-due completed task; only the open task is overdue.
8. Verify deletion is shown as a confirmation and only happens after POST.
9. Update profile and change password; log out using the navigation action.
10. Inspect mobile widths and use keyboard-only navigation.

### Security/release checks

- `DEBUG=False`; production secret is unique and kept in Vercel settings.
- `ALLOWED_HOSTS` contains the deployed/custom hosts; CSRF origins use full HTTPS origins.
- `DATABASE_URL` is Supabase PostgreSQL pooler URL with TLS; no client anon/service key is used by Django.
- Vercel system values are exposed so the project can include generated Vercel hostnames.
- Migrations are applied explicitly before a release uses a changed schema.
- No credentials, `.env`, or database dumps enter Git.
- Review Django/Vercel/Supabase advisories and update dependencies on a planned cadence.

## Production release runbook

1. Merge the reviewed commit to the Vercel production branch (or promote a verified deployment).
2. Confirm production/preview environment values are set in Vercel. Changing an environment variable requires a new deployment.
3. From a trusted environment with production `DATABASE_URL`, run `python manage.py migrate` and verify it exits successfully. Keep the URL private.
4. Confirm Vercel build/collectstatic succeeds; the app's `STATIC_ROOT` is configured.
5. Smoke-test login, task CRUD, filters, owner isolation, and static assets on the deployment URL.
6. Check runtime logs for 4xx/5xx and database connection errors.
7. Record commit, migration state, environment, checks, and any follow-up issue.

## Incident triage

| Symptom | First checks |
|---|---|
| `DisallowedHost` / 400 | Check `ALLOWED_HOSTS`; Vercel system hosts must be exposed; redeploy after env changes |
| Error parsing `DATABASE_URL` | Copy Supabase URI exactly; pooler DNS host is not bracketed; URL-encode reserved password characters |
| 500 on registration | Read Vercel runtime traceback; confirm Supabase is reachable and `auth_user` migrations were applied |
| `relation ... does not exist` | Run `python manage.py showmigrations` against the target DB, then apply `python manage.py migrate` once |
| Duplicate task table after manual SQL | Do not drop tables blindly; check `django_migrations` and reconcile schema/history with a reviewed migration plan |
| Static files missing | Check Vercel build logs for `collectstatic`, `STATIC_ROOT`, CDN paths, and asset manifest |
| Wrong user's task visible | Treat as a security incident; disable the affected route/deployment if necessary; inspect queryset scoping and add regression coverage |

Do not return raw database traces or credentials to users. Use the Vercel runtime log to identify the underlying exception and report a sanitized message to the product owner.

## Recovery and maintenance

- Configure Supabase automated backups/point-in-time recovery based on the account's available plan and recovery needs.
- Periodically test a restore in a separate database before relying on it.
- Keep migrations additive where possible; take/confirm a recoverable database point before risky schema changes.
- Roll back an application deployment through Vercel if a release breaks request handling. Database rollback requires a planned reverse migration or restore; do not assume code rollback reverses data changes.
- Review dependency releases and security advisories at least monthly and before a public event/demo.
- Monitor Vercel function error logs and Supabase connection/usage limits after launches.
