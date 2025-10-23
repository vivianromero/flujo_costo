import { gql } from 'graphql-tag'

export const GET_MEDIDAS = gql`
  query GetMedidas($page: Int!, $limit: Int!, $clave: String, $descripcion: String, $activa: Boolean) {
    medidas(page: $page, limit: $limit, clave: $clave, descripcion: $descripcion, activa: $activa) {
      items {
        id
        clave
        descripcion
        activa
      }
      totalCount
    }
  }
`