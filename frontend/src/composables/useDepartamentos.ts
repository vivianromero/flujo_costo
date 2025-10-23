// 🔹 Este composable usa paginado local con limit 99999
// 🔹 Asume que la cantidad de departamentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente

// src/composables/useDepartamentos.ts
// src/composables/useDepartamentos.ts
import { computed, ref, watch } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from './useSmartPagination'
import { gql } from 'graphql-tag'

const GET_DEPARTAMENTOS = gql`
  query GetDepartamentos($page: Int!, $limit: Int!, $centroId: ID, $centroActivo: Boolean) {
    departamentos(page: $page, limit: $limit, centroId: $centroId, centroActivo: $centroActivo) {
      items {
        id
        codigo
        descripcion
        centrocosto {
          clave
          descripcion
        }
      }
      totalCount
    }
  }
`

export function useDepartamentos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  centroId?: Ref<string | null>
  centroActivo?: Ref<boolean | null>
  columns?: any[]
  loadAll?: boolean
}) {
  const loadAll = options.loadAll ?? false

  // 🔹 Variables reactivas para Apollo

  const variables = ref({
    page: 1,
    limit: 99999,
    centroId: options.centroId?.value ?? null,
    centroActivo: options.centroActivo?.value ?? null
  })

  if (!loadAll) {
    variables.value.page = options.pagination.value.page
    variables.value.limit = options.pagination.value.rowsPerPage

    watch(options.pagination, (newVal) => {
      variables.value.page = newVal.page
      variables.value.limit = newVal.rowsPerPage
    }, { deep: true })
  }



  // 🔹 Actualizar variables si cambian las dependencias
  if (options.centroId) {
    watch(options.centroId, (newVal) => {
      variables.value.centroId = newVal
    })
  }

  if (options.centroActivo) {
    watch(options.centroActivo, (newVal) => {
      variables.value.centroActivo = newVal
    })
  }

  // 🔹 Actualizar paginación si loadAll es false
  if (!loadAll) {
    watch(options.pagination, (newVal) => {
      variables.value.page = newVal.page
      variables.value.limit = newVal.rowsPerPage
    }, { deep: true })
  }

  const smartPagination = useSmartPagination({
    query: GET_DEPARTAMENTOS,
    variables,
    pagination: options.pagination,
    columns: options.columns,
    loadAll
  })

  smartPagination.refetch()

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows
  }
}

