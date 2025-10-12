import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    username: sessionStorage.getItem('username') || null,
    ueb: sessionStorage.getItem('ueb') || null
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
    clearSession() {
      this.token = null
      this.user = null
      this.username = null
      this.ueb = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      sessionStorage.clear()
    }
  }
})


