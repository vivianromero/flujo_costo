import graphene
from graphql_jwt.decorators import login_required
from apps.codificadores.models import UnidadContable
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

class UnidadContableType(DjangoObjectType):
    class Meta:
        model = UnidadContable
        fields = ("id", "codigo", "nombre")  # ← puedes agregar más campos luego

class UserUebType(DjangoObjectType):
    ueb = graphene.String()

    class Meta:
        model = get_user_model()
        fields = ('username', 'ueb')

    def resolve_ueb(self, info):
        return str(self.ueb) if self.ueb else ''


class ConfiguracionQuery(graphene.ObjectType):
    me = graphene.Field(UserUebType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

class ConfiguracionMutation(graphene.ObjectType):
    pass  # Aquí puedes agregar mutaciones como editar perfil, cambiar UEB, etc.


