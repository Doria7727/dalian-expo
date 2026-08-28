// Cloudflare Pages Function：表单提交代理
// 作用：让浏览器只与同源站点（dalian-expo.pages.dev）通信（国内稳定可达），
// 由边缘服务端再转发给 FormSubmit.co，规避"手机直连国外服务被墙/超时"导致提交失败。
// 客户端 POST JSON（含 _subject/_template/_captcha 及表单字段）到 /api/apply 即可。

export async function onRequestPost({ request }) {
  let data;
  try {
    data = await request.json();
  } catch (e) {
    return Response.json({ success: false, message: "invalid body" }, { status: 400 });
  }

  const EMAIL = "1060200619@qq.com";
  try {
    const r = await fetch("https://formsubmit.co/ajax/" + EMAIL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://dalian-expo.pages.dev"
      },
      body: JSON.stringify(data)
    });
    const j = await r.json().catch(() => ({}));
    const ok = r.ok && (j.success === true || j.success === "true");
    if (ok) {
      return Response.json({ success: true, message: j.message || "ok" });
    }
    return Response.json(
      { success: false, message: j.message || "formsubmit rejected" },
      { status: 502 }
    );
  } catch (e) {
    return Response.json({ success: false, message: "forward failed" }, { status: 502 });
  }
}
