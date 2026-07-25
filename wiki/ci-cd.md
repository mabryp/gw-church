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
   (`gw-church-preprod`) and comments the unique URL on the PR
   (e.g. `gw-church-preprod--pr7-<hash>.web.app`). Channels expire after
   7 days; parallel PRs get separate URLs and never collide.
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

## Enforcement gap

**Branch protection on `main` is NOT enabled** — GitHub returns 403 on a
private repo under the free plan ("Upgrade to GitHub Pro or make this
repository public"). Until the repo is public or the plan upgraded, nothing
technically stops a collaborator from pushing straight to `main` (which would
auto-deploy prod); the preprod-first rule is enforced by CLAUDE.md § Deploy
and by convention. Revisit if collaborators are added.

## Targets reference

Deploy targets are committed in `.firebaserc` (`prod` → site `gw-church`,
`preprod` → site `gw-church-preprod`); per-target hosting config is the
two-entry array in `firebase.json`. See [Migration](migration.md) § Hosting
environments for URLs and the manual CLI commands.

## Sources

- Owner directives in working session, 2026-07-22.
- `.github/workflows/preview-deploy.yml`, `.github/workflows/prod-deploy.yml`,
  `.firebaserc`, `firebase.json`.
