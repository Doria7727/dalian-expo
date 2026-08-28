"""fix14d.py - Add proper CSS for .brand-img so the original logo image
              scales to fit the nav bar / footer area.
              Handles CRLF line endings in CSS.
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

css = subprocess.run(["git", "show", f"{BASE}:assets/css/style.css"], capture_output=True).stdout.decode("utf-8")
print("css has CRLF:", "\r\n" in css)

# 1) Insert .brand-img rule right after `.brand:hover { color: #fff; }`
anchor = ".brand:hover { color: #fff; }"
brand_img_rule = ".brand-img {\r\n  height: 52px; width: auto;\r\n  flex: none; display: block;\r\n}"
assert anchor in css, f"anchor not found, looking for: {repr(anchor)}"
css_new = css.replace(anchor, anchor + "\r\n" + brand_img_rule, 1)
print("+brand-img rule")

# 2) Add footer brand-img sizing
footer_anchor = ".footer-brand .brand { margin-bottom: 16px; }"
assert footer_anchor in css_new
css_new = css_new.replace(
    footer_anchor,
    footer_anchor + "\r\n.footer-brand .brand-img { height: 68px; }",
    1,
)
print("+footer rule")

# 3) Mobile rules: replace the 3 obsolete lines + add 2 new ones
old_mobile = "  .brand-d { width: 32px; height: 32px; font-size: 1.15rem; }\r\n  .brand-ief { font-size: .9rem; }\r\n  .brand-leaf { width: 16px; height: 16px; }\r\n  .brand-mark { height: 38px; padding: 3px 8px 3px 3px; }"
new_mobile = "  .brand-img { height: 44px; }\r\n  .footer-brand .brand-img { height: 56px; }"
assert old_mobile in css_new, "mobile block not found"
css_new = css_new.replace(old_mobile, new_mobile, 1)
print("+mobile rules")

# git plumbing
subprocess.run(["git", "read-tree", BASE], check=True, cwd=REPO)
sha = write_blob_str(css_new)
subprocess.run(
    ["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},assets/css/style.css"],
    check=True,
)
print("  + assets/css/style.css", sha[:8])

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "修复 logo 尺寸：.brand-img 加 CSS（头部 52px / 页脚 68px / 移动 44px）"],
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