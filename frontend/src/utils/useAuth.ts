import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'
import { apolloClient } from '@/apollo/client'

export function useAuth() {
  const router = useRouter()
  const session = useSessionStore()

  function login(token: string, username: string, ueb: string, isAdmin: boolean,
                 isAdminempresa: boolean, isOperflujo: boolean, isOpercosto: boolean) {

    sessionStorage.setItem('token', token)
    sessionStorage.setItem('username', username)
    sessionStorage.setItem('ueb', ueb)
    sessionStorage.setItem('isAdmin', isAdmin)
    sessionStorage.setItem('isAdminempresa', isAdminempresa)
    sessionStorage.setItem('isOperflujo', isOperflujo)
    sessionStorage.setItem('isOpercosto', isOpercosto)

    session.setToken(token)
    session.setUsername(username)
    session.setUeb(ueb)
    session.setIsAdmin(isAdmin)
    session.setIsAdminempresa(isAdminempresa)
    session.setIsOperflujo(isOperflujo)
    session.setIsOpercosto(isOpercosto)
  }

  function restoreSession() {
    const token = sessionStorage.getItem('token')
    const username = sessionStorage.getItem('username')
    const ueb = sessionStorage.getItem('ueb')
    const isAdmin = sessionStorage.getItem(isAdmin)
    const isAdminempresa = sessionStorage.getItem(isAdminempresa)
    const isOperflujo = sessionStorage.getItem(isOperflujo)
    const isOpercosto = sessionStorage.getItem(isOpercosto)


    if (token) {
      session.setToken(token)
      if (username) session.setUsername(username)
      if (ueb) session.setUeb(ueb)
    } else {
      router.push('/login')
    }
  }

  function logout() {
    if (apolloClient) {
      apolloClient.clearStore()
    }
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
    isAuthenticated,
    user: () => session.user,
    isAdmin: () => session.isAdmin,
    isAdminempresa: () => session.isAdminempresa,
    isOperflujo: () => session.isOperflujo,
    isOpercosto: () => session.isOpercosto,
  }
}
