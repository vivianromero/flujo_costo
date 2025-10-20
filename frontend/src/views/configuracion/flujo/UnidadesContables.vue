<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useUnidades } from '@/composables/useUnidades'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'nombre', label: 'Nombre', field: 'nombre', align: 'left', sortable: true },
  { name: 'isEmpresa',
    label: 'Empresa',
    field: row => formatters.empresa(row.isEmpresa),
    align: 'center',
    sortable: true },
  { name: 'isComercializadora', label: 'Comercializadora',
    field: row => formatters.comercializadora(row.isComercializadora), align: 'center', sortable: true },
  { name: 'activo', label: 'Activa', field: row => formatters.activa(row.activo), align: 'center', sortable: true },
]

const CrudComponent = createCrudListView(useUnidades, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: true,
  onAction: (action, row) => {
    console.log(`Acción ${action} en unidades:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
