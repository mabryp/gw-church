# CI/CD Pipeline (GitHub Actions → Firebase Hosting)

**Summary:** Git-driven deploys: PRs get temporary preview URLs for review, merging to `main` deploys production — so developers deploy via git alone, with no GCP credentials.

## Why

Owner directive (2026-07-22): all site changes are reviewed on preprod before
production, and other developers must be able to work on the site (and manage
the agent through this repo) without the owner's GCP credentials. GitHub
Actions holds the only deploy credential; developers only need write access to
the GitHub repo.

## Flow

1. **Feature branch → PR** against `main`. Any PR touching `site/` or
   `firebase.json` triggers `.github/workflows/preview-deploy.yml`, which
   deploys a **temporary preview channel** on the preprod site
   (`gw-church-preprod`) with a unique URL
   (e.g. `gw-church-preprod--pr7-<hash>.web.app`). Channels expire after
   7 days; parallel PRs get separate URLs and never collide. The URL is
   surfaced in two places on the PR (owner directive 2026-08-06 — the link
   must be apparent to all collaborators): **pinned at the top of the PR
   description** in a marker-delimited block the workflow updates on every
   push, and in the Firebase bot's comment in the conversation thread.
   Note: the live preprod URL (gw-church-preprod.web.app) does NOT change
   on PR pushes — it only re-syncs to `main` on merge.
2. **Owner reviews the preview URL.** Merging the PR is the acceptance.
3. **Merge to `main`** triggers `.github/workflows/prod-deploy.yml`, which
   deploys the `live` channel of **prod** (gw-church.org) and then re-deploys
   the `live` channel of **preprod**, keeping gw-church-preprod.web.app a
   mirror of `main`.

Wiki/log/CLAUDE.md-only commits deploy nothing (both workflows path-filter on
`site/**` and `firebase.json`). PRs from forks are skipped (no secret access);
developers should push branches to this repo.

## Credentials

- Service account: `github-action-hosting@gw-church.iam.gserviceaccount.com`
  (created 2026-07-22 via gcloud, key `bef7a02e...`).
- Roles (minimal): `roles/firebasehosting.admin`,
  `roles/serviceusage.apiKeysViewer` on project `gw-church`.
- Key stored ONLY as GitHub Actions secret
  `FIREBASE_SERVICE_ACCOUNT_GW_CHURCH` on mabryp/gw-church; the local key file
  was deleted after upload. Rotate: create a new key with
  `gcloud iam service-accounts keys create`, re-run `gh secret set`, delete
  the old key with `gcloud iam service-accounts keys delete`.
- Anyone with repo write access can trigger preprod preview deploys (intended)
  and could modify workflows — grant write access deliberately.

## Enforcement

**Branch protection on `main` is enabled** (2026-07-24, after the repo went
public — the free plan blocks protection on private repos): merging a PR
requires 1 approving review. `enforce_admins` is off, so the owner (admin) can
still push wiki/log commits directly to `main`; collaborators cannot, which is
what technically enforces the preprod-first rule for site changes.

## Targets reference

Deploy targets are committed in `.firebaserc` (`prod` → site `gw-church`,
`preprod` → site `gw-church-preprod`); per-target hosting config is the
two-entry array in `firebase.json`. See [Migration](migration.md) § Hosting
environments for URLs and the manual CLI commands.

## Sources

- Owner directives in working session, 2026-07-22.
- `.github/workflows/preview-deploy.yml`, `.github/workflows/prod-deploy.yml`,
  `.firebaserc`, `firebase.json`.
