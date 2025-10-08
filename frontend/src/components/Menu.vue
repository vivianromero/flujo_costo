<template>
  <q-list>
    <MenuItem
      v-for="item in menu"
      :key="item.id"
      :item="item"
      :level="0"
      @navigate="navigate"
    />
  </q-list>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MenuItem from './MenuItem.vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const session = useSessionStore()
const menu = ref([])

function navigate(url) {
  router.push(url)
}

onMounted(async () => {
  const response = await fetch('/api/menu', {
    headers: { Authorization: `Bearer ${session.token}` }
  })
  menu.value = await response.json()
})

onMounted(async () => {
  try {
    const response = await fetch('/api/menu', {
      method: 'GET',
      headers: {
        'Authorization': `JWT ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) {
      console.error('Error al cargar el menú:', response.status)
      return
    }

    menu.value = await response.json()
  } catch (error) {
    console.error('Error de red al cargar el menú:', error)
  }
})

</script>
