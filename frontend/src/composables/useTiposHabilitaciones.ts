// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de g¡habilitaciones no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_TIPOSHABILITACIONES } from '@/graphql/queries/tiposhabilitaciones'

export function useTiposHabilitaciones(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_TIPOSHABILITACIONES,
    pagination: options.pagination,
    filters: {
      descripcion: options.descripcion!,
      activo: options.activo!
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}
