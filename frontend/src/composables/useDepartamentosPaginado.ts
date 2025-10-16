// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de departamentos no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente

import { ref, computed, watchEffect, watch, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from 'graphql-tag'

const GET_DEPARTAMENTOS = gql`
  query GetDepartamentos($page: Int!, $limit: Int!, $centroId: ID, $activos: Boolean) {
    departamentos(page: $page, limit: $limit, centroId: $centroId, activos: $activos) {
      items {
        id
        codigo
        descripcion
        centrocosto {
          descripcion
        }
      }
      totalCount
    }
  }
`

export function useDepartamentosPaginado(options: {
  pagination: Ref<{ page: number; rowsPerPage: number }>
  centroId?: Ref<string | null>
  activos?: Ref<boolean | null>
}) {
  const allRows = ref<any[]>([]) // 🔹 Todos los datos
  const rows = ref<any[]>([])    // 🔹 Página actual
  const loading = ref(true)
  const totalCount = ref(0)


const variables = computed(() => ({
  page: 1,
  limit: 99999,
  centroId: options.centroId?.value ?? null,
  activos: options.activos?.value ?? null
}))


  const { result, refetch } = useQuery(GET_DEPARTAMENTOS, variables, {
    enabled: computed(() => !!variables.value),
    fetchPolicy: 'cache-first'
  })

  // 🔹 Forzar carga inicial al montar
onMounted(() => {
  if (result.value?.departamentos?.items?.length) {
    console.log('✅ Datos ya disponibles al montar')
    allRows.value = result.value.departamentos.items
    totalCount.value = result.value.departamentos.totalCount
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
    const items = data?.departamentos?.items ?? []
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
