// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de unidades contables no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_UNIDADES } from '@/graphql/queries/unidadescontables'

export function useUnidades(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  nombre?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  return useGenericCompusable ({
    query: GET_UNIDADES,
    pagination: options.pagination,
    columns: options.columns,
    loadAll: options.loadAll
  })
}
