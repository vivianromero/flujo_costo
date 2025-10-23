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
  loadAll?: boolean
}) {
  const allRows = ref<any[]>([])
  const rows = ref<any[]>([])
  const loading = ref(true)
  const totalCount = ref(0)

  const { result, refetch, onResult, onError } = useQuery(options.query, options.variables, {
    fetchPolicy: 'cache-first'
  })

  // 🔥 MANEJO DE ERRORES
  onError((error) => {
    console.error('❌ Error en query GraphQL:', error)
    loading.value = false
  })

  // 🔥 FUNCIÓN MEJORADA PARA EXTRAER DATOS
  function extractData(data: any): { items: any[], totalCount: number } {
    if (!data) return { items: [], totalCount: 0 }

    // Buscar en diferentes estructuras comunes
    const dataKeys = Object.keys(data)

    for (const key of dataKeys) {
      const entityData = data[key]

      // Si tiene estructura { items: [], totalCount: number }
      if (entityData && typeof entityData === 'object') {
        if (Array.isArray(entityData.items) && typeof entityData.totalCount === 'number') {
          return {
            items: entityData.items,
            totalCount: entityData.totalCount
          }
        }

        // Si es un array directo
        if (Array.isArray(entityData)) {
          return {
            items: entityData,
            totalCount: entityData.length
          }
        }
      }
    }

    console.warn('⚠️ No se pudo extraer estructura de datos conocida:', data)
    return { items: [], totalCount: 0 }
  }

  // 🔥 FUNCIÓN DE ORDENAMIENTO INTELIGENTE (igual que antes)
  function getSortValue(item: any, field: string): any {
    if (!field) return ''

    if (options.columns) {
      const column = options.columns.find(col => col.name === field)
      if (column && typeof column.field === 'function') {
        return column.field(item)
      }
    }

    const directValue = item[field]

    if (directValue && typeof directValue === 'object') {
      const displayProperties = ['descripcion', 'nombre', 'name', 'title', 'label', 'text', 'codigo', 'clave']

      for (const prop of displayProperties) {
        if (directValue[prop] !== undefined && directValue[prop] !== null && directValue[prop] !== '') {
          return directValue[prop]
        }
      }

      for (const key in directValue) {
        const value = directValue[key]
        if (typeof value === 'string' && value.trim() !== '') {
          return value
        }
      }

      return ''
    }

    if (field.includes('.')) {
      return field.split('.').reduce((acc, key) => acc?.[key], item) || ''
    }

    return directValue || ''
  }

  // 🔥 PAGINACIÓN CON ORDENAMIENTO
  function paginate() {
    const { page, rowsPerPage, sortBy, descending } = options.pagination.value

    let list = allRows.value.slice()

    if (sortBy) {
      list.sort((a: any, b: any) => {
        const aVal = getSortValue(a, sortBy)
        const bVal = getSortValue(b, sortBy)

        if (aVal === '' || aVal == null) return descending ? -1 : 1
        if (bVal === '' || bVal == null) return descending ? 1 : -1

        if (typeof aVal === 'string' && typeof bVal === 'string') {
          const res = aVal.localeCompare(bVal, undefined, { sensitivity: 'base' })
          return descending ? -res : res
        }

        const res = aVal > bVal ? 1 : aVal < bVal ? -1 : 0
        return descending ? -res : res
      })
    }

    const start = (page - 1) * rowsPerPage
    const end = start + rowsPerPage
    rows.value = list.slice(start, end)
  }

  // 🔥 MANEJO DE DATOS MEJORADO
  function processData(data: any) {
  const { items, totalCount: count } = extractData(data)

  allRows.value = items
  totalCount.value = count
  loading.value = false

  if (options.loadAll) {
    // 🔹 Si se cargan todos, paginar localmente
    paginate()
  } else {
    // 🔹 Si no, usar solo los datos de la página actual
    const { page, rowsPerPage } = options.pagination.value
    rows.value = items
    totalCount.value = count
  }
}


  // 📥 WATCHERS Y MOUNTED
  onMounted(() => {
    if (result.value) {
      processData(result.value)
    } else {
      console.log('⏳ Esperando datos iniciales...')
    }
  })

  // Usar onResult para mejor control
  onResult((queryResult) => {

    if (queryResult.data) {
      processData(queryResult.data)
    }

    loading.value = queryResult.loading
  })

  watch(() => options.pagination.value, () => {
    paginate()
  }, { deep: true })

  return {
    rows,
    loading,
    totalCount,
    refetch,
    allRows
  }
}