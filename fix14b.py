"""fix14b.py - Add proper CSS for .brand-img so the original logo image
              scales to fit the nav bar / footer area.

Current state: image is rendering at full 1324x473, blowing out the navbar.
Fix: add .brand-img rules with proper sizing, plus remove obsolete brand-mark
/ brand-d / brand-ief / brand-leaf rules (now that the image replaces them).
"""
import os
import subprocess

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
os.chdir(REPO)

BASE = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("BASE =", BASE)

def write_blob_str(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    return r.stdout.decode().strip()

# Read current style.css from git (NOT disk - the disk may be stale)
css = subprocess.run(["git", "show", f"{BASE}:assets/css/style.css"], capture_output=True).stdout.decode("utf-8")

# ------------------------------------------------------------------
# Replace the obsolete brand-mark SVG-related CSS with brand-img CSS
# ------------------------------------------------------------------
old_block = """.brand { display: flex; align-items: center; gap: 12px; color: #fff; flex: none; text-decoration: none; }
.brand:hover { color: #fff; }
.brand-mark {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--c-navy);
  border-radius: 8px;
  padding: 4px 12px 4px 4px;
  height: 44px;
  box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.brand-d {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 6px;
  background: linear-gradient(135deg, #d83a1a 0%, #e8541e 100%);
  color: #fff; font-weight: 800; font-size: 1.25rem; font-family: var(--font-en);
  letter-spacing: -.02em;
}
.brand-ief { font-size: 1rem; font-weight: 700; color: #fff; font-family: var(--font-en); letter-spacing: .04em; }
.brand-leaf { width: 18px; height: 18px; flex: none; margin-left: 2px; }
.brand-txt { line-height: 1.2; }
.brand-txt b {
  display: block; color: #fff; font-size: 1.05rem; font-weight: 700;
  letter-spacing: .02em;
}
.brand-txt span {
  display: block; color: rgba(255,255,255,.7); font-size: .72rem;
  letter-spacing: .04em; font-family: var(--font-en);
}"""

new_block = """.brand { display: flex; align-items: center; gap: 12px; color: #fff; flex: none; text-decoration: none; }
.brand:hover { color: #fff; }
.brand-img {
  height: 52px; width: auto;
  flex: none; display: block;
}
.brand-txt { line-height: 1.2; }
.brand-txt b {
  display: block; color: #fff; font-size: 1.05rem; font-weight: 700;
  letter-spacing: .02em;
}
.brand-txt span {
  display: block; color: rgba(255,255,255,.7); font-size: .72rem;
  letter-spacing: .04em; font-family: var(--font-en);
}"""

assert old_block in css, "old CSS block not found"
css_new = css.replace(old_block, new_block, 1)
assert css_new != css, "no replacement made"

# Footer brand-img sizing
old_footer = ".footer-brand .brand { margin-bottom: 16px; }"
new_footer = """.footer-brand .brand { margin-bottom: 16px; }
.footer-brand .brand-img { height: 68px; }"""
assert old_footer in css_new, "footer brand rule not found"
css_new = css_new.replace(old_footer, new_footer, 1)

# Mobile rules (replace brand-mark related ones)
old_mobile = """  .brand-txt span { display: none; }
  .brand-txt b { font-size: .92rem; }
  .brand-d { width: 32px; height: 32px; font-size: 1.15rem; }
  .brand-ief { font-size: .9rem; }
  .brand-leaf { width: 16px; height: 16px; }
  .brand-mark { height: 38px; padding: 3px 8px 3px 3px; }"""

new_mobile = """  .brand-txt span { display: none; }
  .brand-txt b { font-size: .92rem; }
  .brand-img { height: 44px; }
  .footer-brand .brand-img { height: 56px; }"""
assert old_mobile in css_new, "mobile brand rules not found"
css_new = css_new.replace(old_mobile, new_mobile, 1)

# git plumbing
subprocess.run(["git", "read-tree", BASE], check=True, cwd=REPO)
sha = write_blob_str(css_new)
subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},assets/css/style.css"], check=True)
print("  + assets/css/style.css", sha[:8])

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "修复 logo 尺寸：.brand-img 加 CSS（头部 52px / 页脚 68px / 移动 44px），清理已废弃的 brand-mark/d/ief/leaf 样式"],
    capture_output=True, text=True,
).stdout.strip()
print("commit =", commit)
subprocess.run(["git", "update-ref", "refs/heads/main", commit], check=True)

push = subprocess.run(
    ["git", "push", "github", "main", "--force"],
    capture_output=True, text=True,
    env={**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"},
)
print("push rc:", push.returncode)
print("STDOUT:", push.stdout[-500:])
if push.stderr:
    print("STDERR:", push.stderr[-500:])