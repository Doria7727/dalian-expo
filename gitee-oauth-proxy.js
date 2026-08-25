// ============================================================
// Decap CMS 连接 Gitee 的 OAuth 代理（Cloudflare Worker）
// ------------------------------------------------------------
// 为什么需要它：Gitee 没有像 Netlify 那样的一键身份服务，
// Decap CMS 要连 Gitee 改写仓库内容，必须有一个后端来中转 OAuth。
// 本文件部署到 Cloudflare Workers（免费），国内也能访问。
//
// 部署后需在 Cloudflare 控制台设置 3 个环境变量（Secrets）：
//   GITEE_CLIENT_ID     = 你的 Gitee OAuth 应用 Client ID
//   GITEE_CLIENT_SECRET = 你的 Gitee OAuth 应用 Client Secret
//   REDIRECT_URI        = https://你的worker子域.workers.dev/callback
//
// 然后把上面的 REDIRECT_URI 填进 Gitee OAuth 应用的“回调地址”。
// 把 worker 地址（如 https://xxx.workers.dev）填进 admin/config.yml 的 auth_endpoint。
// ============================================================

const GITEE_API = 'https://gitee.com/api/v5'

// 处理跨域（Decap 后台与代理通常不同域，需允许带 cookie 的跨域请求）
function corsHeaders(request) {
  const origin = request.headers.get('Origin') || '*'
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,PATCH,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
  }
}

function withCors(response, request) {
  const h = corsHeaders(request)
  for (const k in h) response.headers.set(k, h)
  return response
}

function getToken(request) {
  const cookie = request.headers.get('Cookie') || ''
  const m = cookie.match(/gitee_token=([^;]+)/)
  return m ? m[1] : null
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const p = url.pathname

    // 预检请求（浏览器跨域 POST/PUT 会先发 OPTIONS）
    if (request.method === 'OPTIONS') {
      return withCors(new Response(null, { status: 204 }), request)
    }

    // 1) 登录：跳转到 Gitee 授权页
    if (p === '/auth') {
      const target = 'https://gitee.com/oauth/authorize?response_type=code' +
        '&client_id=' + env.GITEE_CLIENT_ID +
        '&redirect_uri=' + encodeURIComponent(env.REDIRECT_URI) +
        '&scope=projects'
      return Response.redirect(target, 302)
    }

    // 2) 回调：用 code 换 token，写入 HttpOnly Cookie，跳回后台
    if (p === '/callback') {
      const code = url.searchParams.get('code')
      if (!code) return new Response('missing code', { status: 400 })
      const resp = await fetch('https://gitee.com/oauth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          grant_type: 'authorization_code',
          code,
          client_id: env.GITEE_CLIENT_ID,
          client_secret: env.GITEE_CLIENT_SECRET,
          redirect_uri: env.REDIRECT_URI
        })
      })
      const json = await resp.json()
      const token = json.access_token
      if (!token) {
        return new Response('token exchange failed: ' + JSON.stringify(json), { status: 400 })
      }
      const r = Response.redirect('/admin/', 302)
      r.headers.append('Set-Cookie',
        'gitee_token=' + token + '; Path=/; HttpOnly; Secure; SameSite=None; Max-Age=3600')
      return r
    }

    // 3) 当前登录用户
    if (p === '/user') {
      const token = getToken(request)
      if (!token) {
        return withCors(new Response(JSON.stringify({}),
          { status: 401, headers: { 'Content-Type': 'application/json' } }), request)
      }
      const u = await fetch(GITEE_API + '/user?access_token=' + token).then(r => r.json())
      return withCors(new Response(JSON.stringify(u),
        { status: 200, headers: { 'Content-Type': 'application/json' } }), request)
    }

    // 4) 代理所有 Gitee API 请求（/repos/... 等），自动附带 token
    const token = getToken(request)
    if (!token) {
      return withCors(new Response(JSON.stringify({ message: 'unauthorized' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }), request)
    }
    const qs = url.searchParams.toString()
    const target = GITEE_API + p + (qs ? '?' + qs + '&' : '?') + 'access_token=' + token
    const init = { method: request.method, headers: {} }
    for (const [k, v] of request.headers) {
      if (['content-type', 'accept', 'user-agent'].includes(k.toLowerCase())) init.headers[k] = v
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      init.body = request.body
    }
    const apiResp = await fetch(target, init)
    const body = await apiResp.text()
    return withCors(new Response(body, {
      status: apiResp.status,
      headers: { 'Content-Type': apiResp.headers.get('Content-Type') || 'application/json' }
    }), request)
  }
}
