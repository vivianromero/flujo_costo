// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de g¡habilitaciones no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_TIPOSHABILITACIONES = gql`
  query GetTiposHabilitaciones($page: Int!, $limit: Int!, $descripcion: String, $activo: Boolean) {
    tiposhabilitaciones(page: $page, limit: $limit, descripcion: $descripcion, activo: $activo) {
      items {
        id
        descripcion
        activo
      }
      totalCount
    }
  }
`

export function useTiposHabilitaciones(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    descripcion: options.descripcion?.value ?? null,
    activo: options.activo?.value ?? null,
  }))

  const smartPagination = useSmartPagination({
    query: GET_TIPOSHABILITACIONES,
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
