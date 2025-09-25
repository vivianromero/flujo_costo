<template>
  <q-header elevated class="header-institucional">
    <div class="row items-center justify-between full-width q-px-xl q-py-sm">

      <!-- Logo institucional -->
      <LogoEmpresa />

      <!-- Panel de usuario embebido -->
      <div class="row items-center" style="gap: 16px;">
        <q-icon name="person" size="md" color="blue-10" />
        <span style="font-size: 16px; font-weight: 500; color: #003366;">VivianR</span>
        <q-btn
          label="Salir"
          color="white"
          text-color="brown-10"
          unelevated
          style="font-weight: bold; padding: 6px 12px; border-radius: 4px;"
          @click="logout"
        />
      </div>

    </div>
  </q-header>
</template>

<script setup lang="ts">
import LogoEmpresa from '@/components/LogoEmpresa.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  router.push('/login')
}
</script>






