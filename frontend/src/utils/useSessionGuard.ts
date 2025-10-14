import { useSessionStore } from '@/stores/session'
import { useMenuStore } from '@/stores/menu'

export async function useSessionGuard(router: Router) {
  const session = useSessionStore()
  const menuStore = useMenuStore()

  // ⏳ Esperar a que el menú esté restaurado
  if (!Array.isArray(menuStore.items) || menuStore.items.length === 0) {
    const saved = localStorage.getItem('dynamicMenu')
    if (saved) {
      try {
        const menuItems = JSON.parse(saved)
        menuStore.items = menuItems // ✅ restaurar en el store
      } catch (err) {
        console.error('❌ Error al restaurar menú:', err)
      }
    }
  }

  // ✅ Ahora sí registrar el guard
  router.beforeEach((to, from, next) => {
    const token = session.token || localStorage.getItem('token')

    if (to.meta.public) {
      next()
      return
    }

    if (!token) {
      next({ name: 'login' })
      return
    }

    if (to.name === 'login' && token) {
      next({ name: 'home' })
      return
    }

    if (to.name === 'home' && token) {
      next()
      return
    }

    if (!to.name && Array.isArray(menuStore.items) && menuStore.items.length != 0 && session.username) {
      console.warn('⚠️ No hay ítems en el menú')
      next({ name: 'noaccess' })
      return
    }

    if (Array.isArray(menuStore.items) && menuStore.items.length != 0 && !session.username) {
      console.warn(`🚫 Ruta no permitida: ${to.name}`)
      next({ name: 'unauthorized' })
      return
    }
    next()
  })
}


