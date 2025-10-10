<template>
  <q-layout view="hHh lpR fFf">
    <!-- Header -->
    <q-header reveal bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="fa-solid fa-bars" color="white" @click="toggleLeftDrawer" />
        <q-toolbar-title>
          <div class="row items-center no-wrap">
            <q-avatar circled size="32px" class="bg-blue-2 text-white">
              <q-icon name="fa-solid fa-user" />
            </q-avatar>

            <div class="column q-ml-sm">
              <span class="text-subtitle2">{{ session.username || 'Usuario Anónimo' }}</span>
              <span class="text-caption text-grey-3">Unidad: {{ session.ueb || 'Sin UEB' }}</span>
            </div>
          </div>
        </q-toolbar-title>
        <!-- Botón salir a la derecha -->
        <q-btn flat dense round icon="fa-solid fa-right-from-bracket" color="white" @click="logout">
          <q-tooltip>Salir</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <!-- Drawer -->
    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      overlay
      bordered
      :width="drawerWidth"
      class="relative-position"
    >
      <!-- Contenido del menú -->
      <div class="drawer-content full-height scroll">
        <Menu />
      </div>

      <!-- Handle de resize en esquina inferior derecha -->
      <div
        class="resize-corner"
        @mousedown="startResize"
      />
    </q-drawer>

    <!-- Page container -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <q-footer reveal bordered class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <span class="q-ml-sm">Pie de página</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import Menu from '@/components/Menu.vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

const leftDrawerOpen = ref(true)
const drawerWidth = ref(290)
const isResizing = ref(false)
const router = useRouter()
const session = useSessionStore()

function logout() {
  session.token = null
  sessionStorage.clear()
  session.clearSession()
  localStorage.removeItem('token')
  router.push('/login')
}

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function startResize(e) {
  e.preventDefault()
  e.stopPropagation()

  isResizing.value = true

  const startX = e.clientX
  const startWidth = drawerWidth.value

  function onMouseMove(moveEvent) {
    if (!isResizing.value) return

    const delta = moveEvent.clientX - startX
    const newWidth = Math.max(200, Math.min(500, startWidth + delta))

    drawerWidth.value = newWidth
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
</script>
