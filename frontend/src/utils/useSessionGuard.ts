import { useSessionStore } from '@/stores/session'
import { useMenuStore } from '@/stores/menu'
import type { Router } from 'vue-router'

export async function useSessionGuard(router: Router) {
  const session = useSessionStore()
  const menuStore = useMenuStore()

  const token = sessionStorage.getItem('token')
  session.token = token

  if (!token) {
    console.warn('🔒 No hay token, redirigiendo a /unauthorized')
    session.clearSession()
    router.push({ name: 'unauthorized' })
    return
  }
}


