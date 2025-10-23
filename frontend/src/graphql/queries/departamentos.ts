import { gql } from 'graphql-tag'

export const GET_DEPARTAMENTOS = gql`
  query GetDepartamentos($page: Int!, $limit: Int!, $centroId: ID, $centroActivo: Boolean) {
    departamentos(page: $page, limit: $limit, centroId: $centroId, centroActivo: $centroActivo) {
      items {
        id
        codigo
        descripcion
        centrocosto {
          clave
          descripcion
        }
      }
      totalCount
    }
  }
`
