# Engineering ownership and responsibility matrix

TaskFlow is a small Django product. It needs clear ownership, not a fictional department of specialists. During a hackathon or solo delivery, the **project maintainer** covers the engineering lead roles below and records review decisions in GitHub. The **product owner** provides scope and confirms user-facing behavior. Assign named people in this table when the team is known.

## Consolidated role model

| Department / role | Owner | Core responsibility | Deliverable |
|---|---|---|---|
| Product manager / business analyst | Product owner (name to assign) | Prioritize user needs, accept scope, resolve product questions | PRD and acceptance criteria |
| Technical lead / backend engineer | Project maintainer (name to assign) | Django patterns, route/model ownership, authorization, data integrity | Working application, migrations, technical decisions |
| Product designer / frontend engineer | Project maintainer (name to assign) | Design tokens, page hierarchy, responsive templates, accessible interactions | Templates, CSS, design-system guide |
| Database / platform engineer | Project maintainer (name to assign) | Supabase connection, migration/release process, Vercel configuration | Deployment settings and runbook |
| QA / application security reviewer | Project maintainer; product owner accepts user flow | Regression coverage, ownership checks, release smoke test | Test suite, QA report, release checklist |
| Operations / SRE | Project maintainer (name to assign) | Logs, recovery, dependency maintenance, production incident response | Operational guide and recovery notes |

No AI/ML, dedicated API, 3D, or animation department is needed: the app has no model feature or public JSON API, and an explanatory task illustration is more useful than a decorative character.

## Module responsibility and review

| Module | Responsible | Accountable / approves | Reviews |
|---|---|---|---|
| Authentication and profile | Backend engineer | Technical lead | QA/security reviewer |
| Task CRUD and owner isolation | Backend engineer | Technical lead | QA/security reviewer |
| Dashboard and query performance | Backend engineer | Technical lead | QA reviewer |
| Templates and responsive interaction | Product designer/frontend engineer | Product owner for usability | Accessibility/QA reviewer |
| Database migration and Supabase | Database/platform engineer | Technical lead | Operations reviewer |
| Vercel deploy and static assets | Platform engineer | Technical lead | QA reviewer |
| Scope and acceptance | Product manager/business analyst | Product owner | Technical lead |
| Release and incident response | Operations engineer | Project maintainer | Product owner informed |

## Dependencies and quality gates

- Product acceptance criteria precede implementation decisions.
- UI uses the route and form behavior documented in `product-and-architecture.md`.
- Schema changes require a migration and a review of owner scoping.
- Production releases require database migration status, smoke tests, and a clean Git branch.
- A task detail or mutation change is not accepted until cross-user access is checked.
- Any new external service requires a documented reason, secret-handling plan, cost/availability owner, and rollback path.

## Communication and reporting

- Track work as issues or pull requests linked to one of the milestones in the product and architecture document.
- Commit messages state the user-visible or operational change.
- The maintainer records unresolved requirements in the open decisions section; do not silently create a team feature or external dependency.
- Before a release, send the product owner a short status with included scope, checks performed, known issues, and required account-side actions.
