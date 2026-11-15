# WordPress: Block Themes & Custom Blocks

Use for clients who need to edit content themselves in WordPress. Modern WordPress = **block themes** (Full Site Editing) + **blocks** (Gutenberg). Avoid classic PHP themes and page builders for new work unless the client already uses them.

## Local setup
```bash
npx @wordpress/env start          # Docker-based WP at http://localhost:8888 (admin / password)
```
`.wp-env.json` in the project maps the theme/plugin into the site:
```json
{ "themes": ["./my-theme"], "plugins": ["./my-blocks"] }
```

## Block theme structure (`templates/wordpress-block-theme`)
```
my-theme/
  style.css            theme header (Theme Name, Version, Requires at least, Text Domain…)
  theme.json           design tokens + settings + global styles (version 3)
  functions.php        enqueue editor/front styles, register pattern categories, block styles
  templates/           index.html, home.html, single.html, page.html, archive.html, 404.html, search.html
  parts/               header.html, footer.html
  patterns/            PHP files with a header comment → reusable sections (hero, features, CTA)
  styles/              alternative style variations (dark.json, …)
```

### theme.json essentials
- `settings.color.palette`, `settings.typography.fontFamilies` (with `fontFace` for self-hosted fonts), `settings.typography.fontSizes` (use `fluid`), `settings.spacing.spacingSizes`, `settings.layout.contentSize` / `wideSize`.
- Turn off what clients shouldn't change: `"custom": false`, `"customGradient": false`, `"defaultPalette": false`.
- `styles` sets global defaults and per-element/per-block styles (`styles.elements.button`, `styles.blocks["core/navigation"]`).
- Reference tokens as `var(--wp--preset--color--primary)` / `var:preset|color|primary` inside block markup.

### Templates & parts
Block markup (HTML comments) — e.g. `templates/index.html`:
```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group"><!-- wp:query {"queryId":1,"query":{"perPage":10,"postType":"post","inherit":true}} -->
<div class="wp-block-query"><!-- wp:post-template --><!-- wp:post-title {"isLink":true} /--><!-- wp:post-excerpt /--><!-- /wp:post-template --><!-- wp:query-pagination /--></div>
<!-- /wp:query --></main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```
Tip: design in the Site Editor, then copy the generated markup into files (or use the Create Block Theme plugin to export).

### Patterns
`patterns/hero.php`:
```php
<?php
/**
 * Title: Hero
 * Slug: my-theme/hero
 * Categories: featured, banner
 * Keywords: hero, intro
 */
?>
<!-- wp:cover {"dimRatio":40,"minHeight":70,"minHeightUnit":"vh","align":"full"} --> … <!-- /wp:cover -->
```
Use `esc_html_e()` / `esc_attr_e()` for translatable strings.

## Custom blocks (plugin)
```bash
npx @wordpress/create-block@latest my-blocks --variant dynamic   # scaffolds block.json, edit.js, render.php, build tooling
cd my-blocks && npm start                                         # watch build
```
### block.json (source of truth)
```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "my/testimonial",
  "title": "Testimonial",
  "category": "widgets",
  "icon": "format-quote",
  "attributes": {
    "quote":  { "type": "string", "source": "html", "selector": "blockquote p" },
    "author": { "type": "string", "default": "" },
    "rating": { "type": "number", "default": 5 }
  },
  "supports": { "html": false, "align": ["wide", "full"], "color": { "background": true, "text": true }, "spacing": { "padding": true } },
  "textdomain": "my-blocks",
  "editorScript": "file:./index.js",
  "style": "file:./style-index.css",
  "render": "file:./render.php"
}
```
### Static vs dynamic
| Static (`save.js`) | Dynamic (`render.php`) |
|---|---|
| Markup saved into post content | Rendered on each request |
| Fast, but changing `save` breaks existing blocks → needs **deprecations** | Safe to change output; use for lists, latest posts, data from APIs |

### Editing UI
- `useBlockProps()` on the wrapper (both edit and save / `get_block_wrapper_attributes()` in PHP).
- `RichText` for editable text, `InspectorControls` + `PanelBody` + components (`TextControl`, `RangeControl`, `ToggleControl`) for settings, `MediaUpload` for images, `InnerBlocks` for nested content (+ `allowedBlocks`, `template`).
- Escape everything in PHP: `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`.

### Deprecations (static blocks)
When `save` output changes, add the old version to `deprecated: [{ attributes, save }]` (newest first) — with `migrate` if attributes changed. Otherwise existing posts show "This block contains unexpected or invalid content".

### Block styles & variations
- `register_block_style( 'core/button', [ 'name' => 'pill', 'label' => 'Pill' ] )` + CSS `.is-style-pill`.
- Variations (`registerBlockVariation`) for preconfigured versions of a block (e.g. "Pricing card" group).

## Quality checklist
- [ ] Theme passes Theme Check; no PHP notices with `WP_DEBUG` on
- [ ] All tokens in theme.json, editor matches front end
- [ ] Patterns for every common section so clients never start from blank
- [ ] Blocks: escaped output, i18n text domain, deprecations for changed static blocks
- [ ] Accessibility: skip link, landmarks, focus styles, color contrast
- [ ] Performance: no jQuery on front end unless needed, fonts self-hosted via theme.json
