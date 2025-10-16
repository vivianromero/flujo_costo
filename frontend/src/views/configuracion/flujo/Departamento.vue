<template>
  <InstitucionalTable
    :columns="columns"
    :rows="rows"
    :loading="loading"
    :rows-per-page-options="[5, 15, 25, 30, 50]"
    :rows-per-page="pagination.rowsPerPage"
    v-model:pagination="pagination"
    :rows-number="totalCount"
  />
</template>

<script setup lang="ts">
import InstitucionalTable from '@/components/InstitucionalTable.vue'
import { ref, watch } from 'vue'
import { useDepartamentosPaginado } from '@/composables/useDepartamentosPaginado'

//const pagination = ref({ page: 1, rowsPerPage: 15, rowsNumber: 0 })
const pagination = ref({ page: 1, rowsPerPage: 15 })

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
  {
    name: 'centrocosto',
    label: 'Centro de Costo',
    field: (row: any) => row.centrocosto?.descripcion || 'Sin centro',
    align: 'left',
    sortable: true
  }
]

const { rows, loading, totalCount } = useDepartamentosPaginado({ pagination })

watch(totalCount, (newTotal) => {
  pagination.value.rowsNumber = newTotal
})


</script>


