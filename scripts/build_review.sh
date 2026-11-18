#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HUGO_BIN=${1:-hugo}
BACKUP=../backup-4.10.2023_17-56-43_bbsali0
SQL="$ROOT/$BACKUP/mysql/bbsali0_wrdp1.sql"
UPLOADS="$ROOT/$BACKUP/homedir/public_html/wp-content/uploads"
THEME_DIR="$ROOT/themes/hugo-theme-cleanwhite"
THEME_PIN=$(tr -d '\r\n' < "$ROOT/THEME_COMMIT")

cd "$ROOT"
"$ROOT/scripts/check_hugo_version.sh" "$HUGO_BIN"
"$ROOT/scripts/install_theme.sh"
THEME_ACTUAL=$(git -C "$THEME_DIR" rev-parse HEAD)
[ "$THEME_ACTUAL" = "$THEME_PIN" ] || {
  echo "CleanWhite pin mismatch: expected $THEME_PIN, found $THEME_ACTUAL" >&2
  exit 1
}

python3 scripts/convert.py --sql "$SQL" --uploads "$UPLOADS"
python3 scripts/recover_missing_media.py --sql "$SQL" --uploads "$UPLOADS"
# Re-run conversion after recovery so the ignored review tree contains only
# recovered media that belongs to explicitly published, unprotected articles.
python3 scripts/convert.py --sql "$SQL" --uploads "$UPLOADS"
python3 scripts/import_live_recoveries.py
python3 scripts/audit_migration_sources.py --sql "$SQL" --uploads "$UPLOADS" --review-dir migration-review/generated
python3 scripts/compare_conversion.py --sql "$SQL" --uploads "$UPLOADS"
python3 scripts/prepare_review_content.py
"$HUGO_BIN" --config hugo.toml,config/review.toml --environment review \
  --destination migration-review/site --buildDrafts --cleanDestinationDir --gc --minify
python3 scripts/audit_site.py --site migration-review/site --mode review \
  --base-url http://localhost:1313/ --require-content \
  --report migration-review/site-audit.json
python3 scripts/security_audit.py --repo . --site migration-review/site --include-index --include-history
