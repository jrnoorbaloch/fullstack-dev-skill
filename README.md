# 🚀 Full-Stack Developer Skill for Claude

Give Claude a single prompt and it builds a complete **website, web app, SaaS, API, mobile app (Android/iOS) or desktop software** for you. Write in any language (English, Urdu, Hindi, Arabic, Spanish, etc.) and Claude replies in the same language.

## ✨ What It Can Build
| Category | Examples |
|---|---|
| 🌐 Websites | Landing pages, portfolios, business sites, blogs |
| 🧩 Web apps | SaaS, e-commerce, dashboards, booking systems, LMS, chat, AI apps |
| ⚙️ Backend | REST APIs, databases, authentication, payments |
| 📱 Mobile | React Native/Expo, Flutter → APK / Play Store / App Store |
| 🖥️ Desktop | POS, inventory, utility tools → .exe / .dmg (Tauri, Electron, Python) |
| 🚀 Deploy | Vercel, Netlify, Supabase, Docker, GitHub Actions |

Supports every major programming language: JavaScript/TypeScript, Python, PHP/Laravel, Java, C#, Go, Rust, Dart, Kotlin, Swift and more.

## 🧠 How It Works
For every request, Claude follows a senior-engineer workflow:
1. **Understand** the goal and ask only the questions that matter.
2. **Plan** features, tech stack, folder structure, data model and API.
3. **Build** every file completely, with no placeholders or TODOs.
4. **Run & verify** by installing, building, testing and fixing errors when a shell is available.
5. **Deliver** local run steps, a `.env.example`, deploy instructions and next ideas.

Built-in quality rules cover responsive and accessible design, input validation, secret handling, auth checks, error and loading states, tests and a project README.

---

## 📥 Installation

### Option A: Claude app (Pro, Max, Team, Enterprise)
1. Download **`fullstack-developer.zip`** from the [Releases](https://github.com/jrnoorbaloch/fullstack-dev-skill/releases) page, or download this repo and zip the `skills/fullstack-developer` folder.
2. In Claude, go to **Settings → Capabilities → Skills** (make sure code execution is enabled).
3. Click **Upload skill**, select the zip file, and turn the skill on.
4. Start prompting, for example: *"Build a website for my restaurant."*

### Option B: Claude Code
```bash
/plugin marketplace add jrnoorbaloch/fullstack-dev-skill
/plugin install fullstack-developer@fullstack-dev-skill
```
Or install manually:
```bash
git clone https://github.com/jrnoorbaloch/fullstack-dev-skill.git
mkdir -p ~/.claude/skills
cp -r fullstack-dev-skill/skills/fullstack-developer ~/.claude/skills/
```

---

## 💬 Prompts
Ready-to-use prompts for every project type are in **[PROMPTS.md](PROMPTS.md)**.

Examples:
- `Build a modern website for my business "Ali Bakery" in English and Urdu, with a WhatsApp button.`
- `Build an e-commerce store with cart, checkout, admin panel and Cash on Delivery.`
- `Build an expense tracker app in React Native and show me how to build the APK.`
- `Build Windows POS software with receipt printing and an offline database.`

## 📁 Repository Structure
```
.claude-plugin/              Plugin and marketplace manifests (Claude Code)
skills/fullstack-developer/
  SKILL.md                   Main skill instructions
  references/
    web.md                   Websites and web apps
    backend-db.md            APIs, databases, auth
    mobile.md                Mobile apps
    desktop.md               Desktop software, CLIs, scripts
    deploy.md                Deployment and DevOps
    prompts.md               Prompt library
PROMPTS.md                   Prompt library (copy for easy access)
```

## 🤝 Contributing
Pull requests are welcome. Add new prompts or stack guides under `skills/fullstack-developer/references/`.

## 📄 License
[MIT](LICENSE)
