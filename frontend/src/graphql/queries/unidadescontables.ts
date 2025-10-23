import { gql } from 'graphql-tag'

export const GET_UNIDADES = gql`
  query GetUnidades($page: Int!, $limit: Int!, $codigo: String, $nombre: String, $activo: Boolean) {
    unidades(page: $page, limit: $limit, codigo: $codigo, nombre: $nombre, activo: $activo) {
      items {
        id
        codigo
        nombre
        isComercializadora
        isEmpresa
        activo
      }
      totalCount
    }
  }
`