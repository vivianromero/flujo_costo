<template>
  <div class="institucional-table q-pa-md">
      <q-btn
          flat
          dense
          round
          size="xs"
          icon="fa-solid fa-rotate"
          color="blue-2"
          @click="emit('refresh')"
        >
          <q-tooltip anchor="top middle" self="bottom middle">
            Actualizar Datos
          </q-tooltip>
        </q-btn>

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
      style="position: relative;"
      :grid="$q.screen.xs"
    >

      <!-- 🔹 Encabezados personalizados -->

    </q-table>

  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { QTableColumn } from 'quasar'
import { toRaw } from 'vue'

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
  border-bottom: 2px solid #ccc;
}


.bottom-left-refresh {
  position: absolute;
  left: 8px;
  bottom: 8px;
  z-index: 20;
}
</style>
