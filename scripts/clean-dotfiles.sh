#!/usr/bin/env bash
# clean-dotfiles.sh — remove macOS AppleDouble (._*) and .DS_Store junk.
#
# Why these exist: this repo lives on an NFS mount (fuse-t) that can't store
# macOS extended attributes inline, so the OS spills them into ._<name>
# sidecar files. They're harmless but clutter the tree and the editor, and
# macOS regenerates them on the fly while writing — so re-run this as needed.
# .gitignore already keeps them out of git; this is just local cleanup.
#
# Usage:
#   ./scripts/clean-dotfiles.sh [DIR]   # DIR defaults to the current directory

set -eu

TARGET="${1:-.}"

if [ ! -d "$TARGET" ]; then
  echo "error: '$TARGET' is not a directory" >&2
  exit 1
fi

# How much junk is there? (skip .git internals)
before=$(find "$TARGET" -not -path '*/.git/*' \( -name '._*' -o -name '.DS_Store' \) 2>/dev/null | wc -l | tr -d ' ')
before=${before:-0}

if [ "$before" -eq 0 ]; then
  echo "Nothing to clean in '$TARGET'."
  exit 0
fi

# dot_clean -m: always delete ._* (don't merge xattrs back — the NFS mount
# can't keep them anyway). It only touches ._*, so .DS_Store is handled below.
dot_clean -m "$TARGET"

# Remove .DS_Store plus any ._* dot_clean left behind (e.g. orphans).
find "$TARGET" -not -path '*/.git/*' \( -name '._*' -o -name '.DS_Store' \) -delete 2>/dev/null || true

echo "Cleaned $before macOS junk file(s) from '$TARGET'."
