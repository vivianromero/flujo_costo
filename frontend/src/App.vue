<template>
  <router-view />
</template>
<script setup lang="ts">
import { useSessionGuard } from '@/utils/useSessionGuard'
import { useRouter } from 'vue-router'
import { ref, onMounted, watch } from 'vue'

const router = useRouter()
const loading = ref(true)


onMounted(async () => {
  await useSessionGuard(router)
  loading.value = false
})
</script>






