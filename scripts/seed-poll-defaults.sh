#!/bin/sh
# Writes scripts/poll-defaults.json to {polls,polls-preview}/defaults in
# Firestore. This is the only weekly-poll data the client can never write
# (see firestore.rules), so it is seeded from here instead of the console.
#
#   scripts/seed-poll-defaults.sh emulator   # local emulator on 127.0.0.1:8080
#   scripts/seed-poll-defaults.sh prod       # real gw-church project; needs
#                                            # gcloud logged in as the owner
#
# If the owner's account is not gcloud's active one, name it instead of
# switching configs:  GCLOUD_ACCOUNT=owner@example.com scripts/seed-poll-defaults.sh prod
#
# Re-run any time the theme list changes; it replaces both defaults docs.
set -eu
cd "$(dirname "$0")"

case "${1:-}" in
  emulator) BASE="http://127.0.0.1:8080"; TOKEN="owner" ;;
  prod)     BASE="https://firestore.googleapis.com"
            TOKEN="$(gcloud auth print-access-token ${GCLOUD_ACCOUNT:+--account="$GCLOUD_ACCOUNT"})" ;;
  *) echo "usage: $0 emulator|prod" >&2; exit 2 ;;
esac

BODY="$(python3 - <<'PY'
import json
d = json.load(open("poll-defaults.json"))
fields = {"themes": {"arrayValue": {"values": [{"stringValue": t} for t in d["themes"]]}}}
if d.get("examples"):
    fields["examples"] = {"mapValue": {"fields": {k: {"stringValue": v} for k, v in d["examples"].items()}}}
if d.get("closesNote"):
    fields["closesNote"] = {"stringValue": d["closesNote"]}
print(json.dumps({"fields": fields}))
PY
)"

for COLL in polls polls-preview; do
  URL="$BASE/v1/projects/gw-church/databases/(default)/documents/$COLL/defaults"
  OUT="$(curl -sS -X PATCH "$URL" -H "Authorization: Bearer $TOKEN" \
        -H 'Content-Type: application/json' -d "$BODY")"
  case "$OUT" in
    *'"name"'*) echo "seeded $COLL/defaults" ;;
    *) echo "FAILED $COLL/defaults:"; echo "$OUT"; exit 1 ;;
  esac
done
