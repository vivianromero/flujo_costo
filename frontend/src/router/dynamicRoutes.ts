import type { Router } from 'vue-router'
import { useSessionStore } from '@/stores/session'

// 🔹 Importa automáticamente TODAS las vistas en estas carpetas
const viewModules = import.meta.glob('../views/{configuracion,flujo}/**/*.vue', { eager: false })

// 🔹 Mapa normalizado para búsquedas case-insensitive
const normalizedViewMap = new Map<string, () => Promise<any>>()
for (const [key, importer] of Object.entries(viewModules)) {
  const normalizedKey = key.toLowerCase()
  normalizedViewMap.set(normalizedKey, importer as () => Promise<any>)
}

function normalizePath(url: string): string {
  return '/' + url.replace(/^\/+/, '').replace(/\/+$/, '')
}

// ===========================================================
// ✅ REGISTRO DE RUTAS DINÁMICAS
// ===========================================================
export function registerDynamicRoutes(router: Router, menuItems: any[]) {
  const layoutRouteName = 'main' // 👈 coincide con el nombre en index.ts
  const routes: any[] = []

  function addRoutesRecursively(items: any[]) {
    for (const item of items) {
      if (item.url) {
        const path = normalizePath(item.url)
        const viewPath = `../views${path}.vue`.toLowerCase()

        const component =
          normalizedViewMap.get(viewPath) ??
          (() => import('@/views/FallbackView.vue'))

        const route = {
          path,
          name: item.id || item.name || path,
          component,
          meta: { requiresAuth: true }
        }

        // Agregamos la ruta como hija del layout principal
        try {
          router.addRoute(layoutRouteName, route)
          routes.push(route)
        } catch (err) {
          console.warn(`[DynamicRoute] No se pudo registrar ruta: ${path}`, err)
        }
      }

      if (item.submenu?.length) {
        addRoutesRecursively(item.submenu)
      }
    }
  }

  addRoutesRecursively(menuItems)

  // ✅ Asegurar que FallbackView esté dentro del layout
  const hasFallback = router.getRoutes().some((r) => r.name === '')
  if (!hasFallback) {
    router.addRoute(layoutRouteName, {
      path: ':pathMatch(.*)*',
      name: '',
      component: () => import('@/views/FallbackView.vue'),
    })
  }

  // ✅ Guardamos el menú en localStorage (para restaurar tras F5)
  try {
    localStorage.setItem('dynamicMenu', JSON.stringify(menuItems))
  } catch (err) {
    console.warn('⚠️ No se pudo guardar el menú dinámico en localStorage:', err)
  }
  return routes
}

// ===========================================================
// 🔁 RESTAURAR RUTAS DESDE LOCALSTORAGE
// ===========================================================
export function restoreDynamicRoutes(router: Router, session: ReturnType<typeof useSessionStore>) {
  const saved = localStorage.getItem('dynamicMenu')
  if (!saved) return

  try {

    const token = session.token || localStorage.getItem('token')
    if (!token) {
      console.warn('🔒 No se restauran rutas: usuario no autenticado')
      return
    }

    const menuItems = JSON.parse(saved)
    registerDynamicRoutes(router, menuItems)
  } catch (err) {
    console.error('❌ Error al restaurar rutas dinámicas:', err)
  }
}










