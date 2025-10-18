<script lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useDepartamentos } from '@/composables/useDepartamentos'

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true },
  {
    name: 'centrocosto',
    label: 'Centro de Costo',
    field: row => row.centrocosto?.descripcion || '',
    align: 'left',
    sortable: true
  }
]

export default createCrudListView(useDepartamentos, columns)
</script>



