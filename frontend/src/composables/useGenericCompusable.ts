// useGenericCompusable.ts
import { ref, watch } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from './useSmartPagination'

interface GenericCompusableOptions {
  query: any
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  filters?: Record<string, Ref<any>> // 🔹 Para centroId, centroActivo, etc.
  columns?: any[]
  loadAll?: boolean
}

export function useGenericCompusable(options: GenericCompusableOptions) {
  const loadAll = options.loadAll ?? false

  // 🔹 Variables reactivas para Apollo
  const variables = ref({
    page: 1,
    limit: 99999
  })

  // 🔹 Aplicar filtros dinámicos
  if (options.filters) {
    for (const [key, refValue] of Object.entries(options.filters)) {
      variables.value[key] = refValue ? refValue.value : null
      watch(refValue, (newVal) => {
        variables.value[key] = newVal
      })
    }
  }

  // 🔹 Actualizar paginación si no es carga total
  if (!loadAll) {
    variables.value.page = options.pagination.value.page
    variables.value.limit = options.pagination.value.rowsPerPage

    watch(options.pagination, (newVal) => {
      variables.value.page = newVal.page
      variables.value.limit = newVal.rowsPerPage
    }, { deep: true })
  }

  const smartPagination = useSmartPagination({
    query: options.query,
    variables,
    pagination: options.pagination,
    columns: options.columns,
    loadAll
  })

  smartPagination.refetch()

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows
  }
}
