import { defineStore } from 'pinia'
import logoDatazucar from '@/assets/img/logo_datazucar.png'

interface Site {
  domain: string
  name: string
  icon?: logoDatazucar
}

export const useFooterStore = defineStore('footer', {
  state: () => ({
    site: { domain: 'miempresa.com', name: 'DATAZUCAR', icon: logoDatazucar } as Site,
    year: 2025,
    version: '1.0'
  }),
  actions: {
    setSite(site: Site) {
      this.site = site
    },
    setYear(year: number | string) {
      this.year = year
    },
    setVersion(version: string) {
      this.version = version
    }
  }
})
