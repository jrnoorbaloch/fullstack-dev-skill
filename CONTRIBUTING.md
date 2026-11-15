# Contributing

Thanks for helping make this skill better! Contributions of all sizes are welcome.

## Ways to contribute
- **Prompts** — add useful prompts to `skills/fullstack-developer/references/prompts.md` (then copy the file to `PROMPTS.md`).
- **Guides** — improve or add files in `skills/fullstack-developer/references/` (new stacks, gateways, industries).
- **Templates** — add a starter under `skills/fullstack-developer/templates/<name>/` with its own `README.md`. It must install, build and pass its tests.
- **Examples** — add a project built with the skill under `examples/<name>/` plus screenshots, and list it in `examples/README.md` and `examples/index.html`.
- **Translations** — add `README.<lang>.md` and link it at the top of `README.md`.
- **Bugs / ideas** — open an issue using the templates.

## Rules
1. Keep `SKILL.md` short; put details in `references/`.
2. No secrets, API keys or personal data in any file.
3. Templates: real working code only — no placeholders like `// TODO`. Run `python skills/fullstack-developer/scripts/verify.py <template-dir>` before opening a PR.
4. Write in clear English (translations go in `README.<lang>.md`).
5. One topic per pull request, with a short description of what changed and why.

## Local checks
```bash
python skills/fullstack-developer/scripts/scaffold.py --list
python skills/fullstack-developer/scripts/verify.py skills/fullstack-developer/templates/python-desktop-pos
```
The **Validate** GitHub Action also checks the skill structure on every pull request.

## Packs
`packs/` is generated. Edit the complete skill in `skills/fullstack-developer/` (and `packs.json` to change what a pack contains), then run:
```bash
python tools/build_packs.py          # regenerate packs/
python tools/build_packs.py --check  # what CI runs
```

## Releasing (maintainers)
1. Update `CHANGELOG.md` and bump the version in **all three** files: `package.json`, `pyproject.toml`, `.claude-plugin/plugin.json` (CI checks they match), then run `python tools/build_packs.py`.
2. Publish a GitHub Release with a new tag (e.g. `v1.2.0`), or push the tag: `git tag v1.2.0 && git push origin v1.2.0`.
3. The **Release** workflow attaches every skill zip, the npm tarball and the Python wheel automatically.

### Publishing to npm and PyPI (one-time setup)
- **npm:** create an access token on npmjs.com (Automation / granular, publish rights) → repo **Settings → Secrets and variables → Actions → New secret** `NPM_TOKEN`. Every published release then runs `npm publish`.
- **PyPI:** on pypi.org → *Your account → Publishing → Add a pending publisher*: project `fullstack-dev-skill`, owner `jrnoorbaloch`, repo `fullstack-dev-skill`, workflow `release.yml`. Then add the repository **variable** `PUBLISH_PYPI` = `true`.
