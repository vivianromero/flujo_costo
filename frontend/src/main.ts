import { createApp, provide, h } from 'vue'
import App from './App.vue'
import { router } from './router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo/client'
import { createPinia } from 'pinia'

// Quasar core
import { Quasar } from 'quasar'
import quasarLang from 'quasar/lang/es'
import 'quasar/dist/quasar.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
import '@/assets/css/institucional.css'

// Componentes manuales si no usas auto-import
import {
  QLayout, QHeader, QDrawer, QPageContainer, QFooter,
  QToolbar, QToolbarTitle, QBtn, QAvatar, QIcon,
  QItem, QItemSection, QList, QCard, QCardSection,
  QBreadcrumbs, QBreadcrumbsEl
} from 'quasar'

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App)
})

app.use(createPinia())
app.use(router)
app.use(Quasar, {
  components: {
    QLayout, QHeader, QDrawer, QPageContainer, QFooter,
    QToolbar, QToolbarTitle, QBtn, QAvatar, QIcon,
    QItem, QItemSection, QList, QCard, QCardSection,
    QBreadcrumbs, QBreadcrumbsEl
  },
  lang: quasarLang
})

app.mount('#app')









