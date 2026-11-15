# fullstack-dev-skill (Python installer)

Installs the **Full-Stack Developer skill for Claude** — or one of its focused packs — into Claude Code, or builds a zip to upload in the Claude app.

```bash
pip install fullstack-dev-skill          # or: pipx install fullstack-dev-skill
fullstack-dev-skill list
fullstack-dev-skill install                          # complete skill → ~/.claude/skills
fullstack-dev-skill install fullstack-web --project  # one pack → ./.claude/skills
fullstack-dev-skill zip fullstack-motion-3d -o motion.zip
```

Packs: `fullstack-developer` (complete), `fullstack-web`, `fullstack-mobile`, `fullstack-desktop`, `fullstack-motion-3d`, `fullstack-wordpress`, `fullstack-video`.

Docs, demos and source: https://github.com/jrnoorbaloch/fullstack-dev-skill
