<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useTiposDocumentos } from '@/composables/useTiposDocumentos'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
  { name: 'operacion', label: 'Operación',
     field: row => formatters.entradaSalida(row.operacion),
     align: 'left', sortable: true },
  { name: 'prefijo', label: 'Prefijo', field: 'prefijo', align: 'left', sortable: true },
  { name: 'generado',
    label: 'Generado',
    field: row => formatters.siNo(row.generado),
    align: 'center',
    sortable: true
  },
]

const CrudComponent = createCrudListView(useTiposDocumentos, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: true,
  noView: true,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: true,
  onAction: (action, row) => {
    console.log(`Acción ${action} en tipos de documentos:`, row)
  },
  loadAll: true
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
