<template>
  <router-view />
</template>
<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuth } from '@/utils/useAuth'

const auth = useAuth()

onMounted(() => {
  auth.restoreSession()
})
</script>





