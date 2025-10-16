import { ref, computed, watch } from 'vue'
import type { Ref } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from 'graphql-tag'

const GET_DEPARTAMENTOS = gql`
  query GetDepartamentos($page: Int!, $limit: Int!, $centroId: ID, $activos: Boolean) {
    departamentos(page: $page, limit: $limit, centroId: $centroId, activos: $activos) {
      items {
        id
        codigo
        descripcion
        centrocosto {
          descripcion
        }
      }
      totalCount
    }
  }
`

export function useDepartamentosPaginado(options: {
  pagination: Ref<{ page: number; rowsPerPage: number }>
  centroId?: Ref<string | null>
  activos?: Ref<boolean | null>
}) {
  const rows = ref<any[]>([])
  const loading = ref(true)
  const totalCount = ref(0)

  // 🔹 Variables reactivas
  const variables = computed(() => ({
    page: options.pagination.value.page,
    limit: options.pagination.value.rowsPerPage,
    centroId: options.centroId?.value ?? null,
    activos: options.activos?.value ?? null
  }))

  // 🔹 Verificación
  watch(variables, (val) => {
    console.log('🔹 VARIABLES USADAS EN QUERY', val)
  })

  const { result, refetch } = useQuery(GET_DEPARTAMENTOS, variables, {
    fetchPolicy: 'network-only'
  })

  // 🔹 Refetch cuando cambie la paginación
  watch(
    () => ({ ...options.pagination.value }),
    async (newVal, oldVal) => {
      console.log('🔁 Paginación cambió:', newVal)
      await refetch(variables.value)
    },
    { deep: true }
  )

  // 🔹 Actualizar resultados
  watch(result, (data) => {
    rows.value = data?.departamentos?.items ?? []
    totalCount.value = data?.departamentos?.totalCount ?? 0
    loading.value = false
  })

  return {
    rows,
    loading,
    totalCount,
    refetch
  }
}




