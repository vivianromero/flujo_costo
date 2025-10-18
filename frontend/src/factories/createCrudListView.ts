/**
 * FACTORY PARA VISTAS CRUD REUTILIZABLES
 *
 * 🎯 PROPÓSITO:
 * Crea componentes de tabla CRUD automáticamente, eliminando código repetitivo.
 * Combina un composable de datos con columnas definidas para generar vistas listas para usar.
 *
 * 📦 ENTRADAS:
 * - useComposable: Hook que maneja datos y paginación
 * - columns: Definición de columnas para QTable
 * - options: Configuración opcional (paginación, etc.)
 *
 * 🚀 SALIDA:
 * - Componente Vue completo con tabla, paginación, ordenamiento y refresh
 *
 * 💡 USO:
 * const MiVista = createCrudListView(useMisDatos, columnas, opciones)
 * export default MiVista
 *
 * 🏗️ ARQUITECTURA:
 * Composable (datos) + Columnas (UI) = Vista CRUD Completa
 */

import { defineComponent, h, ref, watch } from 'vue'
import InstitucionalTable from '@/components/InstitucionalTable.vue'

export function createCrudListView(
  useComposable: any,
  columns: any[],
  options: {
    rowsPerPageOptions?: number[],
    rowsPerPage?: number
  } = {}
) {
  return defineComponent({
    name: 'CrudListView',
    setup() {
      const { rowsPerPage = 15 } = options
      const pagination = ref({ page: 1, rowsPerPage: rowsPerPage })

      // 🔥 PASAR LAS COLUMNS AL COMPOSABLE
      const { rows, loading, totalCount, refetch } = useComposable({
        pagination,
        columns // 🔥 ¡IMPORTANTE!
      })

      watch(totalCount, (newTotal) => {
        pagination.value.rowsNumber = newTotal
      })

      const refrescar = async () => {
        loading.value = true
        try {
          await refetch()
        } finally {
          loading.value = false
        }
      }

      const { rowsPerPageOptions = [5, 15, 25, 30, 50] } = options

      return () =>
        h(InstitucionalTable, {
          columns,
          rows: rows.value,
          loading: loading.value,
          pagination: pagination.value,
          'onUpdate:pagination': (val: any) => (pagination.value = val),
          rowsNumber: totalCount.value,
          showRefresh: true,
          onRefresh: refrescar,
          rowsPerPageOptions,
        })
    },
  })
}


