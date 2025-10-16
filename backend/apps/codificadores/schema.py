import graphene
from graphene_django import DjangoObjectType
from .models import Departamento, CentroCosto

# =====================================================
#  TYPES
# =====================================================

class CentroCostoType(DjangoObjectType):
    class Meta:
        model = CentroCosto
        fields = ("id", "clave", "descripcion", "activo")


class DepartamentoType(DjangoObjectType):
    class Meta:
        model = Departamento
        fields = ("id", "codigo", "descripcion", "centrocosto")


class DepartamentoConnection(graphene.ObjectType):
    items = graphene.List(DepartamentoType)
    total_count = graphene.Int()

# =====================================================
#  QUERIES
# =====================================================

class CodificadoresQuery(graphene.ObjectType):
    departamentos = graphene.Field(
        DepartamentoConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        centro_id=graphene.ID(),
        activos=graphene.Boolean()
    )
    centros_costo = graphene.List(CentroCostoType)

    def resolve_departamentos(root, info, page, limit, centro_id=None, activos=None):
        qs = Departamento.objects.select_related("centrocosto")

        if centro_id:
            qs = qs.filter(centrocosto_id=centro_id)

        if activos is not None:
            qs = qs.filter(centrocosto__activo=activos)

        total = qs.count()
        offset = (page - 1) * limit
        items = qs[offset:offset + limit]

        return DepartamentoConnection(items=items, total_count=total)

    def resolve_centros_costo(root, info):
        return CentroCosto.objects.all()

# =====================================================
#  MUTATIONS
# =====================================================

class CodificadoresMutation(graphene.ObjectType):
    pass



