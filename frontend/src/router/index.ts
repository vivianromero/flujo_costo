import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import Login from '@/views/Login.vue'
import { useSessionStore } from '@/stores/session'

const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Inicio.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

// Protección por token y sesión
router.beforeEach((to, from, next) => {
  const session = useSessionStore()
  const token = session.token || localStorage.getItem('token')

  // Si no hay token y la ruta requiere autenticación
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})








