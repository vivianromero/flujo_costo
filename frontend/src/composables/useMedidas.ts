// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de unidades de medida no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_MEDIDAS } from '@/graphql/queries/unidadesmedida'

export function useMedidas(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  nombre?: Ref<string | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_MEDIDAS,
    pagination: options.pagination,
    filters: {
      codigo: options.codigo!,
      nombre: options.nombre!,
      activo: options.activo!
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}