<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useMarcasSalida } from '@/composables/useMarcasSalida'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'descripcion', label: 'Marca', field: 'descripcion', align: 'left', sortable: true },
  { name: 'activa', label: 'Activa',
    field: row => formatters.activa(row.activa),
    align: 'center',
    sortable: true
  },
]

const CrudComponent = createCrudListView(useMarcasSalida, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noView: true,
  noFetchFromSystem: true,
  noExport: !session.isAdminempresa,
  noCreate: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en marcas de salida:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
