import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import Count, F, Value, Case, When
from django.db.models.functions import Now, Concat
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField, TextChoicesField

from apps.codificadores.models import ObjectsManagerAbstract, ProductoFlujo, FichaCostoFilas, Medida, UnidadContable, \
    CostoVarGlobales, CentroCosto, Destino, ClasificadorCargos, DatosCacheManager
from apps.flujo.utils import ChoiceFechas
from . import CHOICES_MESES


class TipoFichaCosto(models.IntegerChoices):
    TORCIDO = 1, 'Torcido'
    TERMINADO = 2, 'Terminado'


class FichaCostoGroupedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values(
            idprod=F('producto__id'),
            Producto=Concat(F('producto__codigo'), Value(' | '), F('producto__descripcion')),
        ).annotate(Cantidad_Fichas=Count('producto'),
                   Tipo_Ficha=Case(
                       When(tipoficha=1, then=Value(TipoFichaCosto.TORCIDO.label)),
                       When(tipoficha=2, then=Value(TipoFichaCosto.TERMINADO.label)),
                   ),
                   ).order_by('tipoficha', 'producto__descripcion')

# Fichas de costo
class FichaCostoProducto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Crate at"))
    fecha = models.DateField(verbose_name=_("Date"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='productoflujo_ficha',
                                 verbose_name=_("Product"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='ficha_medida',
                           verbose_name=_("U.M"))
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0, message=_(
        'The value must be greater than 0'))])
    tasa = models.DecimalField(max_digits=10, decimal_places=6, db_comment='Tasa',
                               verbose_name=_("Tasa"), default=0.0)
    activa = models.BooleanField(default=False, verbose_name=_("Active"))
    confirmada = models.BooleanField(default=False, verbose_name=_("Confirmada"))
    tipoficha = IntegerChoicesField(choices_enum=TipoFichaCosto, verbose_name="Tipo Ficha")

    class Meta:
        db_table = 'cos_fichacostoproducto'
        ordering = ['fecha', 'producto', 'confirmada', '-activa']

        indexes = [
            models.Index(
                fields=[
                    'producto',
                    'activa',
                ]
            ),
        ]

    def __str__(self):
        return "%s %s | %s" % (
            self.fecha,
            self.producto.codigo,
            self.producto.descripcion
        ) if self.cantidad else ''


class FichaCostoProductoFilas(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fichacostoproducto = models.ForeignKey(FichaCostoProducto, on_delete=models.CASCADE,
                                           related_name='fichacostoproducto_ficha',
                                           verbose_name=_("Ficha de Costo"))
    fila = models.ForeignKey(FichaCostoFilas, on_delete=models.PROTECT,
                             related_name='fichacostoproducto_fila')
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                verbose_name=_("Costo"))

    class Meta:
        db_table = 'cos_fichacostoproductofila'
        ordering = ['fila']
        constraints = [
            models.UniqueConstraint(
                fields=['fila', 'fichacostoproducto'],
                name='unique_fichacostoproductofila_fila_fichacostoproducto'
            ),
        ]

    def save(self, *args, **kwargs):
        # Verificar si la instancia ya existe en la base de datos
        if self.pk:
            # Obtener el valor actual de la base de datos
            original = FichaCostoProductoFilas.objects.filter(pk=self.pk)
            # Verificar si el valor de 'costo' ha cambiado
            if original.exists() and original.first().costo != self.costo:
                # Guardar el nuevo valor y ejecutar las actualizaciones
                super().save(*args, **kwargs)
                self.actualizar_costos_dependientes()
        super().save(*args, **kwargs)


    def actualizar_costos_dependientes(self):
        """Actualiza el costo en los encabezados y en las filas calculadas dependientes."""

        # Actualiza los padres ascendentes si son encabezado
        self.actualizar_encabezados_ascendentes(self.fila)

        # Actualiza las filas calculadas dependientes
        filas_calculadas = FichaCostoFilas.objects.filter(filasasumar=self.fila.parent, calculado=True)
        for fila_calculada in filas_calculadas:
            nuevo_costo_calculado = FichaCostoProductoFilas.objects.filter(
                fichacostoproducto=self.fichacostoproducto,
                fila__in=fila_calculada.filasasumar.all()
            ).aggregate(models.Sum('costo'))['costo__sum'] or 0

            FichaCostoProductoFilas.objects.update_or_create(
                fichacostoproducto=self.fichacostoproducto,
                fila=fila_calculada,
                defaults={'costo': nuevo_costo_calculado}
            )

    def actualizar_encabezados_ascendentes(self, fila):
        """Recursivamente actualiza los costos en los encabezados ascendentes."""
        if fila.parent and fila.parent.encabezado:
            nuevo_costo = FichaCostoProductoFilas.objects.filter(
                fichacostoproducto=self.fichacostoproducto,
                fila__parent=fila.parent
            ).aggregate(models.Sum('costo'))['costo__sum'] or 0

            FichaCostoProductoFilas.objects.update_or_create(
                fichacostoproducto=self.fichacostoproducto,
                fila=fila.parent,
                defaults={'costo': nuevo_costo}
            )
            # Llamada recursiva para actualizar los padres
            self.actualizar_encabezados_ascendentes(fila.parent)

class FichaCostoProductoFilaCapas(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fila = models.OneToOneField(FichaCostoProductoFilas, on_delete=models.CASCADE,
                             related_name='desglosecapas_fila',
                             verbose_name=_("Fila"))
    costo_base_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                           db_default=0.00,
                                           verbose_name=_("Norma Costo Base"))
    costo_base_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                            db_default=0.00,
                                            verbose_name=_("Precio Costo Base"))
    costo_base_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                             db_default=0.00,
                                             verbose_name=_("Importe Costo Base"))

    costo_propuesto_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                                db_default=0.00,
                                                verbose_name=_("Norma Costo Base"))
    costo_propuesto_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                                 db_default=0.00,
                                                 verbose_name=_("Precio Costo Base"))
    costo_propuesto_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                                  db_default=0.00,
                                                  verbose_name=_("Importe Costo Propuesto"))

    class Meta:
        db_table = 'cos_fichacostoproductofilacapas'
        ordering = ['fila']

class FichaCostoProductoFilaDesgloseMPMat(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fila = models.ForeignKey(FichaCostoProductoFilas, on_delete=models.CASCADE,
                             related_name='desglosempmat_fila',
                             verbose_name=_("Fila"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='filadesglose_producto',
                                 verbose_name=_("Product"))
    costo_base_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                           db_default=0.00,
                                           verbose_name=_("Norma Costo Base"))
    costo_base_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                            db_default=0.00,
                                            verbose_name=_("Precio Costo Base"))
    costo_base_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                             db_default=0.00,
                                             verbose_name=_("Importe Costo Base"))

    costo_propuesto_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                                db_default=0.00,
                                                verbose_name=_("Norma Costo Base"))
    costo_propuesto_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                                 db_default=0.00,
                                                 verbose_name=_("Precio Costo Base"))
    costo_propuesto_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                                  db_default=0.00,
                                                  verbose_name=_("Importe Costo Propuesto"))

    class Meta:
        db_table = 'cos_fichacostoproductofiladesglosempmat'
        ordering = ['fila', 'producto']
        constraints = [
            models.UniqueConstraint(
                fields=['fila', 'producto'],
                name='unique_fichacostoproductofiladesglosempmat_fila_producto'
            ),
        ]

class FichaCostoProductoFilaDesgloseSalario(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fila = models.ForeignKey(FichaCostoProductoFilas, on_delete=models.CASCADE,
                             related_name='desglosesalario_fila',
                             verbose_name=_("Fila"))
    cargo = models.ForeignKey(ClasificadorCargos, on_delete=models.PROTECT, related_name='filadesglose_cargo',
                                 verbose_name=_("Cargo"))
    salario = models.DecimalField(max_digits=10, decimal_places=2, db_comment='Salario',
                                  verbose_name=_("Salario"))
    salario_calculado = models.DecimalField(max_digits=18, decimal_places=2, db_comment='Salario Calculado',
                                  verbose_name=_("Salario Calculado"), default=0.00)

    cantidad = models.IntegerField(default=0, verbose_name=_("Cantidad de Trabajadores"))
    nr_media = models.IntegerField(default=0, verbose_name=_("Norma Rendimiento Media"),
                                   db_comment='Norma de Rendimiento Media para los trabajadores directos')
    norma_tiempo = models.DecimalField(max_digits=10, decimal_places=4, default=0,
                                       verbose_name=_("Norma de tiempo (hrs)"))

    class Meta:
        db_table = 'cos_fichacostoproductofiladesglosesalario'
        ordering = ['fila', 'cargo']
        constraints = [
            models.UniqueConstraint(
                fields=['fila', 'cargo'],
                name='unique_fichacostoproductofiladesglosesalario_fila_salario'
            ),
        ]

    @property
    def gasto_salario(self):
        return round(self.cantidad * self.salario_hora * self.norma_tiempo, 2)

    @property
    def salario_hora(self):
        return round(self.salario_calculado/Decimal('190.6'), 4)

class FichaCostoGrouped(FichaCostoProducto):
    objects = FichaCostoGroupedManager()

    class Meta:
        proxy = True
        verbose_name_plural = _('Fichas de Costo')
        verbose_name = _('Ficha de Costo')

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''


class FechaProcesamientoCostoCacheManager(DatosCacheManager):

    def get_cached_data(self):
        if self._cache is None:
            self._cache = self.get_fechas_procesamiento_costo()
        return self._cache

    @transaction.atomic
    def get_fechas_procesamiento_costo(self):
        fechas = self.all()
        fechas_dict = {}
        for item in fechas:
            ueb = item.ueb
            if not ueb in fechas_dict.keys():
                fechas_dict[ueb] = {}
            fechas_dict[ueb]['mes'] = item.mes
            fechas_dict[ueb]['anno'] = item.anno
        return fechas_dict
class FechaProcesamientoCosto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anno = models.IntegerField(default=0, verbose_name=_("Año"))
    mes = models.IntegerField(default=0, verbose_name=_("Mes"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='fechaprocesamientocosto_ueb')
    inicial = models.BooleanField(default=False, verbose_name=_("Inicial"))

    objects_cache = FechaProcesamientoCostoCacheManager()

    class Meta:
        db_table = 'cos_fechaprocesamientocosto'
        ordering = ['ueb__codigo']
        verbose_name_plural = _('Fechas de Procesamiento del Costo')
        verbose_name = _('Fecha de Procesamiento del Costo')

        indexes = [
            models.Index(
                fields=[
                    'ueb',
                    'mes',
                    'anno',
                ]
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['mes', 'anno', 'ueb',],
                name='unique_fechaproceccosto'
            ),
        ]

    def to_dict(self):
        return {
            self.ueb: {
                ChoiceFechas.PROCESAMIENTO: {'mes': self.mes, 'anno': self.anno}
            }
        }

    @property
    def mes_nombre(self):
        meses = CHOICES_MESES
        return meses.get(self.mes, _('Desconocido'))

    def get_mes_display(self):
        return self.mes_nombre


class VarGlobalesCosto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='varglobal_ueb')
    anno = models.IntegerField(default=0, verbose_name=_("Año"))
    mes = models.IntegerField(default=0, verbose_name=_("Mes"))
    centrocosto = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, related_name='varglobal_cc', verbose_name='Centro Costo')

    class Meta:
        db_table = 'cos_varglobalescosto'
        ordering = ['ueb__codigo', 'centrocosto__descripcion', '-anno', '-mes']
        verbose_name_plural = _('Centros de Costo Variables Globales')
        verbose_name = _('Centro de Costo Variables Globales')

        indexes = [
            models.Index(
                fields=[
                    'ueb',
                    'mes',
                    'anno',
                    'centrocosto',
                ]
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['ueb', 'mes', 'anno', 'centrocosto',],
                name='unique_varglobalescosto'
            ),
        ]

    def __str__(self):
        return self.centrocosto.descripcion

class VarGlobalesCostoDatos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    varglobalescosto = models.ForeignKey(VarGlobalesCosto, on_delete=models.PROTECT, related_name='varglobaldatos_varglobalescosto')
    variable_global = models.ForeignKey(CostoVarGlobales, on_delete=models.PROTECT, related_name='varglobaldatos_variable', verbose_name=_("Variable"))
    destino = TextChoicesField(choices_enum=Destino, verbose_name=_("Destination"))
    valor = models.DecimalField(max_digits=18, decimal_places=2, db_default=0.00, verbose_name=_("Valor"))

    class Meta:
        db_table = 'cos_varglobalescostodatos'
        ordering = ['variable_global__descripcion', 'destino', 'variable_global__activa']
        verbose_name_plural = _('Valor de las Variables Globales del Costo')
        verbose_name = _('Valor de la Variable Global del Costo')

        indexes = [
            models.Index(
                fields=[
                    'variable_global',
                    'destino',
                ]
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['varglobalescosto', 'variable_global', 'destino',],
                name='unique_varglobalescostodatos'
            ),
        ]

    def __str__(self):
        return self.variable_global.descripcion