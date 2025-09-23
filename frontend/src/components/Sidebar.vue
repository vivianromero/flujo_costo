<template>
  <aside class="sidebar">
    <nav>
      <ul>
        <li @click="navigate('dashboard')">Dashboard</li>
        <li @click="navigate('configuracion')">Configuración</li>
        <li @click="navigate('perfil')">Perfil</li>
        <li @click="navigate('costos')">Costos</li>
        <li @click="navigate('administrativo')">Administrativo</li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import '@/assets/css/sidebar.css'
const router = useRouter()

function navigate(ruta) {
  router.push(`/${ruta}`)
}
</script>
