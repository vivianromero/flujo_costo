// 🔹 Este composable usa paginado local con limit 9999
// 🔹 Asume que la cantidad de conversion de medida no supera ese valor
// 🔹 Si se supera, los datos se truncarán silenciosamente
import { computed } from 'vue'
import type { Ref } from 'vue'
import { useSmartPagination } from '@/composables/useSmartPagination'
import { gql } from 'graphql-tag'

const GET_MEDIDASCONVERSION = gql`
  query GetMedidasConversion($page: Int!, $limit: Int!, $medidao: String, $medidad: String) {
    medidasconversion(page: $page, limit: $limit, medidao: $medidao, medidad: $medidad) {
      items {
        id
        factorConversion
        medidao {
          clave
          descripcion
        }
        medidad {
          clave
          descripcion
        }
      }
      totalCount
    }
  }
`

export function useMedidasConversion(options: {
  pagination: Ref<{ page: number; rowsPerPage: number; sortBy?: string; descending?: boolean }>
  factorConversion?: Ref<string | null>
  medidao?: Ref<string | null>
  medidad?: Ref<string | null>
  columns?: any[]
}) {

    const variables = computed(() => {
      const vars: Record<string, any> = {
        page: options.pagination.value.page,
        limit: options.pagination.value.rowsPerPage,
      }
      if (options.factorConversion?.value) vars.factorConversion = options.factorConversion.value
      if (options.medidao?.value) vars.medidao = options.medidao.value
      if (options.medidad?.value) vars.medidad = options.medidad.value
      return vars
    })

  const smartPagination = useSmartPagination({
    query: GET_MEDIDASCONVERSION,
    variables,
    pagination: options.pagination,
    columns: options.columns // 🔥 Pasar las columns para ordenamiento inteligente
  })

  return {
    rows: smartPagination.rows,
    loading: smartPagination.loading,
    totalCount: smartPagination.totalCount,
    refetch: smartPagination.refetch,
    allRows: smartPagination.allRows // Para debug
  }
}