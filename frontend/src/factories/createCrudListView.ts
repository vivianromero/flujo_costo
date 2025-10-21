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

import { defineComponent, h, ref, watch, computed } from 'vue'
import InstitucionalTable from '@/components/InstitucionalTable.vue'


interface TopAction {
  name: string
  label: string
  icon: string
  color: string
  visible?: boolean | (() => boolean)
  condition?: () => boolean
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

  showTopActions?: boolean
  customTopActions?: TopAction[]
  onTopAction?: (action: string) => void

  noFetchFromSystem?: boolean
  noCreate?: boolean
  noExport?: boolean
  noImport?: boolean
  noExportExcel?: boolean
  tooltipFetchFromSystem?: string
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
        noDelete = false,
        showTopActions = true,
        customTopActions,
        onTopAction,
        noFetchFromSystem = false,
        noCreate = false,
        noExport = false,
        noImport = false,
        noExportExcel = false,
        tooltipFetchFromSystem = 'Actualizar desde otro sistema'
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

      // 🔥 ACCIONES POR DEFECTO FILTRADAS SEGÚN LAS FLAGS
      const defaultActions: TableAction[] = [
        {
          name: 'view',
          icon: 'fa-solid fa-eye',
          color: 'primary',
          tooltip: 'Ver detalles',
          visible: !noView
        },
        {
          name: 'edit',
          icon: 'fa-solid fa-edit',
          color: 'secondary',
          tooltip: 'Editar',
          visible: !noEdit
        },
        {
          name: 'delete',
          icon: 'fa-solid fa-trash',
          color: 'negative',
          tooltip: 'Eliminar',
          visible: !noDelete
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

      const defaultTopActions: TopAction[] = [

       {
         name: 'fetchFromSystem',
         icon: 'fa-solid fa-database',
         //color: 'primary',
         color: 'grey-8',
         tooltip: tooltipFetchFromSystem,
         visible: !noFetchFromSystem
       },
       {
         name: 'create',
         icon: 'fa-solid fa-file-circle-plus',
         //color: 'positive',
         color: 'grey-8',
         tooltip: 'Crear Nuevo Elemento',
         visible: !noCreate
       },
       {
         name: 'export',
         icon: 'fa-solid fa-file-export',
         //color: 'secondary',
         color: 'grey-8',
         tooltip: 'Exportar Datos',
         visible: !noExport
       },
       {
         name: 'import',
         icon: 'fa-solid fa-file-import',
         //color: 'info',
         color: 'grey-8',
         tooltip: 'Importar Datos',
         visible: !noImport
       },
       {
         name: 'exportexcel',
         icon: 'fa-solid fa-file-excel',
         color: 'grey-8',
         tooltip: 'Exportar a excel',
         visible: !noExportExcel
       }
     ]

      const topActionsToUse = customTopActions || defaultTopActions

      // 🔥 FILTRAR ACCIONES SUPERIORES VISIBLES
      const visibleTopActions = computed(() => {
        return topActionsToUse.filter(action => {
          if (typeof action.visible === 'function') {
            return action.visible()
          }
          return action.visible !== false
        })
      })

      const handleTopAction = (actionName: string) => {
        if (onTopAction) {
          onTopAction(actionName)
        } else {
          // 🔥 COMPORTAMIENTO POR DEFECTO
          switch (actionName) {
            case 'fetchFromSystem':
              console.log('Traer datos desde Sistema X')
              break
            case 'create':
              console.log('Crear nuevo elemento')
              break
            case 'export':
              console.log('Exportar datos')
              break
            case 'import':
              console.log('Importar datos')
              break
            default:
              console.log(`Acción superior ${actionName}`)
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
          onAction: handleAction,
          showTopActions,
          topActions: visibleTopActions.value,
          onTopAction: handleTopAction
        })
    },
  })
}


