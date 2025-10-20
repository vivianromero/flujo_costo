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
import { useMenuStore } from '@/stores/menu'
import { registerDynamicRoutes } from '@/router/dynamicRoutes'

const router = useRouter()
const session = useSessionStore()
const menuStore = useMenuStore()

const menu = ref([])
const openItems = ref([])

function navigate(url) {
  router.push(url)
}

function closeSiblings(parentSubmenu, currentId) {
  if (!parentSubmenu) return
  for (const sibling of parentSubmenu) {
    if (sibling.id !== currentId) {
      const index = openItems.value.indexOf(sibling.id)
      if (index !== -1) openItems.value.splice(index, 1)
    }
  }
}

function toggleItem({ item, parentSubmenu }) {
  const id = item.id
  const isOpen = openItems.value.includes(id)

  if (isOpen) {
    openItems.value = openItems.value.filter(openId => openId !== id)
  } else {
    closeSiblings(parentSubmenu, id)
    openItems.value.push(id)
  }
}

onMounted(async () => {
  try {
    const response = await fetch('/api/menu', {
      headers: {
        'Authorization': `JWT ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()

    menu.value = data
    menuStore.setMenu(menu.value)

    // ✅ Registra rutas dinámicas basadas en el menú
    registerDynamicRoutes(router, menuStore.items)

  } catch (error) {
    console.error('[Menu] ❌ Error al cargar el menú:', error)
  }
})

</script>




