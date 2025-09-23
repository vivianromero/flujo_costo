<template>
  <div class="home">
    <h1>Bienvenida, {{ session.username }}</h1>
    <p>UEB: {{ session.ueb }}</p>
    <p>Rol: {{ session.role }}</p>

    <p>Este es el panel principal del sistema TABACUBA.</p>
  </div>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'
const session = useSessionStore()
</script>




