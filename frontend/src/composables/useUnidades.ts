// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de unidades contables no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_UNIDADES = gql`
  query GetUnidades($page: Int!, $limit: Int!, $codigo: String, $nombre: String, $activo: Boolean) {
    unidades(page: $page, limit: $limit, codigo: $codigo, nombre: $nombre, activo: $activo) {
      items {
        id
        codigo
        nombre
        isComercializadoraDisplay
        isEmpresaDisplay
        activoDisplay
      }
      totalCount
    }
  }
`

export function useUnidades(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  nombre?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    codigo: options.codigo?.value ?? null,
    nombre: options.nombre?.value ?? null,
    activo: options.activo?.value ?? null
  }))

  const smartPagination = useSmartPagination({
    query: GET_UNIDADES,
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
