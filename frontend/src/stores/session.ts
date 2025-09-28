import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    username: '',
    token: '',
    ueb: '',
  }),
  actions: {
    setUsername(name: string) {
      this.username = name
    },
    setToken(token: string) {
      this.token = token
    },
    setUeb(ueb: string) {
      this.ueb = ueb
    },
    clearSession() {
      this.username = ''
      this.token = ''
      this.ueb = ''
    }
  }
})
