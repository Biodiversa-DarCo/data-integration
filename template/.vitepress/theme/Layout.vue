<script setup lang="ts">
import DefaultTheme from "vitepress/theme";
const { Layout } = DefaultTheme;
import { withBase } from "vitepress";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiDownload } from "@mdi/js";
</script>

<template>
  <Layout>
    <!-- Slot for extra navbar content -->
    <template #nav-bar-content-after>
      <a
        :href="withBase('/template.xlsx')"
        download
        target="_blank"
        rel="noopener noreferrer"
        class="VPLink link VPNavBarMenuLink"
        style="
          margin-left: 20px;
          background-color: #3e63dd;
          padding: 5px;
          border-radius: 5px;
          color: white;
          display: flex;
          align-items: center;
          font-size: 12px;
          gap: 5px;
        "
      >
        <svg-icon type="mdi" :path="mdiDownload" :size="18"></svg-icon>
        <span> Download template </span>
      </a>
    </template>
  </Layout>
</template>
