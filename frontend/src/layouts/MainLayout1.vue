<template>
  <div class="main-layout">
    <Header />
    <div class="layout-body">
      <Sidebar />
      <main class="content-area">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
    import '@/assets/css/main-layout.css'
    import Header from '@/components/Header.vue'
    import Sidebar from '@/components/Sidebar.vue'
    import { useSessionStore } from '@/stores/session'
    import { useQuery } from '@vue/apollo-composable'
    import gql from 'graphql-tag'

    const session = useSessionStore()

    const ME_QUERY = gql`
      query Me {
          me {
            username
            ueb {
              nombre
            }
          }
        }
    `

    const { result, onResult, onError } = useQuery(ME_QUERY, null, {
          fetchPolicy: 'network-only'
        })

        onResult(({ data }) => {
          console.log('Resultado de ME_QUERY:', data)
          if (data?.me) {
            session.setUserData({
              username: data.me.username,
              ueb: data.me.ueb?.nombre || '',
              role: data.me.role
            })
          }
        })

        onError((error) => {
          console.error('Error en ME_QUERY:', error.message)
        })

</script>





