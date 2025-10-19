<script lang="ts">
import { createCrudListView } from '@/factories/createCrudListView'
import { useDepartamentos } from '@/composables/useDepartamentos'

const columns = [
  { name: 'codigo', label: 'Código', field: 'codigo', align: 'left', sortable: true, width: '100px' },
  { name: 'descripcion', label: 'Descripción', field: 'descripcion', align: 'left', sortable: true, width: '200px' },
  {
    name: 'centrocosto',
    label: 'Centro de Costo',
    field: row => {
        const centro = row.centrocosto
        if (!centro) return 'Sin centro'

        const clave = centro.clave || 'S/C'  // S/C = Sin Código
        const descripcion = centro.descripcion || 'Sin descripción'

        return `${clave} | ${descripcion}`
      },
    align: 'left',
    sortable: true,
    width: '250px'
  }
]

export default createCrudListView(useDepartamentos, columns)
</script>



