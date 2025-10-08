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
</script>
