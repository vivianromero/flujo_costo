// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de tipos de documentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { useGenericCompusable } from '@/composables/useGenericCompusable'
import { GET_TIPOSDOCUMENTOS } from '@/graphql/queries/tiposdocumentos'

export function useTiposDocumentos(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  descripcion?: Ref<string | null>
  operacion?: Ref<string | null>
  prefijo?: Ref<string | null>
  generado?: Ref<boolean | null>
  columns?: any[]
}) {
  return useGenericCompusable({
    query: GET_TIPOSDOCUMENTOS,
    pagination: options.pagination,
    filters: {
      descripcion: options.descripcion!,
      operacion: options.operacion!,
      prefijo: options.prefijo!,
      generado: options.generado!,
    },
    columns: options.columns,
    loadAll: options.loadAll
  })
}
