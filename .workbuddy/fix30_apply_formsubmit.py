"""
fix30: 把 applyForm（apply.html）的 submit handler 改为走 FormSubmit.co AJAX，
发到 1060200619@qq.com。
文件行尾自适应（CRLF/LF）。
"""
import sys

PATH = r"C:\Users\ASUS\Desktop\2027大连工博会网站\assets\js\main.js"

with open(PATH, "rb") as f:
    raw = f.read()

# 探测行尾
if raw.count(b"\r\n") > raw.count(b"\n"):
    NL = b"\r\n"
else:
    NL = b"\n"
print("行尾:", "CRLF" if NL == b"\r\n" else "LF", "rawCRLF=%d rawLF=%d" % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))

def to_bytes(s: str) -> bytes:
    return s.replace("\r\n", "\n").replace("\n", NL.decode("utf-8")).encode("utf-8")

# 1) 改 form.addEventListener("submit", (e) => {  -> async (e) => {
old1 = to_bytes('    form.addEventListener("submit", (e) => {\n      e.preventDefault();')
new1 = to_bytes('    form.addEventListener("submit", async (e) => {\n      e.preventDefault();')

if old1 not in raw:
    print("找不到 old1（submit handler 起始行）", file=sys.stderr)
    sys.exit(2)
raw = raw.replace(old1, new1, 1)
print("step1 OK：handler 改为 async")

# 2) 替换 if (!ok) return; 之后到函数末尾的整段逻辑
old2_str = '\n'.join([
'      if (!ok) return;',
'      try { localStorage.setItem("diie_apply_" + Date.now(), JSON.stringify(data)); } catch (_) {}',
'      const okBox = $("#applyOk");',
'      okBox.textContent = `✅ 报名提交成功！${esc(data.company)}，${esc(data.contact)}，组委会将尽快与您联系对接展位事宜。`;',
'      okBox.classList.remove("hidden");',
'      form.reset();',
'      syncBooth();',
'      okBox.scrollIntoView({ behavior: "smooth", block: "center" });',
'    });',
])
old2 = to_bytes(old2_str)

new2_lines = [
'      if (!ok) return;',
'',
'      // 本地缓存一份（防止网络异常丢数据，本机也可回看）',
'      try { localStorage.setItem("diie_apply_" + Date.now(), JSON.stringify(data)); } catch (_) {}',
'',
'      const submitBtn = form.querySelector(\'button[type="submit"]\');',
'      const okBox = $("#applyOk");',
'      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "\u6b63\u5728\u63d0\u4ea4..."; }',
'',
'      // ---- \u4e3b\u901a\u9053\uff1aFormSubmit.co AJAX\uff0c\u53d1\u5230 1060200619@qq.com ----',
'      // \u9996\u6b21\u63d0\u4ea4\u9700\u4e3b\u8f6e\u673a\u4eba\u5728\u6536\u4ef6\u7bb1\u70b9 "Activate Form" \u90ae\u4ef6\u5b8c\u6210\u6fc0\u6d3b\u3002',
'      let delivered = false;',
'      try {',
'        const payload = {',
'          _subject: "\u3010\u5927\u8fde\u5de5\u535a\u4f1a\u00b7\u53c2\u5c55\u62a5\u540d\u3011" + (data.company || "") + " \u00b7 " + (data.contact || ""),',
'          _template: "table",',
'          _captcha: "false",',
'          "\u4f01\u4e1a\u540d\u79f0": data.company || "",',
'          "\u8054\u7cfb\u4eba": data.contact || "",',
'          "\u624b\u673a\u53f7": data.phone || "",',
'          "\u804c\u52a1": data.title || "",',
'          "\u90ae\u7bb1": data.email || "",',
'          "\u610f\u5411\u53c2\u5c55\u5c55\u533a": data.zone || "",',
'          "\u5c55\u4f4d\u7c7b\u578b": data.boothType || "",',
'          "\u6807\u51c6\u5c55\u4f4d\u6570\u91cf\uff08\u4e2a\uff09": data.boothStd || "",',
'          "\u5149\u5730\u9762\u79ef\uff08\u33a1\uff09": data.boothRaw || "",',
'          "\u4e3b\u8425\u4ea7\u54c1/\u5c55\u54c1\u7c7b\u522b": data.products || "",',
'          "\u5907\u6ce8/\u7279\u6b8a\u9700\u6c42": data.remark || "",',
'          "\u63d0\u4ea4\u65f6\u95f4": new Date().toLocaleString("zh-CN")',
'        };',
'        const r = await fetch("https://formsubmit.co/ajax/1060200619@qq.com", {',
'          method: "POST",',
'          headers: { "Content-Type": "application/json", Accept: "application/json" },',
'          body: JSON.stringify(payload)',
'        });',
'        delivered = r.ok;',
'      } catch (_) { delivered = false; }',
'',
'      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = "\u63d0\u4ea4\u53c2\u5c55\u62a5\u540d"; }',
'',
'      if (delivered) {',
'        okBox.innerHTML = `\u2705 \u5df2\u6536\u5230\uff01\u62a5\u540d\u8868\u5df2\u53d1\u9001\u5230\u7ec4\u59d4\u4f1a\u90ae\u7bb1 <b>1060200619@qq.com</b>\uff0c<b>${esc(data.company)}</b>\uff08${esc(data.contact)}\uff09\u5c06\u5728 <b>1 \u4e2a\u5de5\u4f5c\u65e5\u5185</b>\u4e0e\u60a8\u8054\u7cfb\u5bf9\u63a5\u5c55\u4f4d\u4e8b\u5b9c\u3002`;',
'      } else {',
'        // \u5151\u5e95\uff1a\u8c03\u8d77\u90ae\u4ef6\u5ba2\u6237\u7aef\uff08\u5173\u952e\u4fe1\u606f\u7cbe\u7b80\uff09\uff0c\u540c\u65f6\u63d0\u793a\u76f4\u6253\u7535\u8bdd',
'        const subject = encodeURIComponent("\u3010\u5927\u8fde\u5de5\u535a\u4f1a\u00b7\u53c2\u5c55\u62a5\u540d\u3011" + (data.company || "") + " \u00b7 " + (data.contact || ""));',
'        const body = encodeURIComponent(',
'          "\u4f01\u4e1a\u540d\u79f0\uff1a" + (data.company || "") + "\\n" +',
'          "\u8054\u7cfb\u4eba\uff1a" + (data.contact || "") + "\\n" +',
'          "\u624b\u673a\u53f7\uff1a" + (data.phone || "") + "\\n" +',
'          "\u610f\u5411\u5c55\u533a\uff1a" + (data.zone || "") + "\\n" +',
'          "\u5c55\u4f4d\u7c7b\u578b\uff1a" + (data.boothType || "") + "\\n" +',
'          (data.boothType === "\u6807\u51c6\u5c55\u4f4d" ? "\u6807\u51c6\u5c55\u4f4d\u6570\u91cf\uff1a" + (data.boothStd || "") + "\\n" : "") +',
'          (data.boothType === "\u5ba4\u5185\u5149\u5730" ? "\u5149\u5730\u9762\u79ef\uff1a" + (data.boothRaw || "") + "\u33a1\\n" : "") +',
'          "\u4e3b\u8425\u4ea7\u54c1\uff1a" + (data.products || "") + "\\n" +',
'          "\u5907\u6ce8\uff1a" + (data.remark || "") + "\\n"',
'        );',
'        okBox.innerHTML = `\u26a0\ufe0f \u63d0\u4ea4\u672a\u53d1\u9001\u51fa\u53bb\u3002\u8bf7\u62e8\u6253\u7ec4\u59d4\u4f1a\u7535\u8bdd <a href="tel:18624268832"><b>18624268832</b></a>\uff08\u674e\u73a5\uff09\uff0c\u6216\u70b9\u6b64\u5904\u76f4\u63a5\u53d1\u90ae\u4ef6\uff1a<a href="mailto:1060200619@qq.com?subject=${subject}&body=${body}">1060200619@qq.com</a>\u3002`;',
'      }',
'      okBox.classList.remove("hidden");',
'      form.reset();',
'      syncBooth();',
'      okBox.scrollIntoView({ behavior: "smooth", block: "center" });',
'    });',
]
new2 = to_bytes('\n'.join(new2_lines))

if old2 not in raw:
    print("找不到 old2（核心提交逻辑）", file=sys.stderr)
    # debug: show what is around
    i = raw.find(b'if (!ok) return;')
    print("--- 区段上下文 ---")
    sys.stdout.buffer.write(raw[max(0,i-50):i+400])
    sys.exit(2)
raw = raw.replace(old2, new2, 1)
print("step2 OK：替换提交逻辑")

# 3) 改 form-note 文案（说在前端校验后"本地保存"了）
old3 = to_bytes('<p class="form-note">提交即表示同意主办方与您联系对接参展事宜。本示例表单在前端校验后本地保存。</p>')
new3 = to_bytes('<p class="form-note">提交后，报名信息将发送到组委会邮箱 1060200619@qq.com，主办方 1 个工作日内与您联系。提交即表示同意主办方与您联系对接参展事宜。</p>')
if old3 not in raw:
    print("找不到 old3（form-note）", file=sys.stderr)
    sys.exit(2)
raw = raw.replace(old3, new3, 1)
print("step3 OK：form-note 文案改为真实说明")

with open(PATH, "wb") as f:
    f.write(raw)
print("写入完成")
