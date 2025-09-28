import uuid

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models import Count, F, Value, Case, When
from django.db.models.functions import Now, Concat
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField, TextChoicesField
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from . import ChoiceTiposProd, ChoiceClasesMatPrima, ChoiceCategoriasVit, \
    ChoiceMotivosAjuste, ChoiceTiposDoc, \
    ChoiceConfCentrosElementosOtros


class ObjectsManagerAbstract(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        abstract = True

class DatosCacheManager(models.Manager):
    _cache = None

    def get_cached_data(self):
        return self._cache

    def clear_cache(self):
        self._cache = None

    class Meta:
        abstract = True

# todas las unidades contables de la empresa
class UnidadContable(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=10, verbose_name=_("Code"))
    nombre = models.CharField(unique=True, max_length=30, verbose_name=_("Name"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    is_empresa = models.BooleanField(default=False, verbose_name=_("Is Company"))
    is_comercializadora = models.BooleanField(default=False, verbose_name=_("Is Commercial"))

    class Meta:
        db_table = 'cla_unidadcontable'
        indexes = [
            models.Index(
                fields=[
                    'codigo',
                ]
            ),
        ]
        ordering = ['codigo']
        verbose_name_plural = _('UEBs')
        verbose_name = _('UEB')

    def __str__(self):
        return "%s - %s" % (self.codigo, self.nombre)


class Medida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=6, verbose_name=_("U.M"))
    descripcion = models.CharField(unique=True, max_length=50, verbose_name=_("Description"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_medida'
        indexes = [
            models.Index(
                fields=[
                    'clave',
                    'descripcion',
                ]
            ),
        ]
        ordering = ['clave', 'descripcion']
        verbose_name_plural = _('Measurement units')
        verbose_name = _('Unit of measurement')

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion)


class MedidaConversion(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=6, db_comment='Factor de conversión',
                                            verbose_name=_("Convertion Factor"),
                                            validators=[MinValueValidator(0.000001, message=_(
                                                'The value must be greater than 0'))])
    medidao = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_origen',
                                db_comment='Medida origen de la conversión',
                                verbose_name=_("Origin Measure"))
    medidad = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_destino',
                                db_comment='Medida destino de la conversión',
                                verbose_name=_("Destination Measure"))

    class Meta:
        db_table = 'cla_medidaconversion'
        indexes = [
            models.Index(
                fields=[
                    'medidao',
                    'medidad',
                ]
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['medidao', 'medidad'],
                name='unique_medidaconversion_medidao_medidad'
            ),
        ]
        ordering = ['medidao__descripcion']
        verbose_name_plural = _('Convert measurement units')
        verbose_name = _('Convert unit of measurement')

    def __str__(self):
        return "%s | %s" % (self.medidao, self.medidad) if self.factor_conversion else ''


class Cuenta(MPTTModel, ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_niv = models.IntegerField()
    posicion = models.IntegerField()
    clave = models.CharField(unique=True, max_length=100)
    clavenivel = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000, verbose_name=_("Description"))
    activa = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    objects = models.Manager()
    tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['clave']

    class Meta:
        db_table = 'cla_cuenta'
        indexes = [
            models.Index(
                fields=[
                    'clave',
                ]
            ),
        ]
        ordering = ['clave', 'posicion']
        verbose_name_plural = _('Accounts')
        verbose_name = _('Account')

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion) if self.clave else ''


class CentroCosto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=50, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=255,
                                   verbose_name=_("Description"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_centrocosto'
        indexes = [
            models.Index(
                fields=[
                    'clave', 'descripcion'
                ]
            ),
        ]
        ordering = ['descripcion', 'clave']
        verbose_name_plural = _('Centers of cost')
        verbose_name = _('Cost center')

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion)


class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True, choices=ChoiceTiposProd.CHOICE_TIPOS_PROD, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)
    orden = models.SmallIntegerField(default=1)
    contabilizacion = models.CharField(max_length=10, verbose_name='Elemento a contabilizar en Transf. Externas',
                                       blank=True, null=True)

    contabilizacion = models.CharField(
        max_length=10,  # Ajusta la longitud máxima según tus necesidades
        verbose_name='Elemento a contabilizar en Transf. Externas',
        blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',  # Acepta solo dígitos (0-9)
                message='Este campo solo puede contener dígitos.',
                code='invalid_number'
            )
        ]
    )

    class Meta:
        db_table = 'cla_tipoproducto'
        ordering = ['orden', 'descripcion']

    def __str__(self):
        return ChoiceTiposProd.CHOICE_TIPOS_PROD[self.id]


class EstadoProducto(models.IntegerChoices):
    BUENO = 1, 'Bueno'
    DEFICIENTE = 2, 'Deficiente'
    RECHAZO = 3, 'Rechazo'


class ClaseMateriaPrima(models.Model):
    id = models.AutoField(primary_key=True, choices=ChoiceClasesMatPrima.CHOICE_CLASES, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)
    capote_fortaleza = models.CharField(max_length=1)

    class Meta:
        db_table = 'cla_clasemateriaprima'
        ordering = ['descripcion']

    def __str__(self):
        return self.descripcion


class CategoriaVitola(models.Model):
    id = models.AutoField(primary_key=True, choices=ChoiceCategoriasVit.CHOICE_CATEGORIAS, editable=False, )
    descripcion = models.CharField(unique=True, max_length=50)
    orden = models.IntegerField(unique=True)

    class Meta:
        db_table = 'cla_categoriavitola'
        ordering = ['orden']

    def __str__(self):
        return "%s" % (self.descripcion)


class ProductoFlujo(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=50, verbose_name=_("Code"))
    descripcion = models.CharField(max_length=400, verbose_name=_("Description"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='productoflujo_medida',
                               verbose_name="U.M")
    tipoproducto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, related_name='productoflujo_tipo',
                                     verbose_name=_("Product Type"))
    precio_lop = models.DecimalField(max_digits=10, decimal_places=4,
                                     db_comment='Precio según Listado Oficial de Precio',
                                     verbose_name=_("Precio LOP"), default=0.0000,
                                     validators=[MinValueValidator(0.0000, message=_('El valor debe ser >= 0'))])
    rendimientocapa = models.IntegerField(db_comment='Rendimiento de la capa x millar',
                                          verbose_name=_("Rendimiento x Millar"), default=0,
                                          validators=[MinValueValidator(0, message=_('El valor debe ser >= 0'))])
    vitolas = models.ManyToManyField(CategoriaVitola, related_name='capas_categvitolas',
                                     verbose_name="Vitolas")

    class Meta:
        db_table = 'cla_productoflujo'
        ordering = ['tipoproducto', 'descripcion']

    def __str__(self):
        return "%s | %s" % (self.codigo, self.descripcion)

    @property
    def get_clasemateriaprima(self):
        return None if self.tipoproducto.pk != ChoiceTiposProd.MATERIAPRIMA else self.productoflujoclase_producto.get().clasemateriaprima


class ProductoFlujoClase(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clasemateriaprima = models.ForeignKey(ClaseMateriaPrima, on_delete=models.PROTECT,
                                          related_name='productosflujoclase_clasemateriaprima')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujoclase_producto')

    class Meta:
        db_table = 'cla_productoflujoclase'

    def __str__(self):
        return self.clasemateriaprima.descripcion


class Destino(models.TextChoices):
    CONSUMONACIONAL = 'C', 'Consumo Nacional'
    EXPORTACION = 'E', 'Exportación'


class ProductoFlujoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destino = TextChoicesField(choices_enum=Destino,
                               verbose_name=_("Destination"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE,
                                 related_name='productoflujodestino_producto')

    class Meta:
        db_table = 'cla_productoflujodestino'


class ProductoFlujoCuenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='productoflujocuenta_cuenta')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujocuenta_producto')

    class Meta:
        db_table = 'cla_productoflujocuenta'


class TipoVitola(models.IntegerChoices):
    PICADURA = 1, 'Picadura'
    HOJA = 2, 'Hoja'


class Vitola(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diametro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                   verbose_name=_("Diameter"))
    longitud = models.IntegerField(default=0, verbose_name=_("Length"))
    destino = TextChoicesField(choices_enum=Destino,
                               verbose_name=_("Destination"))
    cepo = models.IntegerField(default=0)
    categoriavitola = models.ForeignKey(CategoriaVitola, on_delete=models.PROTECT, related_name='vitola_categotia', verbose_name=_("Categoría"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='vitola_producto')
    tipovitola = IntegerChoicesField(choices_enum=TipoVitola, verbose_name=_("Type"))
    capa = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='vitola_productocapa')
    pesada = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='vitola_productopesada')

    class Meta:
        db_table = 'cla_vitola'
        ordering = ['destino', 'categoriavitola', 'producto__descripcion']

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.diametro else ''

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.producto.delete()
            self.capa.delete()
            self.pesada.delete()

    @property
    def get_codigo(self):
        return self.producto.codigo

    @property
    def get_descripcion(self):
        return self.producto.descripcion

    @property
    def get_um(self):
        return self.producto.um

    @property
    def get_productoactivo(self):
        return self.producto.activo


class MarcaSalida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=5, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=128, verbose_name=_("Description"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_marcasalida'
        ordering = ['descripcion']

    def __str__(self):
        return "%s | %s" % (self.codigo, self.descripcion)


class LineaSalida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envase = models.IntegerField(default=0, verbose_name=_("Package"))
    norma_embalaje = models.IntegerField(default=0,
                                         verbose_name=_("Packaging Standard"))
    vol_cajam3 = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Box Volume M3"))
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Gross Weight"))
    peso_neto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                    verbose_name=_("Net Weight"))
    peso_legal = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Legal Weight"))
    marcasalida = models.ForeignKey(MarcaSalida, on_delete=models.PROTECT, related_name='lineasalida_marcasalida',
                                    verbose_name=_("Starting Mark"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='lineasalida_producto')
    vitola = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='lineasalida_vitola',
                               verbose_name="Vitola")

    class Meta:
        db_table = 'cla_lineasalida'
        ordering = ['producto__descripcion']

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.envase else ''

    @property
    def get_productoactivo(self):
        return self.producto.activo


class TipoProductoDepartamento(models.IntegerChoices):
    MATERIAPRIMA = 1, 'Materia Prima'  #la materia prima es capote, fortaleza y picadura
    MANOJOS = 2, 'Manojos'
    CAPASINCLASIFICAR = 3, 'Capa sin Clasificar'
    CAPACLASIFICADA = 4, 'Capa Clasificada'
    PESADA = 5, 'Pesadas'
    LINEASINTERMINAR = 6, 'Linea sin Terminar'
    LINEASALIDA = 7, 'Linea de Salida'
    VITOLA = 8, 'Vitola'

class TipoActividadDepartamento(models.IntegerChoices):
    PREPMATERIAPRIMA = 1, 'Preparación Materia Prima'
    CLASIFICADODEHOJAS = 2, 'Clasificado de Hojas'
    DESPACHO = 3, 'Despacho'
    TORCIDO = 4, 'Torcido'

class ActividadDepartamento(models.Model):
    id = models.IntegerField(choices=TipoActividadDepartamento.choices, primary_key=True)

    class Meta:
        db_table = 'cla_actividaddepartamento'

    def __str__(self):
        return TipoActividadDepartamento(self.pk).label

class ProductoDepartamento(models.Model):
    id = models.IntegerField(choices=TipoProductoDepartamento.choices, primary_key=True)

    class Meta:
        db_table = 'cla_productodepartamento'

    def __str__(self):
        return TipoProductoDepartamento(self.pk).label


class OperacionDocumento(models.TextChoices):
    ENTRADA = 'E', 'Entrada'
    SALIDA = 'S', 'Salida'

class TipoDocumentoCacheManager(DatosCacheManager):
    def get_cached_data(self):
        if self._cache is None:
            self._cache = self.get_tipodocumento_prefijos()
        return self._cache

    def get_tipodocumento_prefijos(self):
        tipodoc = TipoDocumento.objects.all()
        return {item.id: {'prefijo': item.prefijo, 'generado': item.generado, 'operacion': item.operacion} for item in
                tipodoc}

class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True, choices=ChoiceTiposDoc.CHOICE_TIPOS_DOC, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128)
    operacion = TextChoicesField(choices_enum=OperacionDocumento,
                                 db_comment='Operación de Entrada (E) o Salida (S)',
                                 verbose_name=_("Operación"))
    generado = models.BooleanField(default=False, db_comment='Si se genera automáticamente',
                                   verbose_name=_("Generado"))
    prefijo = models.CharField(max_length=5, db_comment='Prefijo para el número de control', null=True, blank=True)
    objects = TipoDocumentoCacheManager()

    class Meta:
        db_table = 'cla_tipodocumento'
        ordering = ['operacion', 'descripcion']

    def __str__(self):
        return self.descripcion

class Departamento(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=125, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=125, verbose_name=_("Description"))
    centrocosto = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, related_name='departamento_centrocosto',
                                    verbose_name=_("Cost Center"))
    unidadcontable = models.ManyToManyField(UnidadContable, related_name='departamento_unidadcontable',
                                            verbose_name="UEB")
    relaciondepartamento = models.ManyToManyField('self',
                                                  blank=True,
                                                  verbose_name=_("Destination Department"))
    departamentoproductoentrada = models.ManyToManyField(ProductoDepartamento,
                                                         blank=True,
                                                         related_name='departamentoproductoentrada_producto',
                                                         verbose_name=_("Productos de Entrada"))
    departamentoproductosalida = models.ManyToManyField(ProductoDepartamento,
                                                  blank=True,
                                                  related_name='departamentoproductosalida_producto',
                                                  verbose_name=_("Producto a Producir"))

    departamentoactividad = models.ManyToManyField(ActividadDepartamento,
                                                        blank=True,
                                                        related_name='departamento_actividad',
                                                        verbose_name=_("Actividad"))

    departamentodocumentosentrada = models.ManyToManyField(TipoDocumento,
                                                   blank=True,
                                                   related_name='departamento_documentosentrada',
                                                   verbose_name=_("Documentos de Entrada"))

    departamentodocumentossalida = models.ManyToManyField(TipoDocumento,
                                                   blank=True,
                                                   related_name='departamento_documentossalida',
                                                   verbose_name=_("Documentos de Salida"))

    class Meta:
        db_table = 'cla_departamento'
        ordering = ('codigo',)
        indexes = [
            models.Index(
                fields=[
                    'codigo',
                    'descripcion',
                    'centrocosto'
                ]
            ),
        ]
        ordering = ['codigo']
        verbose_name_plural = _('Departments')
        verbose_name = _('Department')

    def __str__(self):
        return "%s | %s" % (self.codigo, self.descripcion)

    def __name__(self):
        return 'Departamento'

    def inicializado(self, ueb):
        return False if not self else False if not self.fechainicio_departamento.filter(ueb=ueb) else True

class TiposNormas(models.IntegerChoices):
    PESADA = 1, 'Pesada'
    MATERIAPRIMA = 2, 'Materia Prima'
    LINEASALIDA = 4, 'Línea de Salida'
    VITOLA = 5, 'Vitola'
    HABILITADOS = 7, 'Habilitados'

class NormaConsumo(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"))
    activa = models.BooleanField(default=False, verbose_name=_("Active"))
    confirmada = models.BooleanField(default=False, verbose_name=_("Confirmada"))
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Crate at"))
    fecha = models.DateField(verbose_name=_("Date"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='normaconsumo_medida',
                               verbose_name="U.M")
    producto = models.ForeignKey(ProductoFlujo, models.PROTECT, related_name='normaconsumo_producto',
                                 verbose_name=_("Product"))
    tiponorma = IntegerChoicesField(choices_enum=TiposNormas, verbose_name=_("Tipo Norma"))

    class Meta:
        db_table = 'cla_normaconsumo'
        ordering = ['producto__tipoproducto', 'producto__descripcion', 'confirmada', '-activa']
        verbose_name_plural = _('Normas de Consumo')
        verbose_name = _('Norma de Consumo')

    def __str__(self):
        return "%s %s | %s" % (
            self.fecha,
            self.producto.codigo,
            self.producto.descripcion
        ) if self.producto_id else ''


class NormaconsumoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    norma_ramal = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                      verbose_name=_("Ramal Norm"))
    norma_empresarial = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                            verbose_name=_("Enterprise Norm"))
    operativo = models.BooleanField(default=False, db_comment='Si el producto es operativo o no',
                                    verbose_name=_("Operational"))
    normaconsumo = models.ForeignKey(NormaConsumo, on_delete=models.CASCADE,
                                     related_name='normaconsumodetalle_normaconsumo')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='normaconsumodetalle_producto',
                                 verbose_name=_("Product"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='normaconsumodetalle_medida',
                               verbose_name="U.M")

    class Meta:
        db_table = 'cla_normaconsumodetalle'
        constraints = [
            models.UniqueConstraint(
                fields=['normaconsumo', 'producto'],
                name='unique_normaconsumodetalle_normaconsumo_producto'
            ),
        ]
        verbose_name_plural = _('Detalles Norma de Consumo')
        verbose_name = _('Detalles Norma de Consumo')

    def __str__(self):
        return "%s | %s de la norma %s" % (
            self.producto.codigo,
            self.producto.descripcion,
            self.normaconsumo.__str__()
        )


class NormaConsumoGroupedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values(
            idprod=F('producto__id'),
            Producto=Concat(F('producto__codigo'), Value(' | '), F('producto__descripcion')),
        ).annotate(Cantidad_Normas=Count('producto'),
                   Tipo_Norma=Case(
                       When(tiponorma=1, then=Value(TiposNormas.PESADA.label)),
                       When(tiponorma=2, then=Value(TiposNormas.MATERIAPRIMA.label)),
                       When(tiponorma=4, then=Value(TiposNormas.LINEASALIDA.label)),
                       When(tiponorma=5, then=Value(TiposNormas.VITOLA.label)),
                       When(tiponorma=7, then=Value(TiposNormas.HABILITADOS.label)),
                   ), ).order_by('tiponorma','producto__descripcion')


class NormaConsumoGrouped(NormaConsumo):
    objects = NormaConsumoGroupedManager()

    class Meta:
        proxy = True
        ordering = ['producto__tipoproducto', 'producto__descripcion', 'fecha']
        verbose_name_plural = _('Normas de Consumo')
        verbose_name = _('Norma de Consumo')

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''


class MotivoAjuste(ObjectsManagerAbstract):
    id = models.AutoField(primary_key=True, choices=ChoiceMotivosAjuste.CHOICE_MOTIVOS_AJUSTE, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128, verbose_name=_("Description"))
    aumento = models.BooleanField(default=False, db_comment='Ajuste de aumento True en otro caso False',
                                  verbose_name=_("Increase"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_motivoajuste'
        ordering = ['aumento', 'descripcion']

    def __str__(self):
        return self.descripcion

class TipoNumeroDoc(models.IntegerChoices):
    NUMERO_CONSECUTIVO = 1, "Número Consecutivo"
    NUMERO_CONTROL = 2, "Número de Control"

class ConfigNumero(models.IntegerChoices):
    DEPARTAMENTO = 1, 'Por departamento'
    UNICO = 2, 'Unico en el sistema'

class NumeracionDocumentosCacheManager(DatosCacheManager):
    def get_cached_data(self):
        if self._cache is None:
            self._cache = self.get_configuracion_numeracion()
        return self._cache

    def get_configuracion_numeracion(self):
        numeracion = self.all()
        list_dicc = [objeto.to_dict() for objeto in numeracion]
        if list_dicc:
            dicc = {item["tiponumero"]: item for item in list_dicc}
            return dicc[TipoNumeroDoc.NUMERO_CONSECUTIVO], dicc[TipoNumeroDoc.NUMERO_CONTROL]
        return {}, {}


class NumeracionDocumentos(ObjectsManagerAbstract):
    id = models.AutoField(primary_key=True, choices=TipoNumeroDoc, verbose_name=_("Tipo de Número"))
    sistema = models.BooleanField(default=False, db_comment='Si es controlado por el sistema',
                                  verbose_name=_("Controlada por el sistema"))
    pordepartamento = models.BooleanField(default=False, db_comment='Si el número es por departamento',
                                       verbose_name=_("Por Departmento"))
    prefijo = models.BooleanField(default=False,
                                  db_comment='Si el número de documento va a contener un prefijo',
                                  verbose_name=_("Usar Prefijo"))
    objects_cache = NumeracionDocumentosCacheManager()

    class Meta:
        db_table = 'cla_numeraciondocumentos'
        ordering = ['id']

    def to_dict(self):
        mess = 'Ya el ' + (TipoNumeroDoc.NUMERO_CONSECUTIVO.label
                                  if self.id == TipoNumeroDoc.NUMERO_CONSECUTIVO
                                  else TipoNumeroDoc.NUMERO_CONTROL.label) + ' existe '
        peri = ' en el año' if self.id == TipoNumeroDoc.NUMERO_CONTROL else ' en el mes'

        if self.pordepartamento:
            mess = mess + 'para el Departamento'
        mess = mess + peri

        return {
            "tiponumero": self.id,
            'sistema': self.sistema,
            'departamento': self.pordepartamento,
            'prefijo': self.prefijo,
            'mensaje_error': mess
        }


# Documento que se va a configurar la cuenta para su contabilizacion
# class TipoDocumentoCuentaAbstract(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,
#                                   verbose_name=_("Document Type"))
#
#     class Meta:
#         abstract = True


# Se configura la cuenta de los documentos que la llevan,
class TipoDocumentoCuenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,
                                  verbose_name=_("Document Type"))
    cuenta_debe_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                        related_name='tipodocumentocuenta_cuenta_debe_exp',
                                        verbose_name=_("Debit Count Exp"))
    cuenta_debe_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                       related_name='tipodocumentocuenta_cuenta_debe_cn',
                                       verbose_name=_("Debit Count CN"))
    cuenta_haber_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                         related_name='tipodocumentocuenta_cuenta_haber_exp',
                                         verbose_name=_("Credit Count Exp"))
    cuenta_haber_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                        related_name='tipodocumentocuenta_cuenta_haber_cn',
                                        verbose_name=_("Credit Count CN"))

    class Meta:
        db_table = 'cla_tipodocumentocuenta'


# Se va a configurar por unidad contable y los departamentos de la unidad contable
# class TipoDocumentoCuentaTransfExterna(TipoDocumentoCuentaAbstract):
#     unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
#                                        related_name='tipodocumentocuentatransfexterna_unidadcontable',
#                                        db_comment='Esta es la unidad contable para la que se va a configurar el documento',
#                                        verbose_name="UEB")
#     departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
#                                      db_comment='Dpto de la unidad contable para la que se va a configurar el documento',
#                                      related_name='tipodocumentocuentatransfexterna_departamento',
#                                      verbose_name=_("Department"))
#
#     class Meta:
#         db_table = 'cla_tipodocumentocuentatransfexterna'
#
#
# # se configura la cuenta por unidad contable que realiza o recibe la transf.
# # en dependencia del tipo de documento
# class TipoDocumentoCuentaTransfExternaUEB(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     idtipodocumentocuentatransfexterna = models.ForeignKey(TipoDocumentoCuentaTransfExterna, on_delete=models.CASCADE,
#                                                            related_name='tipodocumentocuentatransfexternadpto_ipodocumentocuentatransfexterna')
#     unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
#                                        related_name='tipodocumentocuentatransfexternadpto_unidadcontable',
#                                        db_comment='Unidad contab que recibe o envía la transf, según el tipo de documento')
#     cuenta_debe_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
#                                         related_name='tipodocumentocuentatransfexternadpto_cuenta_debe_exp')
#     cuenta_debe_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
#                                        related_name='tipodocumentocuentatransfexternadpto_cuenta_debe_cn')
#     cuenta_haber_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
#                                          related_name='tipodocumentocuentatransfexternadpto_cuenta_haber_exp')
#     cuenta_haber_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
#                                         related_name='tipodocumentocuentatransfexternadpto_cuenta_haber_cn')
#
#     class Meta:
#         db_table = 'cla_tipodocumentocuentatransfexternaueb'


# Formato del versat para las cuentas y código de los productos
class FormatoCuentaProducto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=30)
    separador = models.CharField(max_length=1)
    posicion = models.IntegerField()
    longitud = models.IntegerField()
    enuso = models.BooleanField(default=True)


class Meta:
    db_table = 'cla_formatocuentaproducto'
    ordering = ['nombre', 'posicion']


class CambioProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productoo = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujo_origen',
                                  verbose_name=_("Origin Product"))
    productod = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujo_destino',
                                  verbose_name=_("Destination Product"))

    class Meta:
        db_table = 'cla_cambioproducto'
        constraints = [
            models.UniqueConstraint(
                fields=['productoo', 'productod'],
                name='unique_cambioproducto_productoo_productod'
            ),
        ]
        ordering = ['productoo__descripcion']

        indexes = [
            models.Index(
                fields=[
                    'productoo',
                    'productod',
                ]
            ),
        ]

        verbose_name_plural = "Cambio de Productos"
        verbose_name = "Cambio de Producto"

    def __str__(self):
        return '' if not self.productoo_id else "%s | %s" % (self.productoo, self.productod)


# Configurar centros de costos, elementos de gastos
# contiene los campos
# clave: Clave que identifica que se configura (CentrosCosto, Elementos)
# descripcion: Elemento que se configura
# valor: El valor de la configuración
class ConfCentrosElementosOtros(ObjectsManagerAbstract):
    id = models.AutoField(primary_key=True, choices=ChoiceConfCentrosElementosOtros.CHOICE_CONF_CC_ELEM_OTROS,
                          editable=False, )
    clave = models.CharField(unique=True, max_length=80, verbose_name="Configurar Centros y Elementos")

    class Meta:
        db_table = 'cla_confcentroselementosotros'
        ordering = ['clave']

    def __str__(self):
        return self.clave


class ConfCentrosElementosOtrosDetalle(ObjectsManagerAbstract):
    id = models.IntegerField(primary_key=True, editable=False, )
    clave = models.ForeignKey(ConfCentrosElementosOtros, on_delete=models.PROTECT, related_name='confccelem_clave',
                              verbose_name="Configurar")
    descripcion = models.CharField(max_length=250)
    valor = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'cla_confcentroselementosotrosdetalle'
        ordering = ['clave__clave', 'descripcion']
        constraints = [
            models.UniqueConstraint(
                fields=['clave', 'valor'],
                name='unique_confcentroselementosotrosdetalle_clave_valor'
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    'clave',
                    'descripcion',
                ]
            ),
        ]

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion)


class ConfCentrosElementosOtrosDetalleGroupedManager(models.Manager):
    def get_queryset(self):
        obj = super().get_queryset().values(Clave=F('clave__clave'),
                                            Clave_id=F('clave__id')).annotate(
            Elementos=Count('clave')).order_by('clave__clave')
        return obj


class ConfCentrosElementosOtrosDetalleGrouped(ConfCentrosElementosOtrosDetalle):
    objects = ConfCentrosElementosOtrosDetalleGroupedManager()

    class Meta:
        proxy = True
        ordering = ['clave__clave', 'descripcion']


class ProductsCapasClaPesadasManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(tipoproducto=ChoiceTiposProd.PESADA) |
            Q(productoflujoclase_producto__clasemateriaprima=ChoiceClasesMatPrima.CAPACLASIFICADA))


class ProductsCapasClaPesadas(ProductoFlujo):
    objects = ProductsCapasClaPesadasManager()

    class Meta:
        proxy = True
        ordering = ['tipoproducto', 'descripcion']


# Costos
# Fichas de costo
class FichaCostoFilas(MPTTModel, ObjectsManagerAbstract):
    id = models.AutoField(primary_key=True)
    fila = models.CharField(max_length=8, unique=True)
    descripcion = models.CharField(max_length=150)
    encabezado = models.BooleanField(default=False,
                                     db_comment='Valor True si tiene descendientes y su valor '
                                                'es la suma de los hijos los valores de sus hijos. '
                                                'Ejemplo Fila 1 es encabezado si exiten filas 1.1, 1.2, 1.n '
                                                'y el valor de Fila 1 es la suma de sus hijos')
    salario = models.BooleanField(default=False, db_comment='Si el concepto constituye salario')
    vacaciones = models.BooleanField(default=False,
                                     db_comment='Si es vacaciones y se relaciona con el concepto salario '
                                                'para calcularlo como el 9.09 del salario')
    desglosado = models.BooleanField(default=False,
                                     db_comment='Si el concepto es resultado de los desgloses establecidos: Salario, '
                                                'Materia Prima y Materiales, Gastos Materia Prima Tabaco')
    calculado = models.BooleanField(default=False,
                                    db_comment='Si su valor depende de la suma de otras filas del encabezado')
    filasasumar = models.ManyToManyField('self',
                                         blank=True,
                                         symmetrical=False,
                                         verbose_name=_("Filas a sumar"))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    padre = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        db_table = 'cla_fichacostofilas'
        ordering = ['fila']

        indexes = [
            models.Index(
                fields=[
                    'fila',
                    'descripcion',
                ]
            ),
        ]

    def __str__(self):
        return "%s - %s" % (self.fila, self.descripcion)

    def descripcion_completa(self):
        """Devuelve la descripción completa para filas calculadas, incluyendo las filas a sumar."""
        if self.calculado:
            # Obtener las filas a sumar y concatenarlas
            filas_a_sumar = self.filasasumar.values_list('fila', flat=True)
            filas_concatenadas = "+".join(filas_a_sumar)
            return f"{self.descripcion} ({filas_concatenadas})"
        # Si no es calculado, devuelve la descripción normal
        return f"{self.descripcion}"


class VinculoCargoProduccion(models.IntegerChoices):
    DIRECTO = 1, 'Directo'
    INDIRECTOPRODUCCION = 2, 'Indirecto Producción'
    INDIRECTO = 3, 'Indirecto'


class GrupoEscalaCargo(ObjectsManagerAbstract):
    id = models.SmallIntegerField(primary_key=True, editable=False, )
    grupo = models.CharField(unique=True, max_length=10)
    salario = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Salario',
                                  verbose_name=_("Salario"),
                                  validators=[MinValueValidator(0.01, message=_(
                                      'The value must be greater than 0'))])

    class Meta:
        db_table = 'cla_grupoescalacargo'

    def __str__(self):
        return "%s | %s" % (self.grupo, self.salario)


class ClasificadorCargos(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=5)
    descripcion = models.CharField(unique=True, max_length=160)
    grupo = models.ForeignKey(GrupoEscalaCargo, on_delete=models.PROTECT, related_name='cargo_grupo',
                              verbose_name="Grupo Escala")
    actividad = TextChoicesField(choices_enum=Destino, verbose_name=_("Actividad"))
    vinculo_produccion = IntegerChoicesField(choices_enum=VinculoCargoProduccion,
                                             db_comment='Directo (1), Indirecto Producción (2), Indirecto (3)',
                                             verbose_name=_("Vinculo Producción"),
                                             default=VinculoCargoProduccion.DIRECTO)

    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    nr_media = models.IntegerField(default=0, verbose_name=_("Norma Rendimiento Media"),
                                   db_comment='Norma de Rendimiento Media para los trabajadores directos')
    norma_tiempo = models.DecimalField(max_digits=10, decimal_places=4, default=0,
                                       verbose_name=_("Norma de tiempo (hrs)"),
                                       validators=[MinValueValidator(0.0000, message=_(
                                           'El valor debe ser >= 0'))]
                                       )
    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    unidadcontable = models.ManyToManyField(UnidadContable, related_name='cargo_unidadcontable',
                                            verbose_name="UEB")

    class Meta:
        db_table = 'cla_clasificadorcargos'

        indexes = [
            models.Index(
                fields=[
                    'codigo',
                    'descripcion',
                    'grupo',
                    'actividad',
                    'vinculo_produccion'
                ]
            ),
        ]

    def __str__(self):
        return "%s | %s" % (
            self.codigo,
            self.descripcion
        )

    @property
    def salario(self):
        return self.grupo.salario


class FechaInicio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='fechainicio_departamento',
                                     verbose_name=_("Department"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='fechainicio_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_fechainicio'
        constraints = [
            models.UniqueConstraint(
                fields=['departamento', 'ueb'],
                name='unique_fechainicio_departamento_ueb'
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    'departamento',
                    'ueb'
                ]
            ),
        ]

class ConfiguracionesGenCacheManager(DatosCacheManager):
    def get_cached_data(self):
        if self._cache is None:
            self._cache = self.get_otras_configuraciones()
        return self._cache

    def get_otras_configuraciones(self):
        numeracion = ConfiguracionesGen.objects.all()
        list_dicc = [objeto.to_dict() for objeto in numeracion]
        return {item["clave"]: item for item in list_dicc}

class ConfiguracionesGen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=100, verbose_name=_("Clave"))
    activo = models.BooleanField(default=True, verbose_name=_("Activo"))
    objects = ConfiguracionesGenCacheManager()

    class Meta:
        db_table = 'cla_configuracionesgen'
        indexes = [
            models.Index(
                fields=[
                    'clave',
                ]
            ),
        ]
        verbose_name_plural = _('Configuraciones Generales')
        verbose_name = _('Configuración General')

    def __str__(self):
        return self.clave

    def to_dict(self):
        return {
            "clave": self.clave,
            'activo': self.activo,
        }

class CostoVarGlobales(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descripcion = models.CharField(unique=True, max_length=125, verbose_name=_("Description"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_costovarglobales'
        ordering = ['descripcion']
        verbose_name_plural = _('Variables Globales del Costo')
        verbose_name = _('Variable Global del Costo')

    def __str__(self):
        return self.descripcion





