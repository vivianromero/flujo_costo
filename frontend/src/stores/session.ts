import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: '',
    ueb: '',
    role: ''
  }),
  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    setUserData({ username, ueb, role }: { username: string; ueb: string; role?: string }) {
      this.username = username
      this.ueb = ueb
      this.role = role || ''
    },
    clearSession() {
      this.token = ''
      this.username = ''
      this.ueb = ''
      this.role = ''
      localStorage.clear()
    }
  }
})


