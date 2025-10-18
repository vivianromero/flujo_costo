<script lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useUnidades } from '@/composables/useUnidades'


const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true },
  { name: 'nombre', label: 'Nombre', field: 'nombre', align: 'left', sortable: true },
  { name: 'isEmpresaDisplay', label: 'Empresa', field: 'isEmpresaDisplay', align: 'center', sortable: true },
  { name: 'isComercializadoraDisplay', label: 'Comercializadora', field: 'isComercializadoraDisplay', align: 'center', sortable: true },
  { name: 'activoDisplay', label: 'Activa', field: 'activoDisplay', align: 'center', sortable: true },
]

export default createCrudListView(useUnidades, columns)
</script>
