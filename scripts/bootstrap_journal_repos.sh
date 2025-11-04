#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 --journal <paper-journal-A|paper-journal-B> --target <output-dir> --primary <git-url> --overleaf <git-url>

Creates a self-contained Git repository for the selected journal template, commits the initial layout, and registers
primary (GitHub/GitLab) and Overleaf remotes.
USAGE
}

JOURNAL=""
TARGET=""
PRIMARY=""
OVERLEAF=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --journal)
      JOURNAL="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --primary)
      PRIMARY="$2"
      shift 2
      ;;
    --overleaf)
      OVERLEAF="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$JOURNAL" || -z "$TARGET" || -z "$PRIMARY" || -z "$OVERLEAF" ]]; then
  echo "Missing required argument." >&2
  usage
  exit 1
fi

ROOT_DIR="$(git rev-parse --show-toplevel)"
SOURCE_DIR="$ROOT_DIR/$JOURNAL"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Journal directory '$JOURNAL' not found under $ROOT_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET"
DEST="$TARGET/$(basename "$JOURNAL")"
rm -rf "$DEST"
rsync -a --exclude='.git' "$SOURCE_DIR/" "$DEST/"

pushd "$DEST" > /dev/null

git init -b main

git add .
git commit -m "Initial commit for $(basename "$JOURNAL")"

git remote add origin "$PRIMARY"
git remote add overleaf "$OVERLEAF"

git remote -v

popd > /dev/null

echo "Created independent repository at $DEST"
