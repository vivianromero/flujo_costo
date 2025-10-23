<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useDepartamentos } from '@/composables/useDepartamentos'
import { useSessionStore } from '@/stores/session'
import { ref } from 'vue'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true, width: '100px' },
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true, width: '200px' },
  {
    name: 'centrocosto',
    label: 'Centro de Costo',
    field: row => {
        const centro = row.centrocosto
        if (!centro) return 'Sin centro'
        const clave = centro.clave || 'S/C'
        const descripcion = centro.descripcion || 'Sin descripción'
        return `${clave} | ${descripcion}`
      },
    align: 'left',
    sortable: true,
    width: '250px'
  }
]

const CrudComponent = createCrudListView(useDepartamentos, columns, {
  showActions: true,
  loadAll: true,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en departamento:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>



