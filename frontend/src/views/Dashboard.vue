<template>
  <div class="dashboard">
    <h2>Sistema de Gestión</h2>
    <div v-if="loading">Cargando datos...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <p>Bienvenida, <strong>{{ user.username }}</strong></p>
      <p>Email: {{ user.email }}</p>
      <!-- Aquí puedes agregar accesos a módulos: Configuración, Flujo, Costo -->
      <nav>
        <button @click="goTo('configuracion')">Configuración</button>
        <button @click="goTo('flujo')">Flujo</button>
        <button @click="goTo('costo')">Costo</button>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const user = ref({ username: '', email: '' })
const loading = ref(true)
const error = ref('')
const router = useRouter()

onMounted(async () => {
  const query = `
    query {
      me {
        username
        email
      }
    }
  `

  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/graphql/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `JWT ${token}`
      },
      body: JSON.stringify({ query })
    })

    const { data, errors } = await res.json()

    if (errors) {
      error.value = 'No se pudo obtener los datos del usuario'
    } else {
      user.value = data.me
    }
  } catch (e) {
    error.value = 'Error de red o servidor'
  } finally {
    loading.value = false
  }
})

function goTo(modulo: string) {
  router.push(`/${modulo}`)
}
</script>

