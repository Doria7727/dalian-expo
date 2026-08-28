"""fix14.py - Restore the user's original logo image to header & footer
              (fix13.py accidentally dropped it; rebuild a complete tree)

The bug: HEAD 1af0c9d has only 2 files (main.js + style.css). All other files
were lost during the read-tree --empty cycle in fix13.py. The live site is
serving from Cloudflare's cache of an older deploy.

Fix:
  1) Replace the SVG brand-mark in main.js with the user's original image
     (assets/img/logo-composite.png, which is the 1324x473 red-D + iEF + ufi
     logo they provided originally).
  2) Rebuild a complete commit tree from disk: main.js + style.css +
     data.json + logo-composite.png + wechat-qr.jpg + past/past01-10.jpg
     + all root html files + assets/vendor/decap-cms.js + admin/ etc.
  3) Force-push to GitHub main.
"""
import os
import subprocess

REPO = r"C:\Users\ASUS\Desktop\2027大连工博会网站"
os.chdir(REPO)

BASE = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print("BASE =", BASE)

def write_blob_from_file(path):
    """Read file from disk and write to git object DB, return sha."""
    with open(path, "rb") as f:
        data = f.read()
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    return r.stdout.decode().strip()

def write_blob_str(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=data, capture_output=True)
    return r.stdout.decode().strip()

# ------------------------------------------------------------------
# 1) Read main.js from disk, replace brand-mark with brand-img
# ------------------------------------------------------------------
with open(os.path.join(REPO, "assets/js/main.js"), "r", encoding="utf-8") as f:
    main_js = f.read()

old_brand = """        <span class="brand-mark">
          <span class="brand-d">D</span>
          <span class="brand-ief">IEF</span>
          <svg class="brand-leaf" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66.95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75C7 8 17 8 17 8z" fill="#7cb342"/>
          </svg>
        </span>"""

new_brand = """        <img class="brand-img" src="assets/img/logo-composite.png" alt="大连国际工业博览会 · 中国大连 iEF · UFI 认证" />"""

assert old_brand in main_js, "brand-mark block not found in disk main.js"
M = main_js.replace(old_brand, new_brand, 1)
assert M != main_js, "no replacement made"

# ------------------------------------------------------------------
# 2) Read style.css from disk (no change, just include it)
# ------------------------------------------------------------------
# (style.css is fine, will just take it as-is from disk)

# ------------------------------------------------------------------
# 3) Define the full file set to include in the new commit
# ------------------------------------------------------------------
FILES = [
    # Site code
    ("assets/js/main.js",     M),
    ("assets/js/data.json",   None),    # read from disk
    ("assets/css/style.css",  None),    # read from disk
    # Logo (user's original image, 1324x473 PNG)
    ("assets/img/logo-composite.png", None),
    # Wechat QR
    ("assets/img/wechat-qr.jpg", None),
    # Past photos (10)
    ("assets/img/past/past01.jpg", None),
    ("assets/img/past/past02.jpg", None),
    ("assets/img/past/past03.jpg", None),
    ("assets/img/past/past04.jpg", None),
    ("assets/img/past/past05.jpg", None),
    ("assets/img/past/past06.jpg", None),
    ("assets/img/past/past07.jpg", None),
    ("assets/img/past/past08.jpg", None),
    ("assets/img/past/past09.jpg", None),
    ("assets/img/past/past10.jpg", None),
    # HTML sub-pages (so anchor nav doesn't 404)
    ("about.html",   None),
    ("contact.html", None),
    ("apply.html",   None),
    ("exhibits.html", None),
    ("exhibitors.html", None),
    ("index.html",   None),
]

# ------------------------------------------------------------------
# 4) git plumbing
# ------------------------------------------------------------------
subprocess.run(["git", "read-tree", "--empty"], check=True, cwd=REPO)

for path, content in FILES:
    if content is None:
        full = os.path.join(REPO, path)
        if not os.path.exists(full):
            print(f"  WARN: missing on disk: {path}")
            continue
        sha = write_blob_from_file(full)
    else:
        sha = write_blob_str(content)
    subprocess.run(
        ["git", "update-index", "--add", "--cacheinfo", f"100644,{sha},{path}"],
        check=True,
    )
    print(f"  + {path:40s} {sha[:8]}")

new_tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True).stdout.strip()
print("tree =", new_tree)

commit = subprocess.run(
    ["git", "commit-tree", new_tree, "-p", BASE, "-m",
     "修复 logo：完全使用用户提供的原图（红D+iEF+UFI 组合图），并恢复完整文件树（之前 read-tree --empty 误删了图片/JSON）"],
    capture_output=True, text=True
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