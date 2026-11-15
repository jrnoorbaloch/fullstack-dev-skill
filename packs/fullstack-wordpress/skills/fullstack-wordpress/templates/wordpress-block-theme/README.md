# WordPress Block Theme + Custom Block

- `theme/` — block theme: design tokens in `theme.json` (colors, fluid type, spacing), header/footer parts, templates (index, front-page, single, page, 404), patterns (hero, features, CTA), a **Dark** style variation and a "Pill" button style.
- `blocks-plugin/` — plugin with a dynamic **Testimonial** block (`block.json` apiVersion 3, RichText editing, star-rating control, escaped `render.php`).

## Run locally (needs Docker)
```bash
npm -g i @wordpress/env
cd blocks-plugin && npm install && npm run build && cd ..
wp-env start            # http://localhost:8888  (admin / password)
```
Activate the theme (Appearance → Themes) and the plugin. Edit with Appearance → Editor.

## Develop the block
`cd blocks-plugin && npm start` (watch). Add more blocks: `npx @wordpress/create-block@latest --no-plugin` inside `src/`.

## Ship
- Theme: zip the `theme/` folder (rename it to your theme slug) → Appearance → Themes → Upload.
- Plugin: `npm run plugin-zip` → Plugins → Add New → Upload.
