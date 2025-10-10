<template>
  <q-list>
    <MenuItem
      v-for="item in menu"
      :key="item.id"
      :item="item"
      :level="0"
      :open-items="openItems"
      :parent-submenu="menu"
      @toggle="toggleItem"
      @navigate="navigate"
    />
  </q-list>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import MenuItem from './MenuItem.vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const session = useSessionStore()
const menu = ref([])
const openItems = ref([])

function navigate(url) {
  console.log('[NAVIGATE]', url)
  router.push(url)
}

function closeSiblings(parentSubmenu, currentId) {
  console.log('[CLOSE SIBLINGS]', { parentSubmenu, currentId })
  if (!parentSubmenu) return
  for (const sibling of parentSubmenu) {
    if (sibling.id !== currentId) {
      const index = openItems.value.indexOf(sibling.id)
      if (index !== -1) openItems.value.splice(index, 1)
    }
  }
}

function toggleItem({ item, parentSubmenu }) {
  console.log('[TOGGLE ITEM]', { id: item.id, parentSubmenu })
  const id = item.id
  const isOpen = openItems.value.includes(id)

  if (isOpen) {
    console.log('→ CERRAR', id)
    openItems.value = openItems.value.filter(openId => openId !== id)
  } else {
    console.log('→ ABRIR', id)
    closeSiblings(parentSubmenu, id)
    openItems.value.push(id)
  }
}

watch(openItems, (val) => {
  console.log('[OPEN ITEMS UPDATED]', JSON.stringify(val))
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
    const data = await response.json()
    console.log('[MENU LOADED]', data)
    menu.value = data
  } catch (error) {
    console.error('Error de red al cargar el menú:', error)
  }
})
</script>


