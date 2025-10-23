import { gql } from 'graphql-tag'

export const GET_MEDIDASCONVERSION = gql`
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