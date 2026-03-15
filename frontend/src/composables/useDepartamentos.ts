// 🔹 Este composable usa paginado local con limit 99999
// 🔹 Asume que la cantidad de departamentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente

// src/composables/useDepartamentos.ts
import { computed } from 'vue'
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
  columns?: any[] // 🔥 Opcional: pasar columns para ordenamiento con funciones
}) {

    const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.centroId?.value) vars.centroId = options.centroId.value
      if (options.centroActivo?.value) vars.centroActivo = options.centroActivo.value
      return vars
    })

  const smartPagination = useSmartPagination({
    query: GET_DEPARTAMENTOS,
    variables,
    pagination: options.pagination,
    columns: options.columns // 🔥 Pasar las columns para ordenamiento inteligente
  })

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows // Para debug
  }
}