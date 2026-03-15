// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de documentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_TIPOSDOCUMENTOS = gql`
  query GetTiposDocumentos($page: Int!, $limit: Int!, $descripcion: String, $operacion: String, $prefijo: String, $generado: Boolean) {
    tiposdocumentos(page: $page, limit: $limit, descripcion: $descripcion, operacion: $operacion, prefijo: $prefijo, generado: $generado) {
      items {
        id
        descripcion
        operacion
        prefijo
        generado
      }
      totalCount
    }
  }
`

export function useTiposDocumentos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  operacion?: Ref<string | null>
  prefijo?: Ref<string | null>
  generado?: Ref<boolean | null>
  columns?: any[]
}) {
     const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.descripcion?.value) vars.descripcion = options.descripcion.value
      if (options.operacion?.value) vars.operacion = options.operacion.value
      if (options.prefijo?.value) vars.prefijo = options.prefijo.value
      if (options.generado?.value) vars.generado = options.generado.value
      return vars
    })
  const smartPagination = useSmartPagination({
    query: GET_TIPOSDOCUMENTOS,
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
