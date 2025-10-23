import { gql } from 'graphql-tag'

export const GET_TIPOSHABILITACIONES = gql`
  query GetTiposHabilitaciones($page: Int!, $limit: Int!, $descripcion: String, $activo: Boolean) {
    tiposhabilitaciones(page: $page, limit: $limit, descripcion: $descripcion, activo: $activo) {
      items {
        id
        descripcion
        activo
      }
      totalCount
    }
  }
`