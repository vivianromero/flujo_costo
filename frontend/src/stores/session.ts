import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    username: sessionStorage.getItem('username') || null,
    ueb: sessionStorage.getItem('ueb') || null,
    isAdmin: sessionStorage.getItem('isAdmin') === 'true',
    isAdminempresa: sessionStorage.getItem('isAdminempresa') === 'true',
    isOperflujo: sessionStorage.getItem('isOperflujo') === 'true',
    isOpercosto: sessionStorage.getItem('isOpercosto') === 'true'

  }),

  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    setUsername(username) {
      this.username = username
      sessionStorage.setItem('username', username)
    },
    setUeb(ueb) {
      this.ueb = ueb
      sessionStorage.setItem('ueb', ueb)
    },
    setIsAdmin(isAdmin: boolean) {
      this.isAdmin = isAdmin
      sessionStorage.setItem('isAdmin', isAdmin.toString())
    },
    setIsAdminempresa(isAdminempresa: boolean) {
      this.isAdminempresa = isAdminempresa
      sessionStorage.setItem('isAdminempresa', isAdminempresa.toString())
    },
    setIsOperflujo(isOperflujo: boolean) {
      this.isOperflujo = isOperflujo
      sessionStorage.setItem('isOperflujo', isOperflujo.toString())
    },

    setIsOpercosto(isOpercosto: boolean) {
      this.isOpercosto = isOpercosto
      sessionStorage.setItem('isOpercosto', isOpercosto.toString())
    },
    setUserData(userData: any) {
      if (userData.username) this.setUsername(userData.username)
      if (userData.ueb) this.setUeb(userData.ueb)
      if (userData.isAdmin) this.setIsAdmin(userData.isAdmin)
      if (userData.isAdminempresa) this.setIsAdminempresa(userData.isAdminempresa)
      if (userData.isOperflujo) this.setIsOperflujo(userData.isOperflujo)
      if (userData.isOpercosto) this.setIsOpercosto(userData.isOpercosto)

      // También guardar el objeto completo en localStorage
      this.user = userData
      localStorage.setItem('user', JSON.stringify(userData))
    },
    clearSession() {
      this.token = null
      this.user = null
      this.username = null
      this.ueb = null
      this.isAdmin = false
      this.isAdminempresa = false
      this.isOperflujo = false
      this.isOpercosto = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      sessionStorage.clear()
    }
  }
})


