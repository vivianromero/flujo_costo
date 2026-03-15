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
        isComercializadora
        isEmpresa
        activo
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

    const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.codigo?.value) vars.codigo = options.codigo.value
      if (options.nombre?.value) vars.nombre = options.nombre.value
      if (options.activo?.value) vars.activo = options.activo.value
      return vars
    })

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
