// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de unidades de medida no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_MEDIDAS = gql`
  query GetMedidas($page: Int!, $limit: Int!, $clave: String, $descripcion: String, $activa: Boolean) {
    medidas(page: $page, limit: $limit, clave: $clave, descripcion: $descripcion, activa: $activa) {
      items {
        id
        clave
        descripcion
        activa
      }
      totalCount
    }
  }
`

export function useMedidas(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  nombre?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    clave: options.clave?.value ?? null,
    descripcion: options.descripcion?.value ?? null,
    activa: options.activa?.value ?? null
  }))

  const smartPagination = useSmartPagination({
    query: GET_MEDIDAS,
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