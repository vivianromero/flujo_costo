<template>
  <q-layout view="hHh lpR fFf">
    <!-- ===== HEADER ===== -->
    <q-header reveal bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="fa-solid fa-bars"
          color="white"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>
          <div class="row items-center no-wrap">
            <q-avatar circled size="32px" class="bg-blue-2 text-white">
              <q-icon name="fa-solid fa-user" />
            </q-avatar>

            <div class="column q-ml-sm">
              <span class="text-subtitle2">
                {{ session.username || 'Usuario Anónimo' }}
              </span>
              <span class="text-caption text-grey-3">
                Unidad: {{ session.ueb || 'Sin UEB' }}
              </span>
            </div>
          </div>
        </q-toolbar-title>

        <!-- Botón salir -->
        <q-btn
          flat
          dense
          round
          icon="fa-solid fa-right-from-bracket"
          color="white"
          @click="logout"
        >
          <q-tooltip>Salir</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <!-- ===== DRAWER ===== -->
    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      behavior="desktop"
      bordered
      :width="drawerWidth"
      class="relative-position"
    >
      <div class="drawer-content full-height scroll">
        <Menu />
      </div>

      <!-- Handle para resize -->
      <div class="resize-corner" @mousedown="startResize" />
    </q-drawer>

    <!-- ===== CONTENIDO PRINCIPAL ===== -->
    <q-page-container>
      <!-- 🧭 Breadcrumbs -->
      <q-breadcrumbs
          class="q-pa-sm bg-grey-2 text-grey-8"
          separator-icon="chevron_right"
          v-if="breadcrumbs.length"
        >
          <q-breadcrumbs-el
            v-for="(crumb, index) in breadcrumbs"
            :key="index"
            :label="crumb.label"
            :to="crumb.to"
            :icon="crumb.icon"
            clickable
          />
        </q-breadcrumbs>


      <!-- (Solo para debug) -->
      <!-- <pre class="q-pa-sm bg-grey-1 text-black">{{ breadcrumbs }}</pre> -->

      <router-view />
    </q-page-container>

    <!-- ===== FOOTER ===== -->
    <Footer/>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router'
import Menu from '@/components/Menu.vue'
import { useSessionStore } from '@/stores/session'
import { useMenuStore } from '@/stores/menu'
import Footer from '@/components/Footer.vue'
import { apolloClient } from '@/apollo/client'
import { createCrudListView } from '@/factories/createCrudListView'


/* ───────────────────────────────
   🔧 Estado y dependencias
──────────────────────────────── */
const leftDrawerOpen = ref(true)
const drawerWidth = ref(290)
const isResizing = ref(false)
const router = useRouter()
const route = useRoute()
const session = useSessionStore()
const menuStore = useMenuStore()

/* ───────────────────────────────
   🚪 Control del Drawer
──────────────────────────────── */
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function startResize(e: MouseEvent) {
  e.preventDefault()
  e.stopPropagation()

  isResizing.value = true
  const startX = e.clientX
  const startWidth = drawerWidth.value

  function onMouseMove(moveEvent: MouseEvent) {
    if (!isResizing.value) return
    const delta = moveEvent.clientX - startX
    drawerWidth.value = Math.max(200, Math.min(500, startWidth + delta))
  }

  function onMouseUp() {
    isResizing.value = false
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }

  document.body.style.cursor = 'ew-resize'
  document.body.style.userSelect = 'none'
  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

/* ───────────────────────────────
   🔐 Logout
──────────────────────────────── */
function logout() {
  if (apolloClient) {
    apolloClient.clearStore()
  }
  session.token = null
  sessionStorage.clear()
  session.clearSession()
  localStorage.removeItem('token')
  router.push('/login')
}

/* ───────────────────────────────
   🧭 Breadcrumbs Dinámicos
──────────────────────────────── */
interface Breadcrumb {
  label: string
  to?: string | null
  icon?: string | null
}


const breadcrumbs = ref<Breadcrumb[]>([])

// Normaliza la URL (asegura que siempre empiece con /)
function normalizeUrl(url: string) {
  return '/' + url.replace(/^\/+/, '').replace(/\/+$/, '')
}

// Busca la ruta actual dentro del árbol del menú
function findPath(menu: any[], path: string, trail: any[] = []): any[] | null {
  for (const item of menu) {
    const currentTrail = [...trail, item]
    if (item.url && normalizeUrl(item.url) === path) {
      return currentTrail
    }
    if (item.submenu) {
      const found = findPath(item.submenu, path, currentTrail)
      if (found) return found
    }
  }
  return null
}

// Actualiza los breadcrumbs dinámicamente
function updateBreadcrumbs() {
  const currentPath = route.path

  // 🔹 Caso especial: ruta raíz "/" siempre muestra Inicio con icono
  if (currentPath === '/' || currentPath === '') {
    breadcrumbs.value = [{ label: 'Inicio', to: '/', icon: 'fa-solid fa-house' }]
    return
  }

  // 🔹 Si el menú no está disponible aún, deja el breadcrumb vacío
  if (!menuStore.items || !menuStore.items.length) {
    breadcrumbs.value = []
    return
  }

  // 🔹 Buscar ruta actual en el menú
  const path = findPath(menuStore.items, currentPath)

  breadcrumbs.value = path
    ? [
        { label: 'Inicio', to: '/', icon: 'fa-solid fa-house' },
        ...path.map((item, i) => ({
          label: item.name,
          to: i < path.length - 1 && item.url ? normalizeUrl(item.url) : null,
          icon: item.icon_class || null
        }))
      ]
    : [{ label: 'Inicio', to: '/', icon: 'fa-solid fa-house' }]
}



/* ───────────────────────────────
   📡 Reacciones a cambios
──────────────────────────────── */

// Cuando cambia la ruta
onBeforeRouteUpdate((to, from, next) => {
  updateBreadcrumbs()
  next()
})

// Cuando el menú o la ruta cambian
watch(
  [() => route.path, () => menuStore.items],
  ([newPath, newMenu]) => {
    if (newMenu && newMenu.length) {
      updateBreadcrumbs()
    }
  },
  { immediate: true, deep: true }
)

// También actualiza cuando se monta el layout
onMounted(() => {
  updateBreadcrumbs() // 👈 fuerza actualización inmediata
})

</script>





