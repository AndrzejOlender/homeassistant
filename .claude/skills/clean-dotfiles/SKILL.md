---
name: clean-dotfiles
description: >-
  Remove macOS junk files — AppleDouble sidecars (._*) and .DS_Store — from this
  Home Assistant config repo. The repo lives on an NFS mount (fuse-t) that can't
  store macOS extended attributes inline, so the OS constantly spawns ._<name>
  sidecar files and drops .DS_Store; they clutter the working tree, the editor,
  and git status. Use this skill whenever the user asks to clean up, remove, or
  get rid of "._*" files, ".DS_Store", "AppleDouble" files, "dot-underscore"
  files, or "macOS junk" — in Polish or English (e.g. "posprzątaj te ._ pliki",
  "wyczyść .DS_Store", "usuń śmieci macOS z repo", "clean the dotfiles", "remove
  AppleDouble junk"). Also use it when the user notices these files reappearing
  and wants them gone again.
allowed-tools: Bash
---

# Clean macOS dotfiles

## Why this exists

This repo is on an NFS mount (`fuse-t`) that can't store macOS extended
attributes inline. macOS therefore spills them into AppleDouble sidecar files
named `._<original>`, and also drops `.DS_Store` files. They're harmless but
clutter the working tree, the editor, and `git status`. `.gitignore` already
keeps them out of git — this skill is for clearing the *local* clutter.

## How to clean

Run the bundled script from the repo root:

```bash
./scripts/clean-dotfiles.sh
```

To clean a specific directory instead of the whole repo, pass it as an argument:

```bash
./scripts/clean-dotfiles.sh path/to/dir
```

The script runs `dot_clean -m` to delete `._*`, plus a `find` pass to remove
`.DS_Store`, skips `.git/`, and prints how many files it removed (e.g.
`Cleaned 5 macOS junk file(s) from '.'.`). Report that count back to the user.

If the script is missing its execute bit, restore it with
`chmod +x scripts/clean-dotfiles.sh` rather than reimplementing the cleanup
inline — keeping the logic in one place is the whole point of the script.

## Note on recurrence

These files come back whenever macOS writes xattrs to the mount, so re-running
this is normal and not a sign anything is broken. If the user wants them to stop
appearing *entirely*, that's an OS/mount-level concern (the NFS share not
supporting extended attributes), which the cleanup can't prevent — say so rather
than re-running in a loop.
