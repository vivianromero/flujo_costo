import graphene
from graphene_django import DjangoObjectType
from .models import Departamento, CentroCosto, UnidadContable
from apps.utiles.utils import paginate_queryset


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

class UnidadContableType(DjangoObjectType):
    class Meta:
        model = UnidadContable
        fields = ("id", "codigo", "nombre", "is_empresa", "is_comercializadora", "activo")


# =====================================================
#  CONNECTION
# =====================================================
class PaginatedType(graphene.ObjectType):
    items = graphene.List(graphene.GenericScalar)  # se sobrescribe luego
    total_count = graphene.Int()

class UnidadContableConnection(PaginatedType):
    items = graphene.List(UnidadContableType)

class DepartamentoConnection(graphene.ObjectType):
    items = graphene.List(DepartamentoType)

# =====================================================
#  QUERIES
# =====================================================

class CodificadoresQuery(graphene.ObjectType):
    departamentos = graphene.Field(
        DepartamentoConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        centro_id=graphene.ID(),
        centroActivo=graphene.Boolean()
    )
    centros_costo = graphene.List(CentroCostoType)

    unidades = graphene.Field(
        UnidadContableConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        codigo=graphene.String(),
        nombre=graphene.String(),
        activo=graphene.Boolean()
    )

    def resolve_departamentos(root, info, page, limit, centro_id=None, centroActivo=None):
        qs = Departamento.objects.select_related("centrocosto")

        if centro_id:
            qs = qs.filter(centrocosto_id=centro_id)

        if centroActivo is not None:
            qs = qs.filter(centrocosto__activo=centroActivo)

        items, total = paginate_queryset(qs, page, limit)
        return DepartamentoConnection(items=items, total_count=total)

    def resolve_centros_costo(root, info):
        return CentroCosto.objects.all()

    def resolve_unidades(root, info, page, limit, codigo=None, nombre=None, activo=None):
        qs = UnidadContable.objects.all()

        if codigo:
            qs = qs.filter(codigo=codigo)

        if nombre:
            qs = qs.filter(nombre__icontains=nombre)

        if activo is not None:
            qs = qs.filter(activo=activo)

        items, total = paginate_queryset(qs, page, limit)
        return UnidadContableConnection(items=items, total_count=total)

# =====================================================
#  MUTATIONS
# =====================================================

class CodificadoresMutation(graphene.ObjectType):
    pass



