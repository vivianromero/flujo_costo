import { defineStore } from 'pinia'
import { registerDynamicRoutes } from '@/router/dynamicRoutes'
import { router } from '@/router'

function normalizeMenu(items: any[]) {
  items.forEach(item => {
    if (item.url) {
      // Asegura que todas las rutas empiecen con "/"
      item.url = '/' + item.url.replace(/^\/+/, '')
    }
    if (item.submenu) normalizeMenu(item.submenu)
  })
}

export const useMenuStore = defineStore('menu', {
  state: () => ({
    items: [] as any[]
  }),
  actions: {
    async loadMenu() {
      const response = await api.get('/menu')
      const data = response.data
      normalizeMenu(data)
      this.items = data
    },
    setMenu(data: any[]) {
      this.items = data
    }
  }
})

