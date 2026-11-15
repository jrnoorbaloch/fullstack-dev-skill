# Changelog

All notable changes to this project are documented here. Versions follow [Semantic Versioning](https://semver.org/).

## [2.1.0] — 2026-11-15
### Added
- **Skill packs**: `fullstack-web`, `fullstack-mobile`, `fullstack-desktop`, `fullstack-motion-3d`, `fullstack-wordpress`, `fullstack-video`, generated from the complete skill by `tools/build_packs.py` (configured in `packs.json`). Each is a Claude Code plugin in the marketplace and a separate zip on every release.
- **npm installer** (`bin/cli.js`, zero dependencies): `list`, `install [pack]`, `uninstall`, `zip` with `--project`, `--dir`, `--force`, `-o`. Works today with `npx github:jrnoorbaloch/fullstack-dev-skill`.
- **pip installer** (`fullstack_dev_skill`): the same commands, installable with `pip install git+https://github.com/jrnoorbaloch/fullstack-dev-skill`.
- Release workflow attaches 7 skill zips, the npm tarball and the Python wheel/sdist; optional automatic publishing to npm (`NPM_TOKEN` secret) and PyPI (trusted publishing + `PUBLISH_PYPI` variable).
- CI checks that packs are up to date, versions agree, and runs installer tests for npm and Python.

## [2.0.0] — 2026-11-15
### Added
- **GSAP animation** guide (`animation-gsap.md`): timelines, ScrollTrigger (pinning, scrubbing, horizontal scroll, batch), SplitText, Flip, Draggable, SVG plugins, `useGSAP` for React, `gsap.matchMedia()` reduced-motion pattern, performance rules and ready-made recipes.
- **Three.js / React Three Fiber** guide (`threejs.md`): scene skeletons, glTF pipeline, interaction, performance budget, fallbacks.
- **React patterns** guide (`react-patterns.md`): best practices (waterfalls, bundle size, rendering, state), composition patterns (compound components, slots, `asChild`, headless hooks), View Transitions.
- **Tailwind design system** guide (`tailwind-system.md`): v4 `@theme` tokens, semantic colors, `cva` + `cn`, component layers.
- **UI constraints** guide (`ui-constraints.md`): hard rules for layout, typography, color, interaction, motion, content and accessibility.
- **Artifacts** (`artifacts.md`), **Slides** (`slides.md`), **Remotion** (`remotion.md`) and **WordPress** (`wordpress.md`) guides.
- **Templates**: `react-vite-shadcn` (React 19 + Vite + Tailwind v4 + shadcn-style UI + GSAP → single-file build), `html-slides` (animated GSAP deck), `wordpress-block-theme` (block theme + dynamic Testimonial block plugin), `remotion-video` (promo in 16:9 and 9:16).
- **Slash commands**: `/new-animated-site`, `/new-3d`, `/new-artifact`, `/new-slides`, `/new-video`, `/new-wordpress`.
- **Examples**: *Aurora* 3D product landing page (Three.js + GSAP) and an animated *pitch deck*.
- 6 new prompt-library sections (animated sites, 3D, artifacts, presentations, videos, WordPress).
- Credits section linking the skills that inspired v2.

### Changed
- `SKILL.md` routes to the new guides/templates and adds a motion quality rule.
- `scaffold.py` fills placeholders in `.php` and `.scss` files.
- CI validates and builds the new templates.

## [1.1.0] — 2026-11-15
### Added
- **Starter templates**: `landing-page`, `nextjs-saas` (Next.js 15 + Supabase, auth, RLS, tests), `expo-app` (Expo Router), `fastapi-api` (JWT + CRUD + tests), `python-desktop-pos` (Tkinter + SQLite POS).
- **Helper scripts**: `scaffold.py`, `verify.py`, `gen_env_example.py`.
- **Slash commands** for Claude Code: `/new-website`, `/new-webapp`, `/new-mobile`, `/new-desktop`, `/new-api`, `/fix-bug`, `/review`, `/deploy`.
- **Guides**: design system, payments (Stripe, PayPal, JazzCash, Easypaisa, COD…), industry blueprints, AI features with the Claude API, SEO & performance, testing.
- **Examples** with live demos and screenshots: Ali Bakery (English/Urdu) and Spendly expense tracker.
- README translations: Urdu, Hindi, Arabic, Spanish.
- GitHub Actions: skill validation, automatic release zip, GitHub Pages for demos.
- `CONTRIBUTING.md`, issue and pull request templates.

## [1.0.0] — 2026-11-15
### Added
- Initial `fullstack-developer` skill with web, backend/database, mobile, desktop and deploy references.
- Prompt library (`PROMPTS.md`).
- Claude Code plugin and marketplace manifests.
