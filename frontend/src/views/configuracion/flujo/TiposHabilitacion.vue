<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useTiposHabilitaciones } from '@/composables/useTiposHabilitaciones'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
  { name: 'activo',
    label: 'Activa',
    field: row => formatters.activa(row.activo),
    align: 'center',
    sortable: true
  },
]

const CrudComponent = createCrudListView(useTiposHabilitaciones, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: true,
  noView: true,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en tipos de habilitaciones:`, row)
  },
  loadAll: true
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
