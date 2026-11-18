#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HUGO_BIN=${1:-hugo}
EXPECTED=$(tr -d '\r\n' < "$ROOT/HUGO_VERSION")
case "$EXPECTED" in
  *[!0-9.]*|'') echo "Invalid Hugo version pin: $EXPECTED" >&2; exit 1 ;;
esac
ACTUAL=$("$HUGO_BIN" version 2>&1) || {
  echo "Hugo is unavailable: $ACTUAL" >&2
  exit 1
}
case "$ACTUAL" in
  *"v$EXPECTED"*) echo "Hugo version verified: $EXPECTED" ;;
  *) echo "Expected Hugo $EXPECTED, got: $ACTUAL" >&2; exit 1 ;;
esac
