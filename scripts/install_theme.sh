#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
THEME_DIR="$ROOT/themes/hugo-theme-cleanwhite"
THEME_URL=https://github.com/zhaohuabing/hugo-theme-cleanwhite.git
PIN=$(tr -d '\r\n' < "$ROOT/THEME_COMMIT")

case "$PIN" in
  *[!0-9a-f]*|'') echo "Invalid CleanWhite commit pin" >&2; exit 1 ;;
esac
[ "${#PIN}" -eq 40 ] || { echo "CleanWhite pin must be a full commit SHA" >&2; exit 1; }

if [ -d "$THEME_DIR/.git" ]; then
  CURRENT=$(git -C "$THEME_DIR" rev-parse HEAD)
  if [ "$CURRENT" = "$PIN" ]; then
    echo "CleanWhite already installed at $PIN"
    exit 0
  fi
  echo "Refusing to replace $THEME_DIR at $CURRENT; remove that checkout to install the pinned commit." >&2
  exit 1
fi

if [ -e "$THEME_DIR" ] && [ -n "$(find "$THEME_DIR" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
  echo "Refusing to overwrite nonempty theme directory: $THEME_DIR" >&2
  exit 1
fi

mkdir -p "$ROOT/themes"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/networkstatic-cleanwhite.XXXXXX")
trap 'rm -rf "$TMP"' EXIT HUP INT TERM
git clone --quiet --filter=blob:none --no-checkout "$THEME_URL" "$TMP/theme"
git -C "$TMP/theme" fetch --quiet --depth 1 origin "$PIN"
git -C "$TMP/theme" checkout --quiet --detach "$PIN"
ACTUAL=$(git -C "$TMP/theme" rev-parse HEAD)
[ "$ACTUAL" = "$PIN" ] || { echo "CleanWhite checkout mismatch: $ACTUAL" >&2; exit 1; }
rm -rf "$THEME_DIR"
mv "$TMP/theme" "$THEME_DIR"
echo "Installed CleanWhite at $ACTUAL"
