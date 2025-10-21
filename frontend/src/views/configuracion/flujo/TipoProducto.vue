<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useTiposProductos } from '@/composables/useTiposProductos'
import { useSessionStore } from '@/stores/session'
import { formatters } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
]

const CrudComponent = createCrudListView(useTiposProductos, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: true,
  noView: true,
  onAction: (action, row) => {
    console.log(`Acción ${action} en tipos de productos:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
