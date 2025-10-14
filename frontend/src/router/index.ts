import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import Login from '@/views/Login.vue'
import { useSessionStore } from '@/stores/session'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/unauthorized',
    name: 'unauthorized',
    component: () => import('@/views/UnauthorizedView.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'main',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Inicio.vue'),
        meta: { breadcrumb: 'Inicio', icon: 'fa-solid fa-home' }
      },
      {
        path: '/noaccess',
        name: 'noaccess',
        component: () => import('@/views/NoAccessView.vue'),
        meta: { public: true }
      },
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

// =========================================================
// ✅ Middleware de autenticación
// =========================================================
router.beforeEach((to, from, next) => {
  const session = useSessionStore()
  const token = session.token || localStorage.getItem('token')

  // 1️⃣ Si la ruta es pública, continuar sin restricciones
  if (to.meta.public) {
    next()
    return
  }

  // 2️⃣ Si requiere autenticación y no hay token, ir al login
  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
    return
  }

  // 3️⃣ Si ya hay token y se intenta ir al login, ir al home
  if (to.name === 'login' && token) {
    next({ name: 'home' })
    return
  }

  // 4️⃣ En cualquier otro caso, continuar
  next()
})

export default router





