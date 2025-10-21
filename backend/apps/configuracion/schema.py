import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

class UserUebType(DjangoObjectType):
    ueb = graphene.String()
    isAdminempresa = graphene.Boolean()
    isOpercosto = graphene.Boolean()
    isOperflujo = graphene.Boolean()
    isAdmin = graphene.Boolean()

    class Meta:
        model = get_user_model()
        fields = ('username', 'ueb', 'is_adminempresa', 'is_opercosto', 'is_operflujo')

    def resolve_ueb(self, info):
        return str(self.ueb) if self.ueb else ''

    def resolve_isAdminempresa(self, info):
        return self.is_adminempresa

    def resolve_isOperflujo(self, info):
        return self.is_operflujo

    def resolve_isOpercosto(self, info):
        return self.is_opercosto

    def resolve_isAdmin(self, info):
        return self.is_admin


class ConfiguracionQuery(graphene.ObjectType):
    me = graphene.Field(UserUebType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

class ConfiguracionMutation(graphene.ObjectType):
    pass  # Aquí puedes agregar mutaciones como editar perfil, cambiar UEB, etc.


