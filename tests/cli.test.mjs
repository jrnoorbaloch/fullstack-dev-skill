import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const CLI = path.resolve("bin/cli.js");
const run = (...args) => execFileSync("node", [CLI, ...args], { encoding: "utf8", env: { ...process.env, NO_COLOR: "1" } });
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), "fds-"));
const packs = Object.keys(JSON.parse(fs.readFileSync("packs.json", "utf8")).packs);

test("version matches package.json", () => {
  assert.equal(run("--version").trim(), JSON.parse(fs.readFileSync("package.json", "utf8")).version);
});

test("list shows every pack", () => {
  const out = run("list");
  for (const p of packs) assert.match(out, new RegExp(p));
});

test("install, refuse overwrite, force, uninstall", () => {
  const dir = tmp();
  for (const p of packs) {
    run("install", p, "--dir", dir);
    const md = fs.readFileSync(path.join(dir, p, "SKILL.md"), "utf8");
    assert.match(md, new RegExp(`^---\\nname: ${p}\\n`));
    assert.ok(!fs.existsSync(path.join(dir, p, "templates", "nextjs-saas", "node_modules")));
  }
  assert.throws(() => run("install", "fullstack-web", "--dir", dir));
  run("install", "fullstack-web", "--dir", dir, "--force");
  run("uninstall", "fullstack-web", "--dir", dir);
  assert.ok(!fs.existsSync(path.join(dir, "fullstack-web")));
});

test("unknown pack fails", () => {
  assert.throws(() => run("install", "nope", "--dir", tmp()));
});

test("zip is valid and rooted at the skill folder", () => {
  const out = path.join(tmp(), "w.zip");
  run("zip", "fullstack-wordpress", "-o", out);
  const listing = execFileSync("python3", ["-c", `import zipfile,sys;z=zipfile.ZipFile(sys.argv[1]);assert z.testzip() is None;print("\\n".join(z.namelist()))`, out], { encoding: "utf8" });
  assert.match(listing, /^fullstack-wordpress\/SKILL\.md$/m);
  assert.match(listing, /^fullstack-wordpress\/templates\/wordpress-block-theme\/theme\/theme\.json$/m);
});
