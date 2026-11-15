# 🚀 Full-Stack Developer Skill for Claude

Ek prompt dein — Claude aap ke liye **website, web app, SaaS, API, mobile app (Android/iOS) ya desktop software** bana dega. Kisi bhi zubaan mein likhein (Urdu, Roman Urdu, English, Hindi, Arabic…), Claude usi mein jawab dega.

Give one prompt — Claude builds a complete website, web app, API, mobile app or desktop software. Works in any language.

## ✨ Kya kar sakta hai
| | |
|---|---|
| 🌐 Websites | Landing page, portfolio, business site, blog |
| 🧩 Web apps | SaaS, e-commerce, dashboards, booking, LMS, chat, AI apps |
| ⚙️ Backend | REST APIs, databases, auth, payments |
| 📱 Mobile | React Native/Expo, Flutter → APK / Play Store / App Store |
| 🖥️ Desktop | POS, inventory, tools → .exe / .dmg (Tauri, Electron, Python) |
| 🚀 Deploy | Vercel, Netlify, Supabase, Docker, GitHub Actions |

Har programming language support: JavaScript/TypeScript, Python, PHP/Laravel, Java, C#, Go, Rust, Dart, Kotlin, Swift…

---

## 📥 Install karne ka tareeqa

### Option A — Claude.ai / Claude app (Pro, Max, Team, Enterprise)
1. Is repo se **`fullstack-developer.zip`** download karein (Releases section), ya repo download kar ke `skills/fullstack-developer` folder ko zip karein.
2. Claude mein jayein: **Settings → Capabilities → Skills** (Code execution ON hona chahiye).
3. **Upload skill** → zip file select karein → skill ON kar dein.
4. Ab bas prompt dein, e.g. *"Mere restaurant ke liye website banao"*.

### Option B — Claude Code (terminal)
```bash
/plugin marketplace add YOUR-USERNAME/fullstack-dev-skill
/plugin install fullstack-developer@fullstack-dev-skill
```
Ya manually:
```bash
git clone https://github.com/YOUR-USERNAME/fullstack-dev-skill.git
mkdir -p ~/.claude/skills
cp -r fullstack-dev-skill/skills/fullstack-developer ~/.claude/skills/
```

---

## 💬 Prompts
Har cheez ke ready prompts: **[PROMPTS.md](PROMPTS.md)**

Misaal:
- `Mere business "Ali Bakery" ke liye modern website banao, Urdu + English, WhatsApp button ke saath.`
- `Ek e-commerce store banao: cart, checkout, admin panel, Cash on Delivery.`
- `React Native mein expense tracker app banao aur APK build ka tareeqa batao.`
- `Shop ke liye Windows POS software banao, receipt print aur offline database ke saath.`

## 📁 Structure
```
.claude-plugin/          plugin + marketplace manifests (Claude Code)
skills/fullstack-developer/
  SKILL.md               main instructions
  references/            web, backend-db, mobile, desktop, deploy, prompts
PROMPTS.md               prompt library
```

## 🤝 Contribute
Pull requests welcome — naye prompts ya stacks `references/` mein add karein.

## 📄 License
MIT
