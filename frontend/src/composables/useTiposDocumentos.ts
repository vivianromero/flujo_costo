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
  const variables = computed(() => ({
    page: 1,
    limit: 99999,
    descripcion: options.descripcion?.value ?? null,
    operacion: options.operacion?.value ?? null,
    prefijo: options.prefijo?.value ?? null,
    generado: options.generado?.value ?? null
  }))

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
