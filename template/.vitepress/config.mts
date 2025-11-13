import { withMermaid } from "vitepress-plugin-mermaid";
// https://vitepress.dev/reference/site-config
export default withMermaid({
  srcDir: ".",
  title: "DarCo data migration",
  description: "Data migration template and docs for DarCo project",
  base: '/data-integration/',
  head: [['link', { rel: 'icon', href: '/data-integration/DarCo.png' }]],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      // { text: 'Download template', link: withBase('/template.xlsx'), rel: 'external', target: '_blank' },
    ],

    sidebar: [
      {
        text: 'Guidelines',
        link: '/README',
      }
    ],

    // socialLinks: [
    //   { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    // ]
  },
  mermaidPlugin: {
    class: "mermaid mermaid-graph"
  }
})
