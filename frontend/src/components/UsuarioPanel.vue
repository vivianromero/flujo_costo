<template>
  <div class="usuario-area">
    <i class="fas fa-user user-circle"></i>
    <div class="user-info">
      <span class="username">{{ session.username || 'Usuario Anónimo' }}</span>
      <span class="ueb">Unidad: {{ session.ueb || 'Sin UEB' }}</span>
    </div>
    <button class="logout-btn" @click="logout">Salir</button>
  </div>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'
import { useRouter } from 'vue-router'

const session = useSessionStore()
const router = useRouter()

function logout() {
  sessionStorage.clear()
  session.clearSession()
  router.push('/login')
}
</script>











