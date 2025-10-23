<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useMotivosAjuste } from '@/composables/useMotivosAjuste'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'descripcion', label: 'Motivo', field: 'descripcion', align: 'left', sortable: true },
  { name: 'aumento', label: 'Aumento/Disminución',
    field: row => formatters.aumentoDisminucion(row.aumento),
    align: 'center',
    sortable: true
  },
  { name: 'activo', label: 'Activa',
    field: row => formatters.estado(row.activo),
    align: 'center',
    sortable: true
  },
]

const CrudComponent = createCrudListView(useMotivosAjuste, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noView: true,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en motivos de ajuste:`, row)
  },
  loadAll: true
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
