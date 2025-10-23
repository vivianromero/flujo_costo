// 🔹 Este composable usa paginado local con limit 99999
// 🔹 Asume que la cantidad de departamentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente

// src/composables/useDepartamentos.ts
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_DEPARTAMENTOS } from '@/graphql/queries/departamentos'

export function useDepartamentos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  centroId?: Ref<string | null>
  centroActivo?: Ref<boolean | null>
  columns?: any[]
  loadAll?: boolean
}) {
  return useGenericCompusable({
    query: GET_DEPARTAMENTOS,
    pagination: options.pagination,
    filters: {
      centroId: options.centroId!,
      centroActivo: options.centroActivo!
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}


