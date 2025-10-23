// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de conversion de medida no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_MEDIDASCONVERSION } from '@/graphql/queries/medidasconversion'


export function useMedidasConversion(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  factorConversion?: Ref<string | null>
  medidao?: Ref<string | null>
  medidad?: Ref<string | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_MEDIDASCONVERSION,
    pagination: options.pagination,
    filters: {
      medidao: options.medidao!,
      medidad: options.medidad!,
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}