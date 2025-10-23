import { gql } from 'graphql-tag'

export const GET_TIPOSPRODUCTOS = gql`
  query GetTiposProductos($page: Int!, $limit: Int!, $descripcion: String) {
    tiposproductos(page: $page, limit: $limit, descripcion: $descripcion) {
      items {
        id
        descripcion
      }
      totalCount
    }
  }
`