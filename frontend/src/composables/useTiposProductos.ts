// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de productos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_TIPOSPRODUCTOS = gql`
  query GetTiposProductos($page: Int!, $limit: Int!, $descripcion: String) {
    tiposproductos(page: $page, limit: $limit, descripcion: $descripcion) {
      items {
        id
        descripcion
      }
      totalCount
    }
  }
`

export function useTiposProductos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  columns?: any[]
}) {
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    descripcion: options.descripcion?.value ?? null,
  }))

  const smartPagination = useSmartPagination({
    query: GET_TIPOSPRODUCTOS,
    variables,
    pagination: options.pagination,
    columns: options.columns
  })

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows // Para debug
  }
}
