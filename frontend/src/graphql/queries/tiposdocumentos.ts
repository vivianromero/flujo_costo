import { gql } from 'graphql-tag'

export const GET_TIPOSDOCUMENTOS = gql`
  query GetTiposDocumentos($page: Int!, $limit: Int!, $descripcion: String, $operacion: String, $prefijo: String, $generado: Boolean) {
    tiposdocumentos(page: $page, limit: $limit, descripcion: $descripcion, operacion: $operacion, prefijo: $prefijo, generado: $generado) {
      items {
        id
        descripcion
        operacion
        prefijo
        generado
      }
      totalCount
    }
  }
`