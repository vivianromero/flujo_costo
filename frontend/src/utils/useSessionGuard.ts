import { useSessionStore } from '@/stores/session'
import { useMenuStore } from '@/stores/menu'

export async function useSessionGuard(router: Router) {

  router.beforeEach((to, from, next) => {
      const session = useSessionStore()
      const token = session.token || localStorage.getItem('token')

      // 1️⃣ Si la ruta es pública, continuar
      if (to.meta.public) {
        next()
        return
      }

      // 2️⃣ Si no hay token, redirigir al login
      if (!token) {
        next({ name: 'login' })
        return
      }

      // 3️⃣ Si intenta ir al login con token, redirigir al home
      if (to.name === 'login' && token) {
        next({ name: 'home' })
        return
      }

      if (to.name === 'home' && token) {
        next()
      }

      // 4️⃣ Validar si tiene acceso a la ruta por su nombre
      const menuStore = useMenuStore()

      if (!to.name && (!Array.isArray(menuStore.items) || menuStore.items.length === 0)) {
          console.warn('⚠️ No hay ítems en el menú')
          next({ name: 'noaccess' })
          return
      }

      if (to.name && (!Array.isArray(menuStore.items) || menuStore.items.length === 0)) {
        console.warn(`🚫 Ruta no permitida: ${to.name}`)
        next({ name: 'unauthorized' })
        return
      }

      // 5️⃣ Continuar si todo está bien
      next()
    })
}


