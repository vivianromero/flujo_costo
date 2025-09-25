import { createApp, provide, h } from 'vue'
import App from './App.vue'
import { router } from './router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo/client'
import { createPinia } from 'pinia'
import { Quasar } from 'quasar'
import quasarLang from 'quasar/lang/es'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
import 'quasar/dist/quasar.css'
import '@/assets/css/institucional.css'

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App)
})

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  plugins: {}, // agregar plugins como Notify, Dialog, etc.
  lang: quasarLang
})
app.mount('#app')







