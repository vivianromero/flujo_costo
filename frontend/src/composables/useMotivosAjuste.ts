// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de motivos de ajuste no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_MOTIVOSAJUSTE } from '@/graphql/queries/motivosajuste'

export function useMotivosAjuste(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  aumento?: Ref<boolean | null>
  activo?: Ref<boolean | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_MOTIVOSAJUSTE,
    pagination: options.pagination,
    filters: {
      descripcion: options.descripcion!,
      aumento: options.aumento!,
      activo: options.activo!,
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}
