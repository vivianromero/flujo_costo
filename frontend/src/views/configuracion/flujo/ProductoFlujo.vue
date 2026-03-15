<script setup lang="ts">
import { ref } from 'vue'
import { createCrudListView } from '@/factories/createCrudListView'
import { useProductoFlujo } from '@/composables/useProductoFlujo'
import { useSessionStore } from '@/stores/session'
import { activoFormatter } from '@/utils/fieldFormatters'
import BaseCrudView from '@/components/cruds/BaseCrudView.vue'

const session = useSessionStore()

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'descripcion', label: 'Producto', field: 'descripcion', align: 'left', sortable: true },
  { name: 'medidaClave', label: 'U.M', field: 'medidaClave', align: 'left', sortable: true },
  { name: 'tipoProducto', label: 'Tipo Producto', field: 'tipoProducto', align: 'left', sortable: true },
  { name: 'claseMateriaprima', label: 'Clase MP/Habilitación', field: (row) => row.claseMateriaprima?.descripcion || '-', align: 'left', sortable: true },
  { name: 'activo', label: 'Activo', field: activoFormatter, align: 'center', sortable: true},
]


const CrudComponent = createCrudListView(useProductoFlujo, columns, {
  rowsPerPage: 50,
  showActions: session.isAdminempresa,
  noEdit: !session.isAdminempresa,
  noDelete: !session.isAdminempresa,
  noView: true,
  onAction: (action, row) => {
    console.log(`Acción ${action} en producto flujo:`, row)
  }
})
</script>

<template>
  <BaseCrudView :component="CrudComponent" />
</template>
