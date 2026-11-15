---
description: Build a WordPress block theme and/or custom Gutenberg blocks
argument-hint: "<site type, design, custom blocks needed>"
---
Use the fullstack-developer skill to build this WordPress project: $ARGUMENTS

1. Read `references/wordpress.md`.
2. Scaffold with `python scripts/scaffold.py wordpress-block-theme <dir> --set THEME_NAME="…" --set AUTHOR="…"`.
3. Put every design token in `theme.json`; build templates, parts and patterns for each section the client needs so they never start from a blank page.
4. Custom blocks: `block.json` apiVersion 3, prefer dynamic blocks (`render.php`) for data-driven output, escape all PHP output, add deprecations if a static block's `save` changes.
5. Run `php -l` on PHP files and `npm run build` in the plugin; explain `wp-env start`, activation and how to zip theme/plugin for upload.
