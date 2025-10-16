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
}>()

const emit = defineEmits(['update:pagination'])


const rowKey = props.rowKey ?? 'id'
const dropdownIcon = props.dropdownIcon ?? 'fa fa-chevron-down'
const rowsPerPageOptions = props.rowsPerPageOptions ?? [5, 10, 20, 50]

function onRequest (props: any) {
  emit('update:pagination', props.pagination)
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


/* Estilos para botones de paginación */
:deep(.q-table__bottom .q-btn) {
  font-size: 14px;
  padding: 4px 6px;
  min-height: 24px;
  min-width: 24px;
}

/* Tamaño de íconos dentro de los botones */
:deep(.q-table__bottom .q-btn .q-icon),
:deep(.q-table__bottom .q-select__dropdown-icon) {
  font-size: 16px;
}


.my-sticky-virtscroll-table {
  /* height or max-height is important */
  height: 500px;
}

.my-sticky-virtscroll-table .q-table__top,
.my-sticky-virtscroll-table .q-table__bottom,
.my-sticky-virtscroll-table thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: bg-grey-2;
}

.my-sticky-virtscroll-table thead tr th {
  position: sticky;
  z-index: 1;
}

.my-sticky-virtscroll-table thead tr:last-child th {
  /* height of all previous header rows */
  top: 48px;
}

.my-sticky-virtscroll-table thead tr:first-child th {
  top: 0;
}

/* prevent scrolling behind sticky top row on focus */
.my-sticky-virtscroll-table tbody {
  /* height of all previous header rows */
  scroll-margin-top: 25px;
}

.institucional-table :deep(.q-table__bottom .q-select__menu) {
  max-width: 200px !important;
}

.institucional-table :deep(.q-table__bottom .q-field) {
  max-width: 120px;
}

</style>
