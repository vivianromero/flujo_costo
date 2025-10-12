from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from apps.flujo.models import DocumentoDetalleProductoNC, DocumentoDetalleReprocesoDeficiente, EstadoProducto, DocumentoDetalleReproceso
from apps.codificadores import ChoiceTiposDoc
from apps.flujo.utils import existencia_producto, actualiza_existencias_documentos


@receiver(post_save, sender=DocumentoDetalleProductoNC)
def actualiza_precio_reporte_produccion(sender, instance, **kwargs):
    """
        Actualiza el precio en DocumentoDetalle cuando se guarda un DocumentoDetalleProductoNC.
        """

    documentodetalle = instance.documentodetalle

    suma_precios = DocumentoDetalleProductoNC.objects.filter(
        documentodetalle=documentodetalle
    ).aggregate(
        total_precios=Sum('precio')
    )['total_precios'] or 0.00  # Si no hay registros, devuelve 0.00

    documentodetalle.precio = suma_precios
    documentodetalle.importe = suma_precios * documentodetalle.cantidad

    documentodetalle.save(update_fields=['precio', 'importe'])

@receiver(post_delete, sender=DocumentoDetalleReprocesoDeficiente)
@receiver(post_delete, sender=DocumentoDetalleReproceso)
def actualiza_reproceso_deficientes(sender, instance, **kwargs):
    """
    Actualiza la existencia de los deficientes que se reprocesaron y los productos del reproceso
    """
    doc, producto, cantidad, estado = instance.documentodetalle.documento, instance.producto, instance.cantidad, instance.estado
    existencia, hay_error = existencia_producto(doc, producto, estado,
                                                cantidad, -1)
    existencia += cantidad
    actualiza_existencias_documentos(doc, producto, estado, existencia)






