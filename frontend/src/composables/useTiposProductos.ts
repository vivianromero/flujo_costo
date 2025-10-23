// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de productos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_TIPOSPRODUCTOS } from '@/graphql/queries/tiposproductos'

export function useTiposProductos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_TIPOSPRODUCTOS,
    pagination: options.pagination,
    filters: {
      descripcion: options.descripcion!
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}
