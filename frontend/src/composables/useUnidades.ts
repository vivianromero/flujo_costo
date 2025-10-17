// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de unidades contables no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente

import { ref, computed, watchEffect, watch, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from 'graphql-tag'

const GET_UNIDADES = gql`
  query GetUnidades($page: Int!, $limit: Int!, $codigo: String, $nombre: String, $activo: Boolean) {
    unidades(page: $page, limit: $limit, codigo: $codigo, nombre: $nombre, activo: $activo) {
      items {
        id
        codigo
        nombre
        isEmpresa
        isComercializadora
        activo
      }
      totalCount
    }
  }
`

export function useUnidades(options: {
  pagination: Ref<{ page: number; rowsPerPage: number }>
  codigo?: Ref<string | null>
  nombre?: Ref<string | null>
  activo?: Ref<boolean | null>
}) {
  const allRows = ref<any[]>([]) // 🔹 Todos los datos
  const rows = ref<any[]>([])    // 🔹 Página actual
  const loading = ref(true)
  const totalCount = ref(0)


const variables = computed(() => ({
  page: 1,
  limit: 99999,
  codigo: options.codigo?.value ?? null,
  nombre: options.nombre?.value ?? null,
  activo: options.activo?.value ?? null
}))


  const { result, refetch } = useQuery(GET_UNIDADES, variables, {
    enabled: computed(() => !!variables.value),
    fetchPolicy: 'cache-first'
  })

  // 🔹 Forzar carga inicial al montar
onMounted(() => {
  if (result.value?.unidades?.items?.length) {
    console.log('✅ Datos ya disponibles al montar')
    allRows.value = result.value.unidades.items
    totalCount.value = result.value.unidades.totalCount
    loading.value = false
    paginate()
  } else {
    console.log('🚀 Forzando refetch al montar')
    refetch(variables.value)
  }
})

  // 🔹 Reforzar reactividad si variables cambian
  watchEffect(() => {
    const vars = variables.value
    if (!vars) return
    console.log('🔁 watchEffect: ejecutando refetch con', vars)
    refetch(vars)
  })

  // 🔹 Cuando llegan los datos, cachea y pagina
  watch(result, (data) => {
    const items = data?.unidades?.items ?? []
    console.log('📦 Datos recibidos:', items.length, 'items')
    allRows.value = items
    totalCount.value = items.length
    loading.value = false
    paginate()
  })

  // 🔹 Recalcula la página visible cuando cambia la paginación
  watch(() => options.pagination.value, (val) => {
    console.log('📄 Cambio de paginación:', val)
    paginate()
  }, { deep: true })


  function paginate() {
    const { page, rowsPerPage } = options.pagination.value
    const start = (page - 1) * rowsPerPage
    const end = start + rowsPerPage
    rows.value = allRows.value.slice(start, end)
    console.log(`📊 Mostrando filas ${start + 1} a ${Math.min(end, totalCount.value)} de ${totalCount.value}`)
  }

  return {
    rows,
    loading,
    totalCount,
    refetch
  }
}
