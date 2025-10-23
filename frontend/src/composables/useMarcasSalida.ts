// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de marcas no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_MARCASSALIDA } from '@/graphql/queries/marcassalida'


export function useMarcasSalida(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  codigo?: Ref<string | null>
  descripcion?: Ref<string | null>
  activa?: Ref<boolean | null>
  columns?: any[]
}) {
return useGenericCompusable({
    query: GET_MARCASSALIDA,
    pagination: options.pagination,
    filters: {
      codigo: options.codigo!,
      descripcion: options.descripcion!,
      activa: options.activa!
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}
