// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de productos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_PRODUCTOFLUJO = gql`
  query GetProductoFlujo($page: Int!, $limit: Int!, $codigo: String, $descripcion: String,
                         $medidaClave: String, $tipoProducto: String, $claseMateriaprima: String,
                         $activo: Boolean) {
    productoflujo(page: $page, limit: $limit, codigo: $codigo, descripcion: $descripcion,
                  medidaClave: $medidaClave, tipoProducto: $tipoProducto, claseMateriaprima: $claseMateriaprima,
                  activo: $activo) {
      items {
            id
            codigo
            descripcion
            medidaClave
            tipoProducto
            claseMateriaprima {
                descripcion
            }
            activo
      }
      totalCount
    }
  }
`

export function useProductoFlujo(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  descripcion?: Ref<string | null>
  medidaClave?: Ref<string | null>
  tipoProducto?: Ref<string | null>
  claseMateriaprima?: Ref<string | null>
  claseMateriaprima?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {

    const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.codigo?.value) vars.codigo = options.codigo.value
      if (options.descripcion?.value) vars.descripcion = options.descripcion.value
      if (options.medidaClave?.value) vars.medidaClave = options.medidaClave.value
      if (options.tipoProducto?.value) vars.tipoProducto = options.tipoProducto.value
      if (options.claseMateriaprima?.value) vars.claseMateriaprima = options.claseMateriaprima.value
      if (options.activo?.value) vars.activo = options.activo.value
      return vars
    })

  const smartPagination = useSmartPagination({
    query: GET_PRODUCTOFLUJO,
    variables,
    pagination: options.pagination,
    columns: options.columns
  })

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows
  }
}
