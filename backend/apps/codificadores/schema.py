import graphene
from graphene_django import DjangoObjectType
from .models import *
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

class MedidaType(DjangoObjectType):
    class Meta:
        model = Medida
        fields = ("id", "clave", "descripcion", "activa")


class MedidaConversionType(DjangoObjectType):
    class Meta:
        model = MedidaConversion
        fields = ("id", "factor_conversion", "medidao", "medidad")

class TipoDocumentoType(DjangoObjectType):
    class Meta:
        model = TipoDocumento
        fields = ("id", "descripcion", "operacion", "generado", "prefijo")

class TipoProductoType(DjangoObjectType):
    class Meta:
        model = TipoProducto
        fields = ("id", "descripcion", "orden", "contabilizacion")

class TipoHabilitacionType(DjangoObjectType):
    class Meta:
        model = TipoHabilitacion
        fields = ("id", "descripcion", "activo")

class MotivoAjusteType(DjangoObjectType):
    class Meta:
        model = MotivoAjuste
        fields = ("id", "descripcion", "aumento", "activo")

class MarcaSalidaType(DjangoObjectType):
    class Meta:
        model = MarcaSalida
        fields = ("id", "codigo", "descripcion", "activa")

# =====================================================
#  CONNECTION
# =====================================================
class PaginatedType(graphene.ObjectType):
    items = graphene.List(graphene.JSONString)
    total_count = graphene.Int()

class UnidadContableConnection(PaginatedType):
    items = graphene.List(UnidadContableType)

class DepartamentoConnection(PaginatedType):
    items = graphene.List(DepartamentoType)

class MedidaConnection(PaginatedType):
    items = graphene.List(MedidaType)

class MedidaConversionConnection(PaginatedType):
    items = graphene.List(MedidaConversionType)

class TipoDocumentoConnection(PaginatedType):
    items = graphene.List(TipoDocumentoType)

class TipoProductoConnection(PaginatedType):
    items = graphene.List(TipoProductoType)

class TipoHabilitacionConnection(PaginatedType):
    items = graphene.List(TipoHabilitacionType)

class MotivoAjusteConnection(PaginatedType):
    items = graphene.List(MotivoAjusteType)

class MarcaSalidaConnection(PaginatedType):
    items = graphene.List(MarcaSalidaType)

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

    medidas = graphene.Field(
        MedidaConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        clave=graphene.String(),
        descripcion=graphene.String(),
        activa=graphene.Boolean()
    )

    medidasconversion = graphene.Field(
        MedidaConversionConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        medidao=graphene.String(),
        medidad=graphene.String(),
    )

    tiposdocumentos = graphene.Field(
        TipoDocumentoConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        descripcion=graphene.String(),
        operacion=graphene.String(),
        prefijo=graphene.String(),
        generado=graphene.Boolean(),
    )

    tiposproductos = graphene.Field(
        TipoProductoConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        descripcion=graphene.String(),
        orden=graphene.Int(),
        contabilizacion=graphene.String(),
    )

    tiposhabilitaciones = graphene.Field(
        TipoHabilitacionConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        descripcion=graphene.String(),
        activo=graphene.Boolean(),
    )

    motivosajuste = graphene.Field(
        MotivoAjusteConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        descripcion=graphene.String(),
        aumento=graphene.Boolean(),
        activo=graphene.Boolean(),
    )

    marcassalida = graphene.Field(
        MarcaSalidaConnection,
        page=graphene.Int(required=True),
        limit=graphene.Int(required=True),
        codigo=graphene.String(),
        descripcion=graphene.String(),
        activa=graphene.Boolean(),
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

    def resolve_medidas(root, info, page, limit, clave=None, descripcion=None, activa=None):
        qs = Medida.objects.all()

        if clave:
            qs = qs.filter(clave=clave)

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        if activa is not None:
            qs = qs.filter(activa=activa)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_medidasconversion(root, info, page, limit, medidao=None, medidad=None):
        qs = MedidaConversion.objects.all()

        if medidao:
            qs = qs.filter(medidao=medidao)

        if medidad:
            qs = qs.filter(medidad=medidad)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_tiposdocumentos(root, info, page, limit, descripcion=None, operacion=None, prefijo=None, generado=None):
        qs = TipoDocumento.objects.all()

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        if operacion:
            qs = qs.filter(operacion=operacion)

        if prefijo:
            qs = qs.filter(prefijo__icontains=prefijo)

        if generado:
            qs = qs.filter(generado=generado)


        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_tiposproductos(root, info, page, limit, descripcion=None):
        qs = TipoProducto.objects.all()

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_tiposhabilitaciones(root, info, page, limit, descripcion=None, activo=None):
        qs = TipoHabilitacion.objects.all()

        if activo:
            qs = qs.filter(activo=activo)

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_motivosajuste(root, info, page, limit, descripcion=None, aumento=None, activo=None):
        qs = MotivoAjuste.objects.all()

        if activo:
            qs = qs.filter(activo=activo)

        if aumento:
            qs = qs.filter(aumento=aumento)

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

    def resolve_marcassalida(root, info, page, limit, codigo=None, descripcion=None, activa=None):
        qs = MarcaSalida.objects.all()

        if activa:
            qs = qs.filter(activa=activa)

        if codigo:
            qs = qs.filter(codigo__icontains=codigo)

        if descripcion:
            qs = qs.filter(descripcion__icontains=descripcion)

        items, total = paginate_queryset(qs, page, limit)
        return MedidaConnection(items=items, total_count=total)

# =====================================================
#  MUTATIONS
# =====================================================

class CodificadoresMutation(graphene.ObjectType):
    pass



