<template>
  <div style="display: flex; align-items: center; gap: 16px;">
    <q-icon name="person" size="md" color="blue-10" />
    <span style="font-size: 16px; font-weight: 500; color: #003366;">Vivian</span>
    <q-btn
      label="Salir"
      color="white"
      text-color="brown-10"
      unelevated
      style="font-weight: bold; padding: 6px 12px; border-radius: 4px;"
      @click="logout"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  router.push('/login')
}
</script>






