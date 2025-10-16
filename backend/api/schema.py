import graphene
import graphql_jwt

from apps.configuracion.schema import ConfiguracionQuery, ConfiguracionMutation, UserUebType
from apps.codificadores.schema import CodificadoresQuery, CodificadoresMutation
# Si tienes otros módulos, los importas igual:


class Query(CodificadoresQuery,
            graphene.ObjectType):
    me = graphene.Field(UserUebType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("No autenticado")
        return user


class Mutation(
    ConfiguracionMutation,
    CodificadoresMutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# import graphene
# from apps.configuracion.schema import ConfiguracionQuery, ConfiguracionMutation
# # from apps.codificadores.schema import CodificadoresQuery, CodificadoresMutation
# from graphql_jwt.decorators import login_required
# import graphql_jwt
#
# class Query(ConfiguracionQuery, graphene.ObjectType):
#     pass
#
# class Mutation(ConfiguracionMutation, graphene.ObjectType):
#     token_auth = graphql_jwt.ObtainJSONWebToken.Field()
#     verify_token = graphql_jwt.Verify.Field()
#     refresh_token = graphql_jwt.Refresh.Field()
#
# schema = graphene.Schema(query=Query, mutation=Mutation)

