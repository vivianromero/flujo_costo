<template>
  <div class="q-pa-md">
    <q-table
      flat
      bordered
      :title="title"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
      :rows-per-page-options="[5, 15, 20, 25, 50]"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import type { QTableColumn } from 'quasar'

interface CrudViewProps {
  title: string
  query: any
  columns: QTableColumn[]
  dataPath?: string
}

const props = defineProps<CrudViewProps>()
console.log('🎯 CrudView props:', props)

const rows = ref<any[]>([])
const loading = ref(true)

// 🔹 Carga con Apollo - USAR onResult
const { result, refetch, loading: apolloLoading, onResult } = useQuery(props.query)

onResult((queryResult) => {
  console.log('🎯 onResult triggered:', queryResult)

  loading.value = queryResult.loading

  if (queryResult.data) {
    console.log('✅ Datos recibidos:', queryResult.data)

    const path = props.dataPath?.split('.') ?? ['departamentos']
    console.log('🛣️ Path a extraer:', path)

    let data: any = queryResult.data
    for (const p of path) {
      console.log(`🔍 Buscando: ${p} en`, data)
      data = data?.[p]
    }

    console.log('📦 Datos extraídos:', data)
    rows.value = Array.isArray(data) ? data : []
    console.log('🎯 Rows actualizado:', rows.value.length, 'elementos')
  }
})

// Watch para el estado de carga (opcional)
watch(apolloLoading, (isLoading) => {
  console.log('📡 Apollo loading:', isLoading)
  loading.value = isLoading
})

// Refetch público
defineExpose({
  refetch
})
</script>
