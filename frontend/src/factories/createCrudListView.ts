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

interface TableAction {
  name: string
  icon: string
  color: string
  tooltip: string
  visible?: boolean | ((row: any) => boolean)
  condition?: (row: any) => boolean
}

interface CrudOptions {
  rowsPerPageOptions?: number[]
  rowsPerPage?: number
  showActions?: boolean
  customActions?: TableAction[]
  onAction?: (action: string, row: any) => void

  noView?: boolean
  noEdit?: boolean
  noDelete?: boolean
}

export function createCrudListView(
  useComposable: any,
  columns: any[],
  options: CrudOptions = {}
) {
  return defineComponent({
    name: 'CrudListView',
    setup() {
      const {
        rowsPerPage = 15,
        showActions = true,
        customActions,
        onAction,
        noView = false,
        noEdit = false,
        noDelete = false
      } = options

      const pagination = ref({ page: 1, rowsPerPage: rowsPerPage })

      // 🔥 AGREGAR COLUMNA DE ACCIONES AUTOMÁTICAMENTE SI showActions ES TRUE
      const tableColumns = [...columns]
      if (showActions) {
        tableColumns.push({
          name: 'actions',
          label: 'Acciones',
          align: 'center',
          sortable: false,
          width: '120px'
        })
      }

      const { rows, loading, totalCount, refetch } = useComposable({
        pagination,
        columns: tableColumns
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

      console.log('Edit create:', noEdit)
      console.log('Delete create:', noDelete)

      // 🔥 ACCIONES POR DEFECTO FILTRADAS SEGÚN LAS FLAGS
      const defaultActions: TableAction[] = [
        {
          name: 'view',
          icon: 'fa-solid fa-eye',
          color: 'primary',
          tooltip: 'Ver detalles',
          visible: !noView // 🔥 MOSTRAR SI noView ES FALSE
        },
        {
          name: 'edit',
          icon: 'fa-solid fa-edit',
          color: 'secondary',
          tooltip: 'Editar',
          visible: !noEdit // 🔥 MOSTRAR SI noEdit ES FALSE
        },
        {
          name: 'delete',
          icon: 'fa-solid fa-trash',
          color: 'negative',
          tooltip: 'Eliminar',
          visible: !noDelete // 🔥 MOSTRAR SI noDelete ES FALSE
        }
      ]

      // 🔥 FILTRAR ACCIONES VISIBLES
      const getVisibleActions = () => {
        const actions = customActions || defaultActions
        return actions.filter(action => {
          if (typeof action.visible === 'function') {
            return action.visible({}) // Ejecutar función de visibilidad
          }
          return action.visible !== false // Mostrar si no es false explícitamente
        })
      }

      const actionsToUse = getVisibleActions()

      const handleAction = ({ action, row }: { action: string; row: any }) => {
        if (onAction) {
          onAction(action, row)
        } else {
          // 🔥 COMPORTAMIENTO POR DEFECTO
          switch (action) {
            case 'view':
              console.log('Ver:', row)
              break
            case 'edit':
              console.log('Editar:', row)
              break
            case 'delete':
              if (confirm(`¿Estás seguro de eliminar ${row.descripcion || row.nombre}?`)) {
                console.log('Eliminar:', row)
              }
              break
            default:
              console.log(`Acción ${action}:`, row)
          }
        }
      }

      return () =>
        h(InstitucionalTable, {
          columns: tableColumns,
          rows: rows.value,
          loading: loading.value,
          pagination: pagination.value,
          'onUpdate:pagination': (val: any) => (pagination.value = val),
          rowsNumber: totalCount.value,
          showRefresh: true,
          onRefresh: refrescar,
          rowsPerPageOptions,
          showActions,
          actions: actionsToUse,
          onAction: handleAction
        })
    },
  })
}


