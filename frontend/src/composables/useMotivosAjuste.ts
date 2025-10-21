// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de motivos de ajuste no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_MOTIVOSAJUSTE = gql`
  query GetMotivosAjuste($page: Int!, $limit: Int!, $descripcion: String, $activo: Boolean, $aumento: Boolean) {
    motivosajuste(page: $page, limit: $limit, descripcion: $descripcion, activo: $activo, aumento: $aumento) {
      items {
        id
        descripcion
        aumento
        activo
      }
      totalCount
    }
  }
`

export function useMotivosAjuste(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  aumento?: Ref<boolean | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    descripcion: options.descripcion?.value ?? null,
    aumento: options.amento?.value ?? null,
    activo: options.activo?.value ?? null,
  }))

  const smartPagination = useSmartPagination({
    query: GET_MOTIVOSAJUSTE,
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
