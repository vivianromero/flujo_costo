<template>
  <div class="breadcrumbs">
    <span v-for="(crumb, index) in crumbs" :key="index">
      <span>{{ crumb }}</span>
      <span v-if="index < crumbs.length - 1"> / </span>
    </span>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const crumbs = route.path.split('/').filter(Boolean)
</script>

<style scoped>
.breadcrumbs {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 1rem;
  background: #eaeaea;
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

</style>
