import { gql } from 'graphql-tag'

export const GET_MOTIVOSAJUSTE = gql`
  query GetMotivosAjuste($page: Int!, $limit: Int!, $descripcion: String, $activo: Boolean, $aumento: Boolean) {
    motivosajuste(page: $page, limit: $limit, descripcion: $descripcion, activo: $activo, aumento: $aumento) {
      items {
        id
        descripcion
        aumento
        activo
      }
      totalCount
    }
  }
`