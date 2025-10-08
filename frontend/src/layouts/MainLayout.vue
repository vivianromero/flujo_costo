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
            <span class="q-ml-sm text-subtitle2">{{ session.username || 'Usuario Anónimo' }}</span>
          </div>
        </q-toolbar-title>
         <!-- Botón salir a la derecha -->
        <q-btn flat dense round icon="fa-solid fa-right-from-bracket" color="white" @click="logout">
            <q-tooltip>Salir</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <!-- Drawer -->
    <q-drawer v-model="leftDrawerOpen" side="left" overlay bordered :width="drawerWidth">
      <div class="drawer-content">
        <Menu />
      </div>
      <div class="resize-handle" @mousedown="startResize" />
    </q-drawer>

    <!-- Page container -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <q-footer reveal bordered class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          <span class="q-ml-sm">Pie de página</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script setup>
    import { ref } from 'vue'
    const leftDrawerOpen = ref(true)
    const drawerWidth = ref(260)


    import { useRouter } from 'vue-router'
    import { useSessionStore } from '@/stores/session'

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

    function startResize(e, MouseEvent) {
      const startX = e.clientX
      const startWidth = drawerWidth.value

      const onMouseMove = (moveEvent, MouseEvent) => {
        const delta = moveEvent.clientX - startX
        drawerWidth.value = Math.max(200, startWidth + delta) // mínimo 200px
      }

      const onMouseUp = () => {
        window.removeEventListener('mousemove', onMouseMove)
        window.removeEventListener('mouseup', onMouseUp)
      }

      window.addEventListener('mousemove', onMouseMove)
      window.addEventListener('mouseup', onMouseUp)
    }
</script>



