import DefaultTheme from "vitepress/theme";
import Layout from "./Layout.vue";

import { Theme } from "vitepress";
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles';
import ReqIcon from "./ReqIcon.vue";
import RecoIcon from "./RecoIcon.vue";

const vuetify = createVuetify({
  components, directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    }
  }
})

const theme: Theme = {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.use(vuetify)
    app.component('ReqIcon', ReqIcon)
    app.component('RecoIcon', RecoIcon)
  },
};

export default theme;