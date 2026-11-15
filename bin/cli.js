#!/usr/bin/env node
// Full-Stack Developer skill installer for Claude. No dependencies.
"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const zlib = require("node:zlib");

const PKG_ROOT = path.resolve(__dirname, "..");
const PKG = JSON.parse(fs.readFileSync(path.join(PKG_ROOT, "package.json"), "utf8"));
const CONFIG = JSON.parse(fs.readFileSync(path.join(PKG_ROOT, "packs.json"), "utf8"));
const FULL = "fullstack-developer";
const SKIP = new Set(["node_modules", "__pycache__", ".pytest_cache", "dist", "build", "out", ".next", ".expo"]);

const c = process.stdout.isTTY && !process.env.NO_COLOR
  ? { b: (s) => `\x1b[1m${s}\x1b[0m`, g: (s) => `\x1b[32m${s}\x1b[0m`, d: (s) => `\x1b[2m${s}\x1b[0m`, r: (s) => `\x1b[31m${s}\x1b[0m` }
  : { b: (s) => s, g: (s) => s, d: (s) => s, r: (s) => s };

function fail(msg) {
  console.error(c.r("Error: ") + msg);
  process.exit(1);
}

function skillDir(name) {
  if (!CONFIG.packs[name]) fail(`Unknown pack "${name}". Run "fullstack-dev-skill list" to see available packs.`);
  const dir = name === FULL ? path.join(PKG_ROOT, CONFIG.source) : path.join(PKG_ROOT, "packs", name, "skills", name);
  if (!fs.existsSync(path.join(dir, "SKILL.md"))) fail(`Pack files not found at ${dir}`);
  return dir;
}

function targetBase(opts) {
  if (opts.dir) return path.resolve(opts.dir);
  if (opts.project) return path.join(process.cwd(), ".claude", "skills");
  return path.join(os.homedir(), ".claude", "skills");
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    if (SKIP.has(entry.name)) continue;
    const s = path.join(src, entry.name), d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else if (entry.isFile()) fs.copyFileSync(s, d);
  }
}

function walk(dir, base = dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    if (SKIP.has(entry.name)) continue;
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p, base, out);
    else if (entry.isFile()) out.push(p);
  }
  return out;
}

// ---- minimal ZIP writer (deflate) ----
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let k = n;
    for (let i = 0; i < 8; i++) k = k & 1 ? 0xedb88320 ^ (k >>> 1) : k >>> 1;
    t[n] = k >>> 0;
  }
  return t;
})();
function crc32(buf) {
  let crc = 0xffffffff;
  for (let i = 0; i < buf.length; i++) crc = CRC_TABLE[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}
function dosDateTime(d) {
  const time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
  const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
  return { time, date };
}
function writeZip(files, outFile) {
  const chunks = [], central = [];
  let offset = 0;
  const { time, date } = dosDateTime(new Date());
  for (const { name, data } of files) {
    const nameBuf = Buffer.from(name, "utf8");
    const comp = zlib.deflateRawSync(data, { level: 9 });
    const crc = crc32(data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0); local.writeUInt16LE(20, 4); local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(8, 8); local.writeUInt16LE(time, 10); local.writeUInt16LE(date, 12);
    local.writeUInt32LE(crc, 14); local.writeUInt32LE(comp.length, 18); local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26); local.writeUInt16LE(0, 28);
    chunks.push(local, nameBuf, comp);
    const cen = Buffer.alloc(46);
    cen.writeUInt32LE(0x02014b50, 0); cen.writeUInt16LE(20, 4); cen.writeUInt16LE(20, 6); cen.writeUInt16LE(0x0800, 8);
    cen.writeUInt16LE(8, 10); cen.writeUInt16LE(time, 12); cen.writeUInt16LE(date, 14);
    cen.writeUInt32LE(crc, 16); cen.writeUInt32LE(comp.length, 20); cen.writeUInt32LE(data.length, 24);
    cen.writeUInt16LE(nameBuf.length, 28); cen.writeUInt32LE(offset, 42);
    central.push(cen, nameBuf);
    offset += local.length + nameBuf.length + comp.length;
  }
  const cenSize = central.reduce((n, b) => n + b.length, 0);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(files.length, 8); end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(cenSize, 12); end.writeUInt32LE(offset, 16);
  fs.mkdirSync(path.dirname(outFile), { recursive: true });
  fs.writeFileSync(outFile, Buffer.concat([...chunks, ...central, end]));
}

// ---- commands ----
function list() {
  console.log(c.b("Available packs") + c.d(`  (v${PKG.version})`) + "\n");
  for (const [name, p] of Object.entries(CONFIG.packs)) {
    const tag = name === FULL ? c.g(" (default, everything)") : "";
    console.log(`  ${c.b(name.padEnd(22))} ${p.title}${tag}`);
  }
  console.log(`\nInstall one with: ${c.b("fullstack-dev-skill install <pack>")}`);
}

function install(name, opts) {
  const src = skillDir(name);
  const dest = path.join(targetBase(opts), name);
  if (fs.existsSync(dest)) {
    if (!opts.force) fail(`${dest} already exists. Use --force to replace it.`);
    fs.rmSync(dest, { recursive: true, force: true });
  }
  copyDir(src, dest);
  console.log(`${c.g("✓")} Installed ${c.b(name)} → ${dest}`);
  console.log(c.d("  Restart Claude Code (or start a new session) to load it. Then just describe what to build."));
}

function uninstall(name, opts) {
  if (!CONFIG.packs[name]) fail(`Unknown pack "${name}".`);
  const dest = path.join(targetBase(opts), name);
  if (!fs.existsSync(path.join(dest, "SKILL.md"))) fail(`${name} is not installed at ${dest}`);
  fs.rmSync(dest, { recursive: true, force: true });
  console.log(`${c.g("✓")} Removed ${dest}`);
}

function makeZip(name, opts) {
  const src = skillDir(name);
  const out = path.resolve(opts.output || `${name}.zip`);
  const files = walk(src).map((f) => ({ name: path.posix.join(name, path.relative(src, f).split(path.sep).join("/")), data: fs.readFileSync(f) }));
  writeZip(files, out);
  console.log(`${c.g("✓")} Wrote ${out} (${files.length} files)`);
  console.log(c.d("  Claude app → Settings → Capabilities → Skills → Upload skill"));
}

function help() {
  console.log(`${c.b("fullstack-dev-skill")} v${PKG.version} — Full-Stack Developer skill for Claude

${c.b("Usage")}
  fullstack-dev-skill list                       Show available packs
  fullstack-dev-skill install [pack] [options]   Install into Claude Code (default pack: ${FULL})
  fullstack-dev-skill uninstall [pack] [options] Remove an installed pack
  fullstack-dev-skill zip [pack] [-o file.zip]   Build a zip for the Claude app (Settings → Skills → Upload)

${c.b("Options")}
  --project      Use ./.claude/skills (this project) instead of ~/.claude/skills
  --dir <path>   Use a custom skills directory
  --force        Replace an existing installation
  -o, --output   Zip output path
  -v, --version  Print version

${c.b("Examples")}
  npx fullstack-dev-skill install
  npx fullstack-dev-skill install fullstack-web --project
  npx fullstack-dev-skill zip fullstack-motion-3d -o motion.zip`);
}

function parse(argv) {
  const opts = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--project") opts.project = true;
    else if (a === "--force" || a === "-f") opts.force = true;
    else if (a === "--dir") opts.dir = argv[++i];
    else if (a === "-o" || a === "--output") opts.output = argv[++i];
    else if (a === "-v" || a === "--version") opts.version = true;
    else if (a === "-h" || a === "--help") opts.help = true;
    else if (a.startsWith("-")) fail(`Unknown option ${a}`);
    else opts._.push(a);
  }
  if ((opts.dir === undefined && argv.includes("--dir")) || (opts.output === undefined && (argv.includes("-o") || argv.includes("--output")))) fail("Missing value for option");
  return opts;
}

function main() {
  const opts = parse(process.argv.slice(2));
  if (opts.version) return console.log(PKG.version);
  const [cmd = "help", name = FULL] = opts._;
  if (opts.help || cmd === "help") return help();
  if (cmd === "list") return list();
  if (cmd === "install") return install(name, opts);
  if (cmd === "uninstall" || cmd === "remove") return uninstall(name, opts);
  if (cmd === "zip") return makeZip(name, opts);
  fail(`Unknown command "${cmd}". Run "fullstack-dev-skill help".`);
}

main();
