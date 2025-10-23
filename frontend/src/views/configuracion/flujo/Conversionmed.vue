<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useMedidasConversion } from '@/composables/useMedidasConversion'
import { useSessionStore } from '@/stores/session'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [

  { name: 'medidao', label: 'Medida Origen',
    field: row => {
        const origen = row.medidao
        if (!origen) return 'Sin origen'
        const clave = origen.clave || 'S/C'
        const descripcion = origen.descripcion || 'Sin descripción'
        return `${clave} | ${descripcion}`
      },
    align: 'left', sortable: true, width: '250px'
  },
  { name: 'medidad', label: 'Medida Destino',
    field: row => {
        const destino = row.medidad
        if (!destino) return 'Sin destino'
        const clave = destino.clave || 'S/C'
        const descripcion = destino.descripcion || 'Sin descripción'
        return `${clave} | ${descripcion}`
      },
    align: 'left', sortable: true, width: '250px'
  },
  { name: 'factorConversion', label: 'Factor de Conversión', field: 'factorConversion',
    align: 'right', sortable: true, width: '50px' },
]

const CrudComponent = createCrudListView(useMedidasConversion, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noView: true,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en conversion de medidas:`, row)
  },
  loadAll: true
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>



