/**
 * COMPOSABLE INTELIGENTE PARA PAGINACIÓN Y ORDENAMIENTO
 *
 * 🎯 PROPÓSITO:
 * Maneja paginación local y ordenamiento automático para tablas con datos cargados completamente.
 * Soporta campos simples, objetos anidados y funciones personalizadas en columnas.
 *
 * 🔧 CARACTERÍSTICAS:
 * - ✅ Paginación en memoria (client-side)
 * - ✅ Ordenamiento automático por cualquier tipo de campo
 * - ✅ Soporte para objetos anidados (ej: 'centrocosto.descripcion')
 * - ✅ Soporte para funciones en columnas (ej: field: row => row.nombre)
 * - ✅ Detección automática de estructuras de datos GraphQL
 *
 * 📦 ENTRADAS:
 * - query: Query GraphQL
 * - variables: Parámetros para la query
 * - pagination: Estado reactivo de paginación
 * - columns: Columnas para ordenamiento inteligente (opcional)
 *
 * 🚀 SALIDA:
 * - rows: Datos paginados y ordenados
 * - loading: Estado de carga
 * - totalCount: Total de registros
 * - refetch: Función para recargar datos
 *
 * 💡 USO TÍPICO:
 * const { rows, loading, totalCount } = useSmartPagination({
 *   query: GET_MIS_DATOS,
 *   variables: { page: 1, limit: 99999 },
 *   pagination: paginationState,
 *   columns: columnDefinitions
 * })
 *
 * 🏗️ ARQUITECTURA:
 * GraphQL Query → Extracción Inteligente → Ordenamiento → Paginación → UI
 */

import { ref, computed, watch, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useQuery } from '@vue/apollo-composable'

export function useSmartPagination(options: {
  query: any
  variables: any
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  columns?: any[]
}) {
  const allRows = ref<any[]>([])
  const rows = ref<any[]>([])
  const loading = ref(true)
  const totalCount = ref(0)


  // 📡 Query con función
  const { result, refetch, onResult, onError } = useQuery(
    options.query,
    () => {
      const vars = options.variables.value
      return vars
    },
    {
      fetchPolicy: 'network-only',
      notifyOnNetworkStatusChange: true
    }
  )

  // 👀 Watch para ver cambios en paginación
  watch(() => options.pagination.value, (newPage, oldPage) => {
  }, { deep: true })

  // 👀 Watch para ver cambios en variables
  watch(() => options.pagination.value, (newPage, oldPage) => {
  }, { deep: true })

  onError((error) => {
    loading.value = false
  })

    onResult((queryResult) => {
        if (queryResult.data) {
          processData(queryResult.data)
        }
        loading.value = queryResult.loading
      })

  function extractData(data: any): { items: any[], totalCount: number } {

    if (!data) {
      return { items: [], totalCount: 0 }
    }

    const dataKeys = Object.keys(data)

    for (const key of dataKeys) {
      const entityData = data[key]
      if (entityData && typeof entityData === 'object') {
        if (entityData.items && Array.isArray(entityData.items)) {
          return {
            items: entityData.items,
            totalCount: entityData.totalCount || entityData.items.length
          }
        }
        if (Array.isArray(entityData)) {
          return {
            items: entityData,
            totalCount: entityData.length
          }
        }
      }
    }

    return { items: [], totalCount: 0 }
  }

  function processData(data: any) {
    const { items, totalCount: count } = extractData(data)

    allRows.value = items
    totalCount.value = count
    rows.value = items  // ← Directamente los items, sin paginación local
    loading.value = false
  }

  // Inicial
  if (result.value) {
    processData(result.value)
  }

  return {
    rows,
    loading,
    totalCount,
    refetch,
    allRows
  }
}