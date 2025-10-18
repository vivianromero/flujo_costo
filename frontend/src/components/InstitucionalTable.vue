<template>
  <div class="institucional-table q-pa-md">
    <q-table
      flat
      bordered
      dense
      virtual-scroll
      :virtual-scroll-sticky-size-start="60"
      :rows="rows"
      :columns="columns"
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
      <!-- 🔹 Encabezados personalizados -->
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
            class="institucional-table__header"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <!-- 🔹 Slot bottom con padding reducido -->
      <template v-slot:bottom>
        <div class="row full-width items-center justify-between" style="padding: 0px 10px 0px 10px;">
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
                  style="min-width: 35px; padding-right:10px; "
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
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { QTableColumn } from 'quasar'

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
}>()

const emit = defineEmits(['update:pagination', 'refresh'])

const rowKey = props.rowKey ?? 'id'
const dropdownIcon = props.dropdownIcon ?? 'fa fa-chevron-down'
const rowsPerPageOptions = props.rowsPerPageOptions ?? [5, 10, 20, 50]

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
</style>
