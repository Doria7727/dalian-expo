// Decap CMS 配置（JS 版，对应 admin/config.yml，避免 fetch 失败问题）
window.CMS_CONFIG = {
  backend: {
    name: 'github',
    repo: 'Doria7727/dalian-expo',
    branch: 'main',
    client_id: 'Ov23liHFOwbuQpQyNCD6',
    // 自建 OAuth 代理（Cloudflare Worker，避开 Netlify 默认 api.netlify.com 的 Not Found）
    auth_endpoint: 'https://dalian-expo-oauth.1060200619.workers.dev'
  },
  media_folder: 'assets/img/uploads',
  public_folder: '/assets/img/uploads',
  locale: 'zh',
  collections: [
    {
      name: 'site',
      label: '网站内容',
      label_singular: '网站内容',
      description: '编辑展会全部文字内容，保存即重新发布',
      files: [
        {
          name: 'data',
          label: '全部内容 (data.json)',
          file: 'assets/js/data.json',
          fields: [
            {
              name: 'SITE',
              label: '展会基本信息',
              widget: 'object',
              fields: [
                { name: 'name', label: '展会全称', widget: 'string' },
                { name: 'shortName', label: '简称', widget: 'string' },
                { name: 'enName', label: '英文名称', widget: 'string' },
                { name: 'edition', label: '届数', widget: 'string' },
                { name: 'year', label: '年份', widget: 'string' },
                { name: 'theme', label: '主题', widget: 'string' },
                { name: 'dateText', label: '展期文字', widget: 'string' },
                { name: 'dateStart', label: '开始日期', widget: 'date' },
                { name: 'dateEnd', label: '结束日期', widget: 'date' },
                { name: 'venue', label: '展馆名称', widget: 'string' },
                { name: 'venueAddr', label: '展馆地址', widget: 'string' },
                {
                  name: 'stats',
                  label: '核心数据条',
                  widget: 'list',
                  fields: [
                    { name: 'num', label: '数值', widget: 'string' },
                    { name: 'label', label: '说明', widget: 'string' }
                  ]
                },
                { name: 'organizer', label: '主办单位', widget: 'string' },
                { name: 'coOrganizer', label: '承办/背书', widget: 'string' },
                {
                  name: 'contact',
                  label: '联系方式',
                  widget: 'object',
                  fields: [
                    { name: 'phone', label: '电话', widget: 'string' },
                    { name: 'email', label: '邮箱', widget: 'string' },
                    { name: 'wechat', label: '微信', widget: 'string' },
                    { name: 'address', label: '地址', widget: 'string' }
                  ]
                }
              ]
            },
            {
              name: 'NAV',
              label: '导航菜单',
              widget: 'list',
              fields: [
                { name: 'label', label: '显示文字', widget: 'string' },
                { name: 'href', label: '链接文件', widget: 'string' },
                { name: 'page', label: '页面标识', widget: 'string' }
              ]
            },
            {
              name: 'ABOUT',
              label: '展会介绍',
              widget: 'object',
              fields: [
                { name: 'intro', label: '简介', widget: 'text' },
                {
                  name: 'highlights',
                  label: '四大亮点',
                  widget: 'list',
                  fields: [
                    { name: 'ic', label: '图标', widget: 'string' },
                    { name: 'title', label: '标题', widget: 'string' },
                    { name: 'desc', label: '描述', widget: 'text' }
                  ]
                },
                { name: 'vision', label: '愿景口号', widget: 'string' },
                {
                  name: 'sections',
                  label: '详细介绍段落',
                  widget: 'list',
                  fields: [
                    { name: 'h', label: '小标题', widget: 'string' },
                    { name: 'p', label: '正文', widget: 'text' }
                  ]
                }
              ]
            },
            {
              name: 'EXHIBIT_SCOPE',
              label: '展品范围（展区）',
              widget: 'list',
              fields: [
                { name: 'group', label: '展区名称', widget: 'string' },
                {
                  name: 'items',
                  label: '展品明细',
                  widget: 'list',
                  summary: '{{fields.text}}',
                  field: { name: 'text', label: '展品', widget: 'string' }
                }
              ]
            },
            {
              name: 'EXHIBITORS',
              label: '展商名录',
              widget: 'list',
              fields: [
                { name: 'name', label: '企业名称', widget: 'string' },
                { name: 'category', label: '所属展区', widget: 'string' },
                { name: 'booth', label: '展位/标注', widget: 'string' },
                { name: 'desc', label: '简介', widget: 'text' },
                { name: 'logo', label: 'Logo 文字', widget: 'string' }
              ]
            },
            {
              name: 'NEWS',
              label: '新闻动态',
              widget: 'list',
              fields: [
                { name: 'id', label: '编号', widget: 'string' },
                { name: 'title', label: '标题', widget: 'string' },
                { name: 'date', label: '日期', widget: 'date' },
                { name: 'category', label: '分类', widget: 'string' },
                { name: 'summary', label: '摘要', widget: 'text' },
                { name: 'cover', label: '封面背景(CSS)', widget: 'string' },
                {
                  name: 'body',
                  label: '正文段落',
                  widget: 'list',
                  summary: '{{fields.text}}',
                  field: { name: 'text', label: '段落', widget: 'text' }
                }
              ]
            },
            {
              name: 'SCHEDULE',
              label: '同期活动',
              widget: 'list',
              fields: [
                { name: 'day', label: '活动板块', widget: 'string' },
                {
                  name: 'sessions',
                  label: '场次',
                  widget: 'list',
                  fields: [
                    { name: 'time', label: '时间', widget: 'string' },
                    { name: 'title', label: '标题', widget: 'string' },
                    { name: 'meta', label: '说明', widget: 'string' }
                  ]
                }
              ]
            },
            {
              name: 'TRANSPORT',
              label: '交通指南',
              widget: 'list',
              fields: [
                { name: 'ic', label: '图标', widget: 'string' },
                { name: 'h', label: '方式', widget: 'string' },
                { name: 'p', label: '说明', widget: 'text' }
              ]
            },
            {
              name: 'HOTELS',
              label: '酒店指南',
              widget: 'list',
              fields: [
                { name: 'name', label: '酒店名称', widget: 'string' },
                { name: 'dist', label: '距离', widget: 'string' },
                { name: 'price', label: '价格', widget: 'string' },
                { name: 'note', label: '备注', widget: 'string' }
              ]
            },
            {
              name: 'APPLY_INFO',
              label: '参展报名信息',
              widget: 'object',
              fields: [
                {
                  name: 'fee',
                  label: '展位费用',
                  widget: 'list',
                  fields: [
                    { name: 'type', label: '类型', widget: 'string' },
                    { name: 'price', label: '价格', widget: 'string' },
                    { name: 'note', label: '说明', widget: 'text' }
                  ]
                },
                {
                  name: 'steps',
                  label: '报名流程',
                  widget: 'list',
                  fields: [
                    { name: 't', label: '步骤标题', widget: 'string' },
                    { name: 'p', label: '说明', widget: 'text' }
                  ]
                },
                {
                  name: 'faq',
                  label: '常见问题',
                  widget: 'list',
                  fields: [
                    { name: 'q', label: '问题', widget: 'string' },
                    { name: 'a', label: '答案', widget: 'text' }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
};
