<script setup lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useUnidades } from '@/composables/useUnidades'
import { useSessionStore } from '@/stores/session'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'nombre', label: 'Nombre', field: 'nombre', align: 'left', sortable: true },
  { name: 'isEmpresaDisplay', label: 'Empresa', field: 'isEmpresaDisplay', align: 'center', sortable: true },
  { name: 'isComercializadoraDisplay', label: 'Comercializadora', field: 'isComercializadoraDisplay', align: 'center', sortable: true },
  { name: 'activoDisplay', label: 'Activa', field: 'activoDisplay', align: 'center', sortable: true },
]

const CrudComponent = createCrudListView(useUnidades, columns, {
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  onAction: (action, row) => {
    console.log(`Acción ${action} en unidades:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
