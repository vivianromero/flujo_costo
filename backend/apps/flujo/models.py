import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import Q, F, Value, DecimalField
from django.db.models.functions import Now, Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.codificadores.models import UnidadContable, Departamento, TipoDocumento, MotivoAjuste, EstadoProducto, \
    ProductoFlujo, ConfigNumero, ObjectsManagerAbstract, OperacionDocumento, TipoNumeroDoc, Medida, \
    NormaconsumoDetalle, FechaInicio, DatosCacheManager
from . import ChoiceFechas

OPERACION_ENTRADA_SALIDA = [
    (1, 'Entrada'),
    (-1, 'Salida')
]

class EstadosDocumentos(models.IntegerChoices):
    EDICION = 1, 'Edición'
    CONFIRMADO = 2, 'Confirmado'
    RECHAZADO = 3, 'Rechazado'
    CANCELADO = 4, 'Cancelado'
    ERRORES = 5, 'Con Errores'


class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Create at"))
    numerocontrol = models.CharField(max_length=50, verbose_name=_("Control Number"))
    numeroconsecutivo = models.IntegerField(verbose_name=_("Consecutive Number"))
    suma_importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    observaciones = models.TextField(blank=True, null=True, verbose_name=_("Observations"))
    estado = IntegerChoicesField(choices_enum=EstadosDocumentos,
                                 db_comment="Estado del documento 1:Edición, 2:Confirmado, 3:Rechazado",
                                 verbose_name=_("Status"), default=EstadosDocumentos.EDICION)
    reproceso = models.BooleanField(default=False, verbose_name=_("Reprocessing"))
    editar_nc = models.BooleanField(default=False)
    comprob = models.CharField(max_length=150, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documento_departamento')
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='documento_tipodocumento', verbose_name=_("Tipo Documento"))
    anno = models.IntegerField(default=0)
    mes = models.IntegerField(default=0)
    confconsec = IntegerChoicesField(choices_enum=ConfigNumero,
                                     db_comment="Para guardar el tipo de conf para el consecutivo y poder establecer la constarint",
                                     default=ConfigNumero.DEPARTAMENTO)
    confcontrol = IntegerChoicesField(choices_enum=ConfigNumero,
                                      db_comment="Para guardar el tipo de conf para el numero de control y poder establecer la constarint",
                                      default=ConfigNumero.DEPARTAMENTO)
    error = models.BooleanField(default=False, verbose_name=_("Error"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documento_ueb')
    cerrado = models.BooleanField(default=False)

    class Meta:
        db_table = 'fp_documento'
        constraints = [
            models.UniqueConstraint(
                fields=['numeroconsecutivo', 'departamento', 'mes', 'anno', 'ueb'],
                condition=Q(confconsec=ConfigNumero.DEPARTAMENTO),
                name='unique_numeroconsecutivo_departamento_tipodocumento'
            ),
            models.UniqueConstraint(
                fields=['numeroconsecutivo', 'mes', 'anno', 'ueb'],
                condition=Q(confconsec=ConfigNumero.UNICO),
                name='unique_numeroconsecutivo_ueb'
            ),
            models.UniqueConstraint(
                fields=['numerocontrol', 'departamento', 'anno', 'ueb'],
                condition=Q(confcontrol=ConfigNumero.DEPARTAMENTO),
                name='unique_numerocontrol_departamento'
            ),
            models.UniqueConstraint(
                fields=['numerocontrol', 'anno', 'ueb'],
                condition=Q(confcontrol=ConfigNumero.UNICO),
                name='unique_numerocontrol_ueb'
            ),
        ]
        ordering = ['ueb', 'departamento', '-numeroconsecutivo', 'tipodocumento']
        indexes = [
            models.Index(
                fields=[
                    'ueb',
                    'departamento',
                    'fecha',
                    'estado']
            ),
            models.Index(
                fields=[
                    'fecha',
                    'numeroconsecutivo'
                ]
            )
        ]

    def __str__(self):
        return self.tipodocumento.descripcion if self.numeroconsecutivo else ''

    def get_numerocontrol(self):
        nros = self.numerocontrol.split('/')
        return int(nros[len(nros) - 1])

    def get_numerocontrol_prefijo(self):
        return '' if not '/' in self.numerocontrol else self.numerocontrol.split('/')[0]

    @property
    def operacion(self):
        return 1 if self.tipodocumento.operacion == OperacionDocumento.ENTRADA else -1

    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método delete para actualizar existencias en documentos posteriores
        """
        from .utils import actualiza_existencias_documentos
        from apps.codificadores import ChoiceTiposDoc

        with transaction.atomic():
            # 1. Recolectar todos los productos/estados afectados
            productos_estados = set()

            # Productos en DocumentoDetalle principal
            productos_estados.update(
                self.documentodetalle_documento
                    .values_list('producto_id', 'estado')
                    .distinct()
            )

            # Productos en relaciones relacionadas
            relaciones = [
                ('documentodetalleestado_detalle', 'producto_id'),
                ('documentodetalleproducto_detalle', 'producto_id'),
                ('documentodetalleproductonc_detalle', 'normaconsumodetalles__producto_id'),
                ('documentodetalleproductono_detalle', 'normaoperativadetalle__producto_id'),
            ]

            for relacion, campo_producto in relaciones:
                productos_estados.update(
                    self.documentodetalle_documento
                        .values_list(f"{relacion}__{campo_producto}", f"{relacion}__estado")
                        .distinct()
                )

            # Guardar el consecutivo antes de eliminar
            consecutivo = self.numeroconsecutivo

            # 2. Primero llamar al delete original para borrar el documento y sus relaciones
            super().delete(*args, **kwargs)

            # 3. Actualizar documentos posteriores para cada producto/estado
            for producto_id, estado in productos_estados:
                if producto_id is None:  # Saltar relaciones nulas
                    continue

                condiciones = Q(
                    # DocumentoDetalle
                    Q(documentodetalle_documento__estado=estado) &
                    Q(documentodetalle_documento__producto_id=producto_id)
                ) | Q(
                    # DocumentoDetalleEstado
                    Q(documentodetalle_documento__documentodetalleestado_detalle__estado=estado) &
                    Q(documentodetalle_documento__documentodetalleestado_detalle__producto_id=producto_id)
                ) | Q(
                    # DocumentoDetalleProducto
                    Q(documentodetalle_documento__documentodetalleproducto_detalle__estado=estado) &
                    Q(documentodetalle_documento__documentodetalleproducto_detalle__producto_id=producto_id)
                ) | Q(
                    # DocumentoDetalleProductoNC
                    Q(documentodetalle_documento__documentodetalleproductonc_detalle__estado=estado) &
                    Q(documentodetalle_documento__documentodetalleproductonc_detalle__normaconsumodetalles__producto_id=producto_id)
                ) | Q(
                    # DocumentoDetalleProductoNO
                    Q(documentodetalle_documento__documentodetalleproductono_detalle__estado=estado) &
                    Q(documentodetalle_documento__documentodetalleproductono_detalle__normaoperativadetalle__producto_id=producto_id)
                )

                # Encontrar primer documento posterior con este producto/estado
                primer_anterior = Documento.objects.filter(
                    condiciones,
                    numeroconsecutivo__lt=consecutivo
                ).annotate(
                    producto_documentodetalle=F('documentodetalle_documento__producto_id'),
                    documentodetalleproductono_id=F('documentodetalle_documento__documentodetalleproductono_detalle__id'),
                    existencia=Coalesce(F('documentodetalle_documento__existencia'), Value(0.00, output_field=DecimalField())),
                    existencia_estado=Coalesce(F('documentodetalle_documento__documentodetalleestado_detalle__existencia'), Value(0.00, output_field=DecimalField())),
                    existencia_producto=Coalesce(F('documentodetalle_documento__documentodetalleproducto_detalle__existencia'), Value(0.00, output_field=DecimalField())),
                    existencia_nc=Coalesce(F('documentodetalle_documento__documentodetalleproductonc_detalle__existencia'), Value(0.00, output_field=DecimalField())),
                    existencia_no=Coalesce(F('documentodetalle_documento__documentodetalleproductono_detalle__existencia'), Value(0.00, output_field=DecimalField())),
                    cantidad_usada=Coalesce(F('documentodetalle_documento__documentodetalleproductono_detalle__cantidad_usada'), Value(0.00, output_field=DecimalField()))
                ).order_by(
                    '-numeroconsecutivo',
                    'documentodetalle_documento__documentodetalleproductono_detalle__existencia'
                ).distinct().first()

                existencia_anterior = Decimal('0.0')
                documento = self
                if primer_anterior:
                    if primer_anterior.tipodocumento.id != ChoiceTiposDoc.RECEPCION_PRODUCCION:
                        existencia_anterior = primer_anterior.existencia + primer_anterior.existencia_estado + primer_anterior.existencia_producto
                    elif primer_anterior.producto_documentodetalle == producto_id:
                        existencia_anterior = primer_anterior.existencia
                    elif not primer_anterior.documentodetalleproductono_id is None:
                        existencia_anterior = primer_anterior.existencia_no
                    else:
                        existencia_anterior = primer_anterior.existencia_nc
                actualiza_existencias_documentos(
                    doc=documento,
                    producto=producto_id,
                    estado=estado,
                    existencia_anterior=existencia_anterior
                )


class DocumentoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"),
                                   validators=[MinValueValidator(0.0001, message=_(
                                       'El valor debe ser >= 0'))]
                                   )
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentodetalle_documento')
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetalle_producto',
                                 verbose_name=_("Product"))
    error = models.BooleanField(default=False, verbose_name=_("Error"))
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=1
    )

    class Meta:
        db_table = 'fp_documentodetalle'

        constraints = [
            models.UniqueConstraint(
                fields=['documento', 'estado', 'producto'],
                name='unique_documentodetalle_documento_estado_producto'
            )
        ]
        indexes = [
            models.Index(
                fields=[
                    'documento']
            ),
            models.Index(
                fields=[
                    'producto']
            )
        ]

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''


class DocumentoAjuste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentoajuste_documento')
    motivoajuste = models.ForeignKey(MotivoAjuste, on_delete=models.PROTECT, related_name='documentoajuste_motivo',
                                     verbose_name=_("Adjustment Reason"))

    class Meta:
        db_table = 'fp_documentoajuste'


class DocumentoTransfDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentotransfdepartamento_documento')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='documentotransfdepartamento_departamento',
                                     verbose_name=_("Department"))

    class Meta:
        db_table = 'fp_documentotransfdepartamento'


# esto es el detalle de la transf hacia departamento PARA EL DEPARTAMENTO DE CONTROL TECNICO
# se genera la transf hacia departamento con los buenos, suma de los defectuosos y prueba sensorial
class DocumentoDetalleTransfDptoControlTecnico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity")
                                   )
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentodetalletransfdptocontroltecnico_documento')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalletransfdptocontroltecnico_producto',
                                 verbose_name=_("Product"))
    buenos = models.IntegerField(default=0, verbose_name=_("Good"))
    defectuoso_cc = models.IntegerField(default=0, verbose_name=_("Defective CC"))
    defectuoso_cien = models.IntegerField(default=0, verbose_name=_("Defective 100%"))
    sensorial = models.IntegerField(default=0, verbose_name=_("Sensory Test"))
    rotos = models.IntegerField(default=0, verbose_name=_("Broken"))
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=1
    )

    class Meta:
        db_table = 'fp_documentodetalletransfdptocontroltecnico'


class DocumentoTransfDepartamentoRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentotransfdepartamentorecibida_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                        related_name='documentotransfdepartamentorecibida_documentoorigen',
                                        db_comment="Documento que originó la transferencia hacia el departamento")

    class Meta:
        db_table = 'fp_documentotransfdesdedepartamento'

    def __str__(self):
        return self.documento.tipodocumento.descripcion if self.documento.numeroconsecutivo else ''


class DocumentoTransfExterna(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentotransfext_documento')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                       related_name='documentotransfext_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexterna'


class DocumentoTransfExternaDptoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentotransfext = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                           related_name='documentotransfextdptodest_documento')
    departamento_destino = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                             related_name='documentotransfext_departamento_destino')

    class Meta:
        db_table = 'fp_documentotransfexternadptodestino'


# transf hacia recibida desde otra unidad contable
class DocumentoTransfExternaRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentotransfextrecibida_documento')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                       related_name='documentotransfextrecibida_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexternarecibida'


# ID DEL DOC QUE ORIGINO LA TRANSF
# SI LA BD NO ES UNICA EL DATO DEL ID DOCUMENTO NO EXISTE Y NO SE PUEDE DEFINIR LA UNIDAD CONTABLE ORIGEN.
class DocumentoTransfExternaRecibidaDocOrigen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, default=None,
                                  related_name='documentotransfextrecibidadocorigen_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT, default=None,
                                        related_name='documentotransfextrecibida_documentoorigen')

    class Meta:
        db_table = 'fp_documentotransfexternarecibidadocorigen'


# Venta a trabajadores
class DocumentoDetalleVenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                         related_name='documentodetalleventa_detalle')

    class Meta:
        db_table = 'fp_documentodetalleventa'


# Cambio de estado, estado destino
class DocumentoDetalleEstado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleestado_detalle')
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalleproducto_estado',
                                 verbose_name=_("Product"), default=None)
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetalleestado'

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
    ]


# Cambio de producto, producto destino
# el producto origen está en documentodetalle
class DocumentoDetalleProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalleproducto_producto',
                                 verbose_name=_("Product"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.BUENO)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleproducto_detalle')
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity")
                                   )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetalleproducto'

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
        models.Index(
            fields=[
                'producto']
        )
    ]


class DocumentoDevolucion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentodevolucion_documento')

    class Meta:
        db_table = 'fp_documentodevolucion'


# Devolución recibida desde otro dpto
class DocumentoDevolucionRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentodevolucionrecibida_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                        related_name='documentodevolucionrecibida_documentoorigen',
                                        db_comment="Documento que originó la devolucion hacia el departamento")

    class Meta:
        db_table = 'fp_documentodevolucionrecibida'


class NormaOperativa(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='normaoperativa_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_normaoperativa'
        verbose_name_plural = _('Normas Operativas')
        verbose_name = _('Norma Operativa')

        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'ueb'],
                name='unique_normaoperativa_fecha_ueb'
            ),
        ]

        indexes = [
            models.Index(fields=[
                'fecha',
                'ueb'
            ]),
        ]

class NormaOperativaProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    normaoperativa = models.ForeignKey(NormaOperativa, on_delete=models.CASCADE, related_name='normaoperativaproductos')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='productonormaoperativa')
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='medida_normaoperativaproducto',
                               verbose_name=_("Medida"))
    fecha_creacion = models.DateTimeField(default=timezone.now)
    idsispax = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'fp_normaoperativa_producto'
        ordering = ['producto__descripcion']

    indexes = [
        models.Index(fields=[
            'normaoperativa',
            'producto'
        ]),
    ]

    def __str__(self):
        return f"{self.producto.descripcion}"



class NormaOperativaDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    norma = models.DecimalField(max_digits=18, decimal_places=6, default=0.0)
    normaoperativaproducto = models.ForeignKey(NormaOperativaProducto, on_delete=models.CASCADE,
                                               related_name='normaoperativaproducto_detalles')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='productonormaoperativa_detalle')
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='medida_normaoperativadetalle',
                               verbose_name=_("Medida"))

    class Meta:
        db_table = 'fp_normaoperativa_detalle'


class DocumentoDetalleProductoNC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleproductonc_detalle')
    normaconsumodetalles = models.ForeignKey(NormaconsumoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleproductoncdetalle_detalle')
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.BUENO)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity")
                                   ) #se usa la norma ramal para el calculo de esta cantidad
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=-1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetalleproductonc'
        ordering = ['normaconsumodetalles__producto__descripcion']

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
        models.Index(
            fields=[
                'producto']
        ),
        models.Index(
            fields=[
                'normaconsumodetalles']
        )
    ]

    @property
    def producto(self):
        return self.normaconsumodetalles.producto

class DocumentoDetalleProductoNO(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleproductono_detalle')
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.BUENO)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"),
                                   db_comment="Cantidad de productos producidos usando esta Norma Operativa"
                                   )
    normaoperativadetalle = models.ForeignKey(NormaOperativaDetalle, on_delete=models.PROTECT,
                                         related_name='documentodetalleproductono_no')
    cantidad_usada = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"),
                                   db_comment="Cantidad que se usó del producto de la norma operativa"
                                   )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=-1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))
    orden = models.IntegerField(default=0, verbose_name=_("Orden"))

    class Meta:
        db_table = 'fp_documentodetalleproductono'
        ordering = ['documentodetalle', 'orden']

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
        models.Index(
            fields=[
                'producto']
        ),
        models.Index(
            fields=[
                'normaoperativa'
            ]
        )
    ]

    @property
    def producto(self):
        return self.normaoperativadetalle.producto

# Se guardan los documentos que se salvan o confirman y son los procedents del versat
class DocumentoOrigenVersat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoversat = models.IntegerField()
    fecha_documentoversat = models.DateTimeField(db_default=Now(), verbose_name=_("Fecha versat at"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentoorigenversat_documento')
    documento_origen = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        db_table = 'fp_documentoorigenversat'


# Los documentos del versat que son rechazados, se guarda el id de los documentos del versat que se rechazan
class DocumentoVersatRechazado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoversat = models.IntegerField()
    fecha_documentoversat = models.DateField()
    fecha_rechazo = models.DateTimeField(db_default=Now())
    documento_origen = models.JSONField(blank=True, null=True, default=dict)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documentoversatrechazado_ueb')

    class Meta:
        db_table = 'fp_documentoversatrechazado'

#Detalle de los Reporcesos
class DocumentoDetalleReproceso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetallereprocesodeficiente_documentodetalle')
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.BUENO)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"),
                                   validators=[MinValueValidator(0.0001, message=_('El valor debe ser >= 0'))]
                                   )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetallereproceso_producto')
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=-1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetallereproceso'

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
        models.Index(
            fields=[
                'producto']
        ),
    ]

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''


class DocumentoDetalleReprocesoDeficiente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetallereprocesodeficiente_reproceso')
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.DEFICIENTE)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"),
                                 validators=[MinValueValidator(0.0000001, message=_('El valor debe ser >= 0'))]
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"),
                                   validators=[MinValueValidator(0.0001, message=_('El valor debe ser >= 0'))]
                                   )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetallereprocesodeficiente_detalle')
    operacion = models.SmallIntegerField(
        choices=OPERACION_ENTRADA_SALIDA,
        default=-1
    )
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetallereprocesodeficientes'

    indexes = [
        models.Index(
            fields=[
                'documentodetalle']
        ),
        models.Index(
            fields=[
                'producto']
        ),
    ]
    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''

class FechaPeriodoCacheManager(DatosCacheManager):

    def get_cached_data(self):
        if self._cache is None:
            self._cache = self.get_fechas_procesamiento_inicio()
        return self._cache

    @transaction.atomic
    def get_fechas_procesamiento_inicio(self):
        fechas = self.all()
        fechasinicio = FechaInicio.objects.select_for_update().all()
        list_dicc = [objeto.to_dict() for objeto in fechas]
        fechas_dict = {}
        for item in list_dicc:
            ueb = item.pop('ueb')
            dpto = [x for x in item.keys()][0]
            inicio = fechasinicio.filter(ueb=ueb, departamento=dpto).first()
            if ueb in fechas_dict.keys():
                fechas_dict[ueb][dpto] = item[dpto]
                fechas_dict[ueb][dpto]['fecha_inicio'] = inicio.fecha if inicio else None
            else:
                fechas_dict[ueb] = item
                fechas_dict[ueb][dpto]['fecha_inicio'] = inicio.fecha if inicio else None
        return fechas_dict

class FechaPeriodo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='fechaperiodo_departamento',
                                     verbose_name=_("Department"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='fechaperiodo_ueb',
                            verbose_name="UEB")
    objects = FechaPeriodoCacheManager()

    class Meta:
        db_table = 'fp_fechaperiodo'
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'departamento', 'ueb'],
                name='unique_fechaperiodo_fecha_departamento_ueb'
            ),
        ]

    def to_dict(self):
        return {
            "ueb": self.ueb,
            self.departamento: {
                ChoiceFechas.PROCESAMIENTO: self.fecha,
            }
        }

    @property
    def fecha_mes_procesamiento(self):
        return self.fecha.replace(day=1).strftime('%Y-%m-%d')


class FechaCierreMes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='fechacierremes_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_fechacierremes'
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'ueb'],
                name='unique_fechacierremes_fecha_ueb'
            ),
        ]


class ExistenciaDpto(ObjectsManagerAbstract):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='existencias_producto',
                                 verbose_name=_("Product"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    cantidad_inicial = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                           verbose_name=_("Cantidad Inicial"))
    cantidad_entrada = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                           verbose_name=_("Entradas"))
    cantidad_salida = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                          verbose_name=_("Salidas"))
    cantidad_final = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                         verbose_name=_("Cantidad Final"))
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='existencias_departamento')
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='existencias_ueb')
    anno = models.IntegerField(default=0)
    mes = models.IntegerField(default=0)

    class Meta:
        db_table = 'fp_existenciadpto'
        constraints = [
            models.UniqueConstraint(
                fields=['producto', 'estado', 'departamento', 'ueb', 'mes', 'anno'],
                name='unique_existencias_producto_estado_departamento_ueb_mes_anno'
            )
        ]
        indexes = [
            models.Index(
                fields=[
                    'producto',
                    'estado',
                    'departamento',
                    'ueb',
                    'mes',
                    'anno']
            )
        ]


class NumeroDocumentos(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tiponumero = IntegerChoicesField(choices_enum=TipoNumeroDoc, verbose_name=_("Tipo número"),
                                     default=TipoNumeroDoc.NUMERO_CONSECUTIVO)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='numdoc_departamento',
                                     verbose_name=_("Department"),
                                     blank=True, null=True)
    numero = models.IntegerField(verbose_name=_("Número"), default=0)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='numdoc_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_numerodocumentos'
        constraints = [
            models.UniqueConstraint(
                fields=['tiponumero', 'departamento', 'ueb'],
                name='unique_numdocumentos_tiponumero_departamento_ueb'
            ),
        ]

        indexes = [
            models.Index(fields=[
                'departamento',
                'ueb'
            ]),
            models.Index(fields=[
                'ueb'
            ]
            ),
        ]