import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import UserUeb
from apps.codificadores.models import UnidadContable

class UnidadContableType(DjangoObjectType):
    class Meta:
        model = UnidadContable
        fields = ("id", "codigo", "nombre")  # ← puedes agregar más campos luego

class UserUebType(DjangoObjectType):
    class Meta:
        model = UserUeb
        fields = ("id", "username", "ueb")  # ← solo lo esencial por ahora


class ConfiguracionQuery(graphene.ObjectType):
    me = graphene.Field(UserUebType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

class ConfiguracionMutation(graphene.ObjectType):
    pass  # Aquí puedes agregar mutaciones como editar perfil, cambiar UEB, etc.


