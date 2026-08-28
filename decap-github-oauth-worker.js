// ===========================================================================
// Decap CMS — GitHub OAuth 代理（部署在 Cloudflare Worker）
// ---------------------------------------------------------------------------
// 作用：Decap CMS 的 "github" 后端默认借用 Netlify 的 OAuth 代理
//       (api.netlify.com/auth)，但本站部署在 Cloudflare Pages，Netlify 找不到
//       本项目，会返回 Not Found。此 Worker 在 Cloudflare 上自建 OAuth 握手，
//       让 Decap 能走 GitHub 登录。
//
// 此文件只负责 OAuth 握手（/auth 跳转 + /callback 换 token），
// 不代理 GitHub API（Decap 拿到 user token 后直接调 api.github.com）。
//
// 部署后在 Cloudflare Worker 设置两个【加密变量 secrets】：
//   CLIENT_ID     = Ov23liHFOwbuQpQyNCD6
//   CLIENT_SECRET = GitHub OAuth App 里生成的 client secret
// ===========================================================================

// 你的网站后台地址（Decap 登录成功后跳回这里）
const CMS_URL = 'https://dalian-expo.pages.dev';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { CLIENT_ID, CLIENT_SECRET } = env;
    const path = url.pathname.replace(/\/+$/, ''); // 去掉尾部斜杠，兼容 /auth/ 写法

    // ---- 1. OAuth 授权跳转：重定向到 GitHub 登录页 ----
    if (path === '/auth') {
      const provider = url.searchParams.get('provider') || 'github';
      if (provider !== 'github') {
        return new Response('Unsupported provider: ' + provider, { status: 400 });
      }
      const ghAuth = new URL('https://github.com/login/oauth/authorize');
      ghAuth.searchParams.set('client_id', CLIENT_ID);
      ghAuth.searchParams.set('scope', 'repo');
      ghAuth.searchParams.set('response_type', 'code');
      ghAuth.searchParams.set('redirect_uri', `${url.origin}/callback`); // 必须是本 Worker 的 /callback
      return Response.redirect(ghAuth.toString(), 302);
    }

    // ---- 2. OAuth 回调：用 code 换 access_token，再跳回后台 ----
    if (path === '/callback') {
      const code = url.searchParams.get('code');
      if (!code) {
        return new Response('Missing code parameter', { status: 400 });
      }
      const tokenResp = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: CLIENT_ID,
          client_secret: CLIENT_SECRET,
          code,
          redirect_uri: `${url.origin}/callback`
        })
      });
      const tokenData = await tokenResp.json();
      if (tokenData.error) {
        return new Response(
          'GitHub OAuth error: ' + (tokenData.error_description || tokenData.error),
          { status: 400 }
        );
      }
      // 把 token 放进 URL hash（#access_token=...），Decap 会读取它
      const target =
        `${CMS_URL}/admin/#access_token=${tokenData.access_token}` +
        `&token_type=bearer&scope=${encodeURIComponent(tokenData.scope || 'repo')}`;
      return Response.redirect(target, 302);
    }

    // ---- 其他路径：404 ----
    return new Response('Not Found', { status: 404 });
  }
};
