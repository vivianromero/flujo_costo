import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import Login from '@/views/Login.vue'
import { useSessionStore } from '@/stores/session'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { public: true } // 👈 útil si más adelante agregas roles o autenticación avanzada
  },
  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import('@/views/UnauthorizedView.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'main', // 👈 layout principal
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Inicio.vue'),
        meta: { breadcrumb: 'Inicio', icon: 'fa-solid fa-home' }
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})


// ✅ Protección de rutas
router.beforeEach((to, from, next) => {
  const session = useSessionStore()
  const token = session.token || localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'unauthorized' }) // 👈 redirige aquí en vez de login
  } else if (to.name === 'login' && token) {
    next({ name: 'home' })
  } else {
    next()
  }
})

// ✅ Exportación por defecto opcional (para main.ts)
export default router








