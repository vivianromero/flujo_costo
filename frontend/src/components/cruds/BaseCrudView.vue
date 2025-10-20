<script setup lang="ts">
defineProps<{
  component: any
}>()
</script>

<template>
  <div>
    <component :is="component" />
  </div>
</template>