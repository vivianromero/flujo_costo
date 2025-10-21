import { createApp, provide, h } from 'vue'
import App from './App.vue'
import { router } from './router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo/client'
import { createPinia } from 'pinia'
import { restoreDynamicRoutes } from './router/dynamicRoutes'
import { useMenuStore } from '@/stores/menu'
import { useSessionGuard } from '@/utils/useSessionGuard'

// Quasar core - IMPORTAR CORRECTAMENTE
import { Quasar } from 'quasar'
import quasarLang from 'quasar/lang/es'

// Importar estilos CORRECTOS
import 'quasar/dist/quasar.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
import '@/assets/css/institucional.css'
import iconSet from 'quasar/icon-set/fontawesome-v6'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

const menuStore = useMenuStore()
restoreDynamicRoutes(router, menuStore)

await useSessionGuard(router)
app.provide(DefaultApolloClient, apolloClient)

app.use(router)

// Configuración Quasar
app.use(Quasar, {
  plugins: {},
  lang: quasarLang,
  iconSet
})


app.mount('#app')















