<template>
  <div class="institucional-table q-pa-md">
    <div v-if="showTopActions && topActions.length > 0" class="top-actions-container row justify-end items-center q-mb-md">
      <div class="top-actions row justify-end">
        <q-btn
          v-for="action in topActions"
          :key="action.name"
          :icon="action.icon"
          :color="action.color"
          @click="$emit('topAction', action.name)"
          flat
          dense
          round
          size="sm"
          class="top-action-btn"
        >
          <q-tooltip anchor="top middle" self="bottom middle">
            {{ action.tooltip }}
          </q-tooltip>
        </q-btn>
      </div>
    </div>
    <q-table
      flat
      bordered
      dense
      virtual-scroll
      :virtual-scroll-sticky-size-start="60"
      :rows="rows"
      :columns="processedColumns"
      :row-key="rowKey"
      :loading="loading"
      :rows-per-page-options="rowsPerPageOptions"
      :dropdown-icon="dropdownIcon"
      hide-bottom-if-empty
      class="my-sticky-virtscroll-table"
      :pagination="props.pagination"
      @update:pagination="val => emit('update:pagination', val)"
      @request="onRequest"
      :rows-number="props.rowsNumber"
    >
      <!-- 🔹 Encabezados personalizados CON REDIMENSIONADO -->
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
            class="institucional-table__header resizable-column"
            :style="getColumnStyle(col.name)"
            @mousedown="startResize(col.name, $event)"
          >
            {{ col.label }}
            <div
              class="column-resize-handle"
              @mousedown.stop="startResize(col.name, $event)"
            ></div>
          </q-th>
        </q-tr>
      </template>

      <!-- 🔹 Cuerpo de la tabla con acciones -->
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            <!-- 🔥 COLUMNA DE ACCIONES -->
            <template v-if="col.name === 'actions' && showActions">
              <div class="actions-container">
                <!-- Slot para acciones personalizadas -->
                <slot
                  name="actions"
                  :row="props.row"
                  :actions="getRowActions(props.row)"
                >
                  <!-- Acciones por defecto -->
                  <template v-for="action in getRowActions(props.row)" :key="action.name">
                    <q-btn
                      v-if="isActionVisible(action, props.row)"
                      flat
                      dense
                      round
                      size="xs"
                      :icon="action.icon"
                      :color="action.color"
                      @click="emitAction(action.name, props.row)"
                      class="action-btn"
                    >
                      <q-tooltip>{{ action.tooltip }}</q-tooltip>
                    </q-btn>
                  </template>
                </slot>
              </div>
            </template>

            <!-- 🔥 COLUMNAS NORMALES -->
            <template v-else>
              {{ col.value }}
            </template>
          </q-td>
        </q-tr>
      </template>

      <!-- 🔹 Slot bottom con padding reducido -->
      <template v-slot:bottom>
        <div class="row full-width items-center justify-between" style="padding: 0px 5px 0px 5px;">
          <!-- 🔄 Botón de refresh a la izquierda -->
          <div class="col-auto" style="background-color:blue;">
            <q-btn
              v-if="props.showRefresh"
              flat
              dense
              round
              size="xs"
              icon="fa-solid fa-rotate"
              color="white"
              @click="emit('refresh')"
              class="refresh-btn"
            >
              <span></span> <!-- 🔹 Ancla para el tooltip -->
              <q-tooltip anchor="top middle" self="bottom middle">
                {{ props.refreshTooltip || 'Actualizar Datos' }}
              </q-tooltip>
            </q-btn>

          </div>

          <!-- 📄 Controles de paginación a la derecha -->
          <div class="col-auto">
            <div class="row items-center no-wrap q-gutter-sm">
              <!-- Selector de filas por página -->
              <div class="row items-center no-wrap q-gutter-xs">
                <span class="text-caption text-grey-7">Filas por página:</span>
                <q-select
                  dense
                  borderless
                  :model-value="props.pagination.rowsPerPage"
                  @update:model-value="onRowsPerPageChange"
                  :options="rowsPerPageOptions"
                  style="min-width: 35px; padding-right:10px;"
                  emit-value
                  map-options
                  dropdown-icon="fas fa-caret-down"
                  class="custom-select"
                />
              </div>

              <!-- Información de paginación -->
              <div class="text-caption text-grey-7">
                {{ paginationInfo }}
              </div>

              <!-- Botones de navegación -->
              <q-btn
                flat dense round
                icon="fas fa-backward-step"
                :disable="props.pagination.page === 1"
                @click="goToPage(1)"
                size="sm"
              />
              <q-btn
                flat dense round
                icon="fa-solid fa-chevron-left"
                :disable="props.pagination.page === 1"
                @click="goToPage(props.pagination.page - 1)"
                size="sm"
              />

              <!-- Página actual -->
              <span class="text-caption text-weight-medium">
                {{ props.pagination.page }}
              </span>

              <q-btn
                flat dense round
                icon="fa-solid fa-chevron-right"
                :disable="isLastPage"
                @click="goToPage(props.pagination.page + 1)"
                size="sm"
              />
              <q-btn
                flat dense round
                icon="fas fa-forward-step"
                :disable="isLastPage"
                @click="goToPage(lastPage)"
                size="sm"
              />
            </div>
          </div>
        </div>
      </template>

      <!-- Slot de loading -->
      <template v-slot:loading>
        <q-inner-loading showing color="primary" />
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import type { QTableColumn } from 'quasar'

// 🔥 INTERFACE PARA ACCIONES
interface TableAction {
  name: string
  icon: string
  color: string
  tooltip: string
  visible?: boolean | ((row: any) => boolean)
  condition?: (row: any) => boolean
}

const props = defineProps<{
  columns: QTableColumn[]
  rows: any[]
  pagination: {
    page: number
    rowsPerPage: number
  }
  rowsNumber: number
  loading?: boolean
  rowKey?: string
  dropdownIcon?: string
  rowsPerPageOptions?: number[]
  refreshTooltip?: string
  showRefresh?: boolean
  // 🔥 NUEVAS PROPS PARA ACCIONES
  showActions?: boolean
  actions?: TableAction[]
  showTopActions?: boolean
  topActions?: any[]
}>()

const emit = defineEmits([
  'update:pagination',
  'refresh',
  'action',
  'topAction'
])

const rowKey = props.rowKey ?? 'id'
const dropdownIcon = props.dropdownIcon ?? 'fa fa-chevron-down'
const rowsPerPageOptions = props.rowsPerPageOptions ?? [5, 10, 20, 50]

// 🔥 VALORES POR DEFECTO PARA ACCIONES
const showActions = props.showActions ?? true
const actions = props.actions ?? []

// 🔥 ESTADO PARA REDIMENSIONADO
const columnWidths = ref<Record<string, number>>({})
const isResizing = ref(false)
const currentResizeColumn = ref<string | null>(null)
const startX = ref(0)
const startWidth = ref(0)

// 🔥 COLUMNAS PROCESADAS CON ANCHOS (FILTRAR ACCIONES SI NO SE MUESTRAN)
const processedColumns = computed(() => {
  let columnsToProcess = props.columns

  // Si showActions es false, filtrar la columna actions
  if (!showActions) {
    columnsToProcess = props.columns.filter(col => col.name !== 'actions')
  }

  return columnsToProcess.map(col => ({
    ...col,
    style: getColumnStyle(col.name),
    classes: 'resizable-column'
  }))
})

// 🔥 INICIALIZAR ANCHOS
onMounted(() => {
  processedColumns.value.forEach(col => {
    if (!columnWidths.value[col.name]) {
      columnWidths.value[col.name] = getDefaultWidth(col)
    }
  })
})

// 🔥 OBTENER ANCHO POR DEFECTO GENÉRICO
function getDefaultWidth(col: QTableColumn): number {
  // 🔥 ANCHO FIJO PARA ACCIONES
  if (col.name === 'actions') return 120

  const labelLength = col.label?.length || 0
  const fieldType = typeof col.field

  if (labelLength <= 5) return 100
  if (labelLength <= 10) return 150
  if (labelLength <= 15) return 180
  if (labelLength > 15) return 220

  if (fieldType === 'function') return 200
  if (col.align === 'center') return 120

  return 160
}

// 🔥 INICIAR REDIMENSIONADO
function startResize(columnName: string, event: MouseEvent) {
  isResizing.value = true
  currentResizeColumn.value = columnName
  startX.value = event.clientX
  startWidth.value = columnWidths.value[columnName]

  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'

  event.preventDefault()
}

// 🔥 MANEJAR REDIMENSIONADO
function handleResize(event: MouseEvent) {
  if (!isResizing.value || !currentResizeColumn.value) return

  const deltaX = event.clientX - startX.value
  const newWidth = Math.max(80, startWidth.value + deltaX) // Mínimo 80px

  columnWidths.value[currentResizeColumn.value] = newWidth
}

// 🔥 DETENER REDIMENSIONADO
function stopResize() {
  isResizing.value = false
  currentResizeColumn.value = null

  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// 🔥 OBTENER ESTILO PARA COLUMNA
function getColumnStyle(columnName: string) {
  const width = columnWidths.value[columnName] || getDefaultWidth(props.columns.find(c => c.name === columnName)!)
  return {
    width: `${width}px`,
    minWidth: columnName === 'actions' ? '120px' : '80px',
    maxWidth: '500px',
    position: 'relative'
  }
}

// 🔥 LIMPIAR EVENT LISTENERS
onUnmounted(() => {
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
})

// 🔥 FUNCIONES PARA MANEJAR ACCIONES
const getRowActions = (row: any) => {
  return actions.filter(action => {
    // Si tiene condición, evaluarla
    if (action.condition && typeof action.condition === 'function') {
      return action.condition(row)
    }
    return true
  })
}

const isActionVisible = (action: TableAction, row: any) => {
  if (typeof action.visible === 'function') {
    return action.visible(row)
  }
  return action.visible !== false
}

const emitAction = (actionName: string, row: any) => {
  emit('action', { action: actionName, row })
}

// 🔹 Computed para información de paginación
const paginationInfo = computed(() => {
  const start = (props.pagination.page - 1) * props.pagination.rowsPerPage + 1
  const end = Math.min(start + props.pagination.rowsPerPage - 1, props.rowsNumber)
  return `${start}-${end} de ${props.rowsNumber}`
})

// 🔹 Computed para última página
const lastPage = computed(() => {
  return Math.ceil(props.rowsNumber / props.pagination.rowsPerPage)
})

// 🔹 Computed para verificar si es la última página
const isLastPage = computed(() => {
  return props.pagination.page >= lastPage.value
})

// 🔹 Función para cambiar de página
function goToPage(page: number) {
  if (page >= 1 && page <= lastPage.value) {
    emit('update:pagination', {
      ...props.pagination,
      page: page
    })
  }
}

// 🔹 Función para cambiar filas por página
function onRowsPerPageChange(rowsPerPage: number) {
  emit('update:pagination', {
    ...props.pagination,
    rowsPerPage: rowsPerPage,
    page: 1
  })
}

function onRequest(propsRequest: any) {
  emit('update:pagination', propsRequest.pagination)
}
</script>

<style scoped>
/* Encabezados personalizados */
.institucional-table__header {
  font-weight: 700;
  font-size: 14px;
  background-color: #f5f5f5;
  color: #1c1c1c;
  text-transform: uppercase;
  border-bottom: 1px solid #ccc;
}

/* 🔥 PADDING Y MARGIN REDUCIDOS */
:deep(.q-table__bottom) {
  min-height: 32px !important;
  border-top: 1px solid rgba(0,0,0,0.12);
  background-color: #fafafa;
  padding: 0px !important; /* Eliminado padding interno */
}

:deep(.q-table__bottom .q-btn) {
  font-size: 12px;
  padding: 1px 3px !important; /* Reducido padding de botones */
  min-height: 20px;
  min-width: 20px;
  margin: 0px 1px !important; /* Reducido margin de botones */
}

:deep(.q-table__bottom .q-btn .q-icon) {
  font-size: 12px;
}

:deep(.q-table__bottom .q-select) {
  font-size: 12px;
  min-width: 60px;
  margin: 0px 2px !important; /* Reducido margin del select */
}

:deep(.q-table__bottom .q-select__dropdown-icon) {
  font-size: 12px;
}

:deep(.q-table__bottom .text-caption) {
  font-size: 12px;
  margin: 0px 4px !important; /* Reducido margin de textos */
}

/* Espacios reducidos entre elementos */
:deep(.q-table__bottom .q-gutter-sm) {
  margin: 0 -2px !important;
}

:deep(.q-table__bottom .q-gutter-xs) {
  margin: 0 -1px !important;
}

.my-sticky-virtscroll-table {
  height: 500px;
}

.my-sticky-virtscroll-table .q-table__top,
.my-sticky-virtscroll-table .q-table__bottom,
.my-sticky-virtscroll-table thead tr:first-child th {
  background-color: bg-grey-2;
}

.my-sticky-virtscroll-table thead tr th {
  position: sticky;
  z-index: 1;
}

.my-sticky-virtscroll-table thead tr:last-child th {
  top: 48px;
}

.my-sticky-virtscroll-table thead tr:first-child th {
  top: 0;
}

.my-sticky-virtscroll-table tbody {
  scroll-margin-top: 25px;
}


:deep(.custom-select .q-select__dropdown-icon) {
  font-size: 18px !important;
  padding: 2px;
}

/* 🔥 SCROLL MUY DISCRETO */
:deep(.my-sticky-virtscroll-table ::-webkit-scrollbar) {
  width: 6px !important;
  height: 6px !important;
}

:deep(.my-sticky-virtscroll-table ::-webkit-scrollbar-thumb) {
  background: #dee2e6;
  border-radius: 2px;
}

:deep(.my-sticky-virtscroll-table ::-webkit-scrollbar-thumb:hover) {
  background: #6c757d;
 }


.actions-container {
  display: flex;
  gap: 4px;
  justify-content: center;
  align-items: center;
}

.action-btn {
  margin: 0 2px;
}

.column-resize-handle {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 5px;
  cursor: col-resize;
  background: transparent;
  transition: background-color 0.2s;
}

.column-resize-handle:hover {
  background-color: #ccc;
}

.resizable-column {
  position: relative;
}

.top-actions-container {
  min-height: 5px;
  padding: 0px 0px 0px 0px;
}

.top-actions {
  display: flex;
  gap: 20px;
}

.top-actions {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  gap: 20px;
}

.top-action-btn {
  margin: 0;
  width: 5px;
  height: 5px;
}

/* Efecto hover sutil */
.top-action-btn:hover {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}

</style>
