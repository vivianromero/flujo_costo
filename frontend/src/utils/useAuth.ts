import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'

export function useAuth() {
  const router = useRouter()
  const session = useSessionStore()

  function login(token: string, username: string, ueb: string) {
    sessionStorage.setItem('token', token)
    sessionStorage.setItem('username', username)
    sessionStorage.setItem('ueb', ueb)

    session.setToken(token)
    session.setUsername(username)
    session.setUeb(ueb)
  }

  function restoreSession() {
    const token = sessionStorage.getItem('token')
    const username = sessionStorage.getItem('username')
    const ueb = sessionStorage.getItem('ueb')

    if (token) {
      session.setToken(token)
      if (username) session.setUsername(username)
      if (ueb) session.setUeb(ueb)
    } else {
      router.push('/login')
    }
  }

  function logout() {
    sessionStorage.clear()
    session.clearSession()
    router.push('/login')
  }

  function isAuthenticated(): boolean {
    return !!sessionStorage.getItem('token')
  }

  return {
    login,
    restoreSession,
    logout,
    isAuthenticated
  }
}
