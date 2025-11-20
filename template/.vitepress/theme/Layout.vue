<script setup lang="ts">
import { withBase } from "vitepress";
import DefaultTheme from "vitepress/theme";
const { Layout } = DefaultTheme;
</script>

<template>
  <Layout>
    <!-- Slot for extra navbar content -->
    <template #nav-bar-content-after>
      <v-btn
        :href="withBase('/template.xlsx')"
        target="_blank"
        prepend-icon="mdi-download"
        size="small"
        color="primary"
        class="ml-3"
      >
        Download template
      </v-btn>
    </template>
  </Layout>
</template>
