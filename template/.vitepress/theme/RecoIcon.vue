<template>
  <span class="text-no-wrap">
    {{ maybe ? "(" : "" }}
    <v-icon icon="mdi-circle-medium" color="primary" size="small"></v-icon>
    {{ maybe ? ")" : "" }}
  </span>
</template>

<script setup lang="ts">
defineProps<{ maybe?: true }>();
</script>

<style scoped lang="scss"></style>
