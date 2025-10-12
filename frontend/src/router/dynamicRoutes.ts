import type { Router } from 'vue-router'
const viewModules = import.meta.glob('../views/{configuracion, flujo}/**/*.vue')

const normalizedViewMap = new Map()

for (const [key, importer] of Object.entries(viewModules)) {
  const normalizedKey = key.toLowerCase()
  normalizedViewMap.set(normalizedKey, importer)
}

console.log(normalizedViewMap)

function normalizePath(url: string): string {
  return '/' + url.replace(/^\/+/, '').replace(/\/+$/, '')
}

export function registerDynamicRoutes(router: Router, menuItems: any[]) {
  const layoutRouteName = 'main' // 👈 nombre del layout principal en router/index.ts
  const routes: any[] = []

  function addRoutesRecursively(items: any[]) {
    for (const item of items) {
      if (item.url) {
        const path = normalizePath(item.url)

        try {
          // Verifica si la vista existe en src/views
          const viewPath = `../views${path}.vue`

          const route = {
            path,
            name: item.id || item.name || path,
            component: normalizedViewMap.get(viewPath)
                    ? normalizedViewMap.get(viewPath)
                    : () => import('@/views/FallbackView.vue')
          }

          // 🔹 agregamos la ruta dentro del layout
          router.addRoute(layoutRouteName, route)
          routes.push(route)
        } catch (err) {
          console.warn(`[DynamicRoute] No se encontró la vista para: ${item.url}`)
        }
      }

      // recursividad
      if (item.submenu && item.submenu.length) {
        addRoutesRecursively(item.submenu)
      }
    }
  }

  addRoutesRecursively(menuItems)

  // ✅ Asegurar que el fallback también esté dentro del layout principal
  const hasFallback = router.getRoutes().some(r => r.name === 'NotFound')
  if (!hasFallback) {
    router.addRoute('main', {
      path: ':pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/FallbackView.vue')
    })
  }

  console.log('✅ Rutas dinámicas registradas dentro del layout:', routes)
}








