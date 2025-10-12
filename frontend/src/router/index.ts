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
    name: 'main', // 👈 necesario para router.addRoute('main', ...)
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Inicio.vue'),
        meta: { breadcrumb: 'Inicio' }
      }
    ]
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const session = useSessionStore()
  const token = session.token || localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) next('/login')
  else next()
})







