// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de marcas no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_MARCASSALIDA = gql`
  query GetMarcasSalida($page: Int!, $limit: Int!, $codigo: String, $descripcion: String, $activa: Boolean) {
    marcassalida(page: $page, limit: $limit, codigo: $codigo, descripcion: $descripcion, activa: $activa) {
      items {
        id
        codigo
        descripcion
        activa
      }
      totalCount
    }
  }
`

export function useMarcasSalida(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  descripcion?: Ref<string | null>
  activa?: Ref<boolean | null>
  columns?: any[]
}) {
   const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.codigo?.value) vars.codigo = options.codigo.value
      if (options.descripcion?.value) vars.descripcion = options.descripcion.value
      if (options.activa?.value) vars.activa = options.activa.value
      return vars
    })

  const smartPagination = useSmartPagination({
    query: GET_MARCASSALIDA,
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
