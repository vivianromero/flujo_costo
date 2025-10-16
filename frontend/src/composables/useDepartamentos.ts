// src/composables/useDepartamentos.ts
import { ref } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from 'graphql-tag'

const GET_DEPARTAMENTOS = gql`
  query GetDepartamentos {
    departamentos {
      id
      codigo
      descripcion
      centrocosto {
        id
        clave
        descripcion
        activo
      }
    }
  }
`

export function useDepartamentos() {
  const rows = ref([])
  const loading = ref(true)

  const { result, refetch } = useQuery(GET_DEPARTAMENTOS, null, {
    fetchPolicy: 'network-only'
  })

  result.watch((data) => {
    rows.value = data?.departamentos ?? []
    loading.value = false
  })

  return {
    rows,
    loading,
    refetch
  }
}

