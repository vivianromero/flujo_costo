import { gql } from 'graphql-tag'

export const GET_MARCASSALIDA = gql`
  query GetMarcasSalida($page: Int!, $limit: Int!, $codigo: String, $descripcion: String, $activa: Boolean) {
    marcassalida(page: $page, limit: $limit, codigo: $codigo, descripcion: $descripcion, activa: $activa) {
      items {
        id
        codigo
        descripcion
        activa
      }
      totalCount
    }
  }
`