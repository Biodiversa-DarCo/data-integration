<template>
  <span class="text-no-wrap">
    {{ maybe ? "(" : "" }}
    <v-icon icon="mdi-hexagram" color="red" size="small"></v-icon>
    {{ maybe ? ")" : "" }}
  </span>
</template>

<script setup lang="ts">
defineProps<{ maybe?: true }>();
</script>

<style scoped lang="scss"></style>
