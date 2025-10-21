<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useMedidas } from '@/composables/useMedidas'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'clave', label: 'U.M', field: 'clave', align: 'left', sortable: true },
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
  { name: 'activa',
    label: 'Activa',
    field: row => formatters.activa(row.activa),
    align: 'center',
    sortable: true
   }
]

const CrudComponent = createCrudListView(useMedidas, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noView: true,
  noFetchFromSystem: !session.isAdminempresa,
  tooltipFetchFromSystem: 'Actualizar desde Versat',
  noExport: !session.isAdminempresa,
  noCreate: true,
  onAction: (action, row) => {
    console.log(`Acción ${action} en medidas:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
