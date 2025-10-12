# import calendar
# import datetime
# import json
# from ast import literal_eval
# from datetime import datetime
# from datetime import timedelta
#
# import requests
# import sweetify
# from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
# from django.db import IntegrityError
# from django.db.models import Max
# from django.db.models import ProtectedError
# from django.http import HttpResponse, HttpResponseRedirect
# from django.http import JsonResponse
# from django.shortcuts import redirect, get_object_or_404
# from django.urls import reverse
# from django.utils.translation import gettext as _
# from django.utils.translation import gettext_lazy as _
# from django.views.decorators.csrf import csrf_exempt
# from django_htmx.http import HttpResponseLocation, trigger_client_event
#
# from apps.app_apiversat.functionapi import getAPI
# from apps.app_index.views import CommonCRUDView, BaseModalFormView
# from apps.codificadores.models import *
# from apps.cruds_adminlte3.inline_htmx_crud import InlineHtmxCRUD
# from apps.flujo.filters import DocumentoFilter, NormaOperativaFilter, NormaOperativaProductoFilter
# from apps.flujo.tables import DocumentoTable, DocumentoProduccionTable, DocumentoDetalleReprocesoTable, \
#     DocumentoProduccionNOTable, DocumentosVersatTable, DocumentosVersatDetalleTable, DocumentoDetalleTable, \
#     NormaOperativaTable, NormaOperativaProductoTable, NormaOperativaDetalleTable
# from apps.utiles.utils import message_error
# from .forms import *
# from .forms import DameDptoATransfForm
# from .reportsforms import *
# from .utils import ids_documentos_versat_procesados, actualiza_numeros, \
#     dame_fecha, renumerar_documentos, dame_precio_salida
#
#
# class DocumentoDetalleReprocesoHtmxCRUD(InlineHtmxCRUD):
#     model = DocumentoDetalleReproceso
#     base_model = DocumentoDetalle
#     namespace = 'app_index:flujo'
#     inline_field = 'documentodetalle'
#     add_form = DocumentoDetalleReprocesoForm
#     update_form = DocumentoDetalleReprocesoForm
#     detail_form = DocumentoDetalleReprocesoForm
#     table_class = DocumentoDetalleReprocesoTable
#
#
#     views_available = [
#         'update',
#         'create',
#         'list',
#         'list_detail',
#         'detail',
#         'delete',
#     ]
#
#     title = "Recepción de Producción de Reproceso"
#
#     hx_retarget = '#generic_modal_inner'
#     hx_reswap = 'innerHTML'
#     hx_swap = 'innerHTML'
#     hx_form_target = '#generic_modal_inner'
#     hx_form_swap = 'innerHTML'
#
#     def get_create_view(self):
#         create_view = super().get_create_view()
#
#         class CreateView(create_view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 try:
#                     doc = self.model_id
#                     self.object = form.save(commit=False, doc=doc, existencia=None)
#                     setattr(self.object, self.inline_field, self.model_id)
#                     self.object.save()
#                 except IntegrityError as e:
#                     mess_error = self.integrity_error
#                 return super().form_valid(form)
#         return CreateView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 try:
#                     doc = self.model_id
#                     self.object = form.save(commit=False, doc=doc, existencia=None)
#                     setattr(self.object, self.inline_field, self.model_id)
#                     self.object.save()
#                 except IntegrityError as e:
#                     mess_error = self.integrity_error
#                 return super().form_valid(form)
#
#         return OEditView
#
# class DocumentoDetalleProductoNCHtmxCRUD(InlineHtmxCRUD):
#     model = DocumentoDetalleProductoNC
#     base_model = DocumentoDetalle
#     namespace = 'app_index:flujo'
#     inline_field = 'documentodetalle'
#     detail_form = DocumentoDetalleProductoNCForm
#     table_class = DocumentoProduccionTable
#
#
#     views_available = [
#         'list',
#         'list_detail',
#         'detail',
#     ]
#
#     title = "Normas de Consumo"
#
#     hx_retarget = '#generic_modal_inner'
#     hx_reswap = 'innerHTML'
#     hx_swap = 'innerHTML'
#     hx_form_target = '#generic_modal_inner'
#     hx_form_swap = 'innerHTML'
#
#     def get_create_view(self):
#         create_view = super().get_create_view()
#
#         class CreateView(create_view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 try:
#                     doc = self.model_id
#                     self.object = form.save()
#                     setattr(self.object, self.inline_field, self.model_id)
#                     self.object.save()
#                 except IntegrityError as e:
#                     mess_error = self.integrity_error
#
#                 return super().form_valid(form)
#
#         return CreateView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 doc = self.model_id
#                 setattr(self.object, self.inline_field, self.model_id)
#                 self.object.save()
#                 return super().form_valid(form)
#
#         return OEditView
#
# class DocumentoDetalleProductoNOHtmxCRUD(InlineHtmxCRUD):
#     model = DocumentoDetalleProductoNO
#     base_model = DocumentoDetalle
#     namespace = 'app_index:flujo'
#     inline_field = 'documentodetalle'
#     add_form = DocumentoDetalleProductoNOForm
#     update_form = DocumentoDetalleProductoNOForm
#     detail_form = DocumentoDetalleProductoNOForm
#     table_class = DocumentoProduccionNOTable
#
#     views_available = [
#         'list',
#         'list_detail',
#         'create',
#         'update',
#         'delete',
#         'detail',
#     ]
#
#     title = "Normas Operativas"
#
#     hx_retarget = '#generic_modal_inner'
#     hx_reswap = 'innerHTML'
#     hx_swap = 'innerHTML'
#     hx_form_target = '#generic_modal_inner'
#     hx_form_swap = 'innerHTML'
#
#     def get_create_view(self):
#         create_view = super().get_create_view()
#
#         class CreateView(create_view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs['documento_detalle'] = self.model_id
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 context['target'] = self.request.GET.get('target', None)
#                 return context
#
#             def form_valid(self, form, **kwargs):
#                 event_action = None
#                 if self.request.method == 'POST':
#                     event_action = self.request.POST.get('event_action', None)
#                 elif self.request.method == 'GET':
#                     event_action = self.request.GET.get('event_action', None)
#                 target = '#id_%s_myList' % self.name
#                 documento_detalle = self.model_id
#                 producto = documento_detalle.producto
#                 fecha_documento = form.cleaned_data['fecha_documento']
#                 ueb = documento_detalle.documento.ueb
#                 departamento = documento_detalle.documento.departamento
#
#                 try:
#                     existencia_obj = ExistenciaDpto.objects.get(
#                         producto=producto,
#                         ueb=ueb,
#                         departamento=departamento,
#                         mes=documento_detalle.documento.fecha.month,
#                         anno=documento_detalle.documento.fecha.year
#                     )
#                 except ExistenciaDpto.DoesNotExist:
#                     existencia_obj = None
#
#                 normas_operativas = NormaOperativaDetalle.objects.filter(
#                     normaoperativaproducto__producto=producto,
#                     normaoperativaproducto__normaoperativa__fecha=fecha_documento,
#                     normaoperativaproducto__normaoperativa__ueb=ueb
#                 ).select_related('normaoperativaproducto__normaoperativa').distinct()
#                 if normas_operativas.exists():
#                     DocumentoDetalleProductoNO.objects.filter(documentodetalle=documento_detalle).delete()
#                     # Preparar listas para bulk_create
#                     nuevos_registros = []
#                     orden = 1
#                     for detalle in normas_operativas:
#                         nuevos_registros.append(
#                             DocumentoDetalleProductoNO(
#                                 documentodetalle=documento_detalle,
#                                 normaoperativadetalle=detalle,
#                                 existencia=existencia_obj.cantidad_final if existencia_obj else 0.0,
#                                 cantidad=0.0,
#                                 estado=existencia_obj.estado if existencia_obj else 1,
#                                 precio=documento_detalle.precio,
#                                 orden=orden,
#                             )
#                         )
#                         orden += 1
#
#                     producto_documento = self.model_id.producto  # Producto del DocumentoDetalle
#                     precio_producto = dame_precio_salida(producto_documento, self.model_id.estado,
#                                                             self.model_id.documento)
#                     # Buscar NormaConsumo asociadas al producto del DocumentoDetalle
#                     normas_consumo = NormaConsumo.objects.filter(
#                         producto=producto_documento,
#                         activa=True,
#                         confirmada=True
#                     ).prefetch_related('normaconsumodetalle_normaconsumo').first()  # Optimización
#
#                     dicc_exist_nc = {}
#
#                     # Iterar sobre cada NormaConsumo y sus detalles
#                     if normas_consumo:
#                         for detalle_norma in normas_consumo.normaconsumodetalle_normaconsumo.all():
#                             # Calcular cantidad (ejemplo)
#                             base_norma = normas_consumo.cantidad
#                             if base_norma <= 0:
#                                 raise ValueError(f"La cantidad base de la norma {normas_consumo.id} no puede ser cero")
#
#                             cantidad_calculada = (
#                                 Decimal(self.model_id.cantidad) *
#                                 detalle_norma.norma_ramal /
#                                 Decimal(base_norma)
#                             ).quantize(Decimal('0.000000'))
#                             precio_producto = dame_precio_salida(detalle_norma.producto, self.model_id.estado,
#                                                 self.model_id.documento)
#                             existencia = valida_existencia_producto(self.model_id.documento, detalle_norma.producto,
#                                                                     self.model_id.estado, cantidad_calculada, -1)
#                             if not existencia:
#                                 form.add_error(None, "No hay existencias de materia prima para la producción de este producto")
#                                 self.model_id.delete()
#                                 return self.form_invalid(form)
#
#                             dicc_exist_nc[detalle_norma.producto] = {'existencia': existencia, 'precio': precio_producto}
#                             # Crear/actualizar DocumentoDetalleProductoNC
#                             DocumentoDetalleProductoNC.objects.update_or_create(
#                                 documentodetalle=self.model_id,
#                                 normaconsumodetalles=detalle_norma,
#                                 defaults={
#                                     'existencia': existencia,
#                                     'estado': self.model_id.estado,
#                                     'precio': precio_producto,
#                                     'cantidad': cantidad_calculada,
#                                     'importe': precio_producto * cantidad_calculada
#                                 }
#                             )
#                     # Crear todos los registros en una sola operación
#                     if nuevos_registros:
#                         DocumentoDetalleProductoNO.objects.bulk_create(nuevos_registros)
#                     self.object = self.model.objects.filter(documentodetalle=self.model_id).first()
#                 else:
#                     form.add_error(None, "No hay Normas Operativas para la fecha seleccionada")
#                     return super().form_invalid(form)
#
#                 return HttpResponseLocation(
#                     self.get_success_url(),
#                     target=target,
#                     headers={
#                         'HX-Trigger': self.request.htmx.trigger,
#                         'HX-Trigger-Name': self.request.htmx.trigger_name,
#                         'event_action': event_action,
#                     },
#                     values={
#                         'event_action': event_action,
#                     }
#                 )
#         return CreateView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 form_kwargs['documento_detalle'] = self.model_id
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 doc = self.model_id
#                 self.object.documentodetalle = self.model_id
#                 setattr(self.object, self.inline_field, self.model_id)
#                 self.object.save()
#                 return super().form_valid(form)
#
#         return OEditView
#
#     def get_detail_view(self):
#         view = super().get_detail_view()
#
#         class DetailView(view):
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#         return DetailView
#
#
# # ------ DocumentoDetalle / HtmxCRUD ------
# class DocumentoDetalleHtmxCRUD(InlineHtmxCRUD):
#     model = DocumentoDetalle
#     base_model = Documento
#     namespace = 'app_index:flujo'
#     inline_field = 'documento'
#     add_form = DocumentoDetalleForm
#     update_form = DocumentoDetalleForm
#     detail_form = DocumentoDetalleDetailForm
#     table_class = DocumentoDetalleTable
#     list_fields = [
#         'producto',
#         'estado',
#         'cantidad',
#         'precio',
#         'importe',
#         'existencia',
#     ]
#
#     views_available = [
#         'list',
#         'list_detail',
#         'create',
#         'update',
#         'delete',
#         'detail',
#     ]
#
#     inlines = []
#
#     title = "Detalles de documentos"
#
#     hx_retarget = '#edit_modal_inner'
#     hx_reswap = 'innerHTML'
#     hx_swap = 'innerHTML'
#     hx_form_target = '#edit_modal_inner'
#     hx_form_swap = 'innerHTML'
#
#     def get_create_view(self):
#         create_view = super().get_create_view()
#
#         class CreateView(create_view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_form(self, form_class=None):
#                 form = super().get_form(form_class)
#                 if not form.fields['producto'].queryset.exists():
#                     form.fields['producto'].help_text = "No hay productos disponibles para este documento"
#                     form.fields['producto'].disabled = True
#                 return form
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def form_valid(self, form):
#                 try:
#                     with transaction.atomic():
#
#                         doc = self.model_id
#                         existencia = None
#                         producto = form.cleaned_data['producto']
#                         estado = form.cleaned_data['estado']
#                         cantidad = form.cleaned_data['cantidad']
#                         ueb = doc.ueb
#                         departamento = doc.departamento
#                         fecha_documento = doc.fecha
#
#                         # Validación de existencia
#                         if doc.tipodocumento.operacion == OperacionDocumento.SALIDA:
#                             existencia = valida_existencia_producto(
#                                 doc,
#                                 producto,
#                                 estado,
#                                 cantidad,
#                                 -1
#                             )
#                             if existencia is None:
#                                 form.add_error(None, "No se puede dar salida a esa cantidad")
#                                 return self.form_invalid(form)
#
#                         # Guardar DocumentoDetalle
#                         self.object = form.save(commit=False, doc=doc, existencia=existencia)
#                         setattr(self.object, self.inline_field, self.model_id)
#                         self.object.save()
#
#                         # Si el documento es "Recepción de Producción", generar registros en DocumentoDetalleProductoNC
#                         if self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION:
#                             producto_documento = self.object.producto  # Producto del DocumentoDetalle
#                             precio_producto = dame_precio_salida(producto_documento, self.object.estado,
#                                                                  self.object.documento)
#                             # Buscar NormaConsumo asociadas al producto del DocumentoDetalle
#                             normas_consumo = NormaConsumo.objects.filter(
#                                 producto=producto_documento,
#                                 activa=True,
#                                 confirmada=True
#                             ).prefetch_related('normaconsumodetalle_normaconsumo').first()  # Optimización
#
#                             dicc_exist_nc = {}
#
#                             # Iterar sobre cada NormaConsumo y sus detalles
#                             if normas_consumo:
#                                 for detalle_norma in normas_consumo.normaconsumodetalle_normaconsumo.all():
#                                     # Calcular cantidad (ejemplo)
#                                     base_norma = normas_consumo.cantidad
#                                     if base_norma <= 0:
#                                         raise ValueError(f"La cantidad base de la norma {normas_consumo.id} no puede ser cero")
#
#                                     cantidad_calculada = (
#                                         Decimal(self.object.cantidad) *
#                                         detalle_norma.norma_ramal /
#                                         Decimal(base_norma)
#                                     ).quantize(Decimal('0.000000'))
#                                     precio_producto = dame_precio_salida(detalle_norma.producto, self.object.estado,
#                                                        self.object.documento)
#                                     existencia = valida_existencia_producto(self.object.documento, detalle_norma.producto,
#                                                                             self.object.estado, cantidad_calculada, -1)
#                                     if not existencia:
#                                         form.add_error(None, f"No hay existencias de materia prima para producir {self.object.cantidad:,.2f} del producto {self.object.producto}")
#                                         self.object.delete()
#                                         return self.form_invalid(form)
#
#                                     dicc_exist_nc[detalle_norma.producto] = {'existencia': existencia, 'precio': precio_producto}
#                                     # Crear/actualizar DocumentoDetalleProductoNC
#                                     DocumentoDetalleProductoNC.objects.update_or_create(
#                                         documentodetalle=self.object,
#                                         normaconsumodetalles=detalle_norma,
#                                         defaults={
#                                             'existencia': existencia,
#                                             'estado': self.object.estado,
#                                             'precio': precio_producto,
#                                             'cantidad': cantidad_calculada,
#                                             'importe': cantidad_calculada * precio_producto,
#                                         }
#                                     )
#
#                                 if normas_consumo.normaconsumodetalle_normaconsumo.filter(operativo=1).count()>0:
#                                     normas_operativas = NormaOperativaDetalle.objects.filter(
#                                         normaoperativaproducto__producto=producto,
#                                         normaoperativaproducto__normaoperativa__fecha=fecha_documento,
#                                         normaoperativaproducto__normaoperativa__ueb=ueb
#                                     ).select_related('normaoperativaproducto__normaoperativa').distinct()
#
#                                     if normas_operativas.exists():
#                                         # DocumentoDetalleProductoNO.objects.filter(documentodetalle=self.object).delete()
#                                         # Preparar listas para bulk_create
#                                         nuevos_registros = []
#                                         orden = 1
#                                         for detalle in normas_operativas:
#
#                                             nuevos_registros.append(
#                                                 DocumentoDetalleProductoNO(
#                                                     documentodetalle=self.object,
#                                                     normaoperativadetalle=detalle,
#                                                     existencia=dicc_exist_nc[detalle.producto]['existencia'],
#                                                     cantidad=0.0,
#                                                     estado=self.object.estado,
#                                                     precio=dicc_exist_nc[detalle.producto]['precio'],
#                                                     orden=orden
#                                                 )
#                                             )
#                                             orden += 1
#                                         # Crear todos los registros en una sola operación
#                                         if nuevos_registros:
#                                             DocumentoDetalleProductoNO.objects.bulk_create(nuevos_registros)
#                             else:
#                                 self.object.importe = Decimal(precio_producto) * Decimal(self.object.cantidad)
#
#                 except IntegrityError as e:
#                     # Maneja el error de integridad (duplicación de campos únicos)
#                     mess_error = self.integrity_error
#
#                 return super().form_valid(form)
#
#         return CreateView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#             integrity_error = "El producto ya existe para el documento!"
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 doc = self.model_id
#                 if self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION:
#                     base_filter = DocumentoDetalleProductoNC.objects.filter(
#                         documentodetalle=self.object,
#                         normaconsumodetalles__normaconsumo__producto=self.object.producto.id
#                     )
#
#                     normac = base_filter.exists()
#                     normaop = base_filter.filter(normaconsumodetalles__operativo=True).exists()
#
#                     context['fecha_normaoperativa'] = get_DateNormaOperativa(self.object)
#
#                     inlines = context['inlines'].copy()  # Trabajamos con una copia para evitar efectos secundarios
#
#                     # Manejo de NC (siempre primero)
#                     nc_en_lista = DocumentoDetalleProductoNCHtmxCRUD in inlines
#
#                     if normac:
#                         if not nc_en_lista:
#                             inlines.insert(0, DocumentoDetalleProductoNCHtmxCRUD)  # NC siempre primero
#                         elif inlines[0] != DocumentoDetalleProductoNCHtmxCRUD:  # Asegurar posición
#                             inlines.remove(DocumentoDetalleProductoNCHtmxCRUD)
#                             inlines.insert(0, DocumentoDetalleProductoNCHtmxCRUD)
#
#                         # Manejo de NO (después de NC)
#                         no_en_lista = DocumentoDetalleProductoNOHtmxCRUD in inlines
#                         if normaop and not no_en_lista:
#                             inlines.append(DocumentoDetalleProductoNOHtmxCRUD)  # NO se agrega al final
#                         elif not normaop and no_en_lista:
#                             inlines.remove(DocumentoDetalleProductoNOHtmxCRUD)
#                     else:
#                         # Eliminar ambos si no hay normac
#                         if nc_en_lista:
#                             inlines.remove(DocumentoDetalleProductoNCHtmxCRUD)
#                         if DocumentoDetalleProductoNOHtmxCRUD in inlines:
#                             inlines.remove(DocumentoDetalleProductoNOHtmxCRUD)
#
#                     context['inlines'] = inlines  # Actualizar contexto
#                 else:
#                     # Eliminamos ambos cuando no es el tipo de documento adecuado
#                     context['inlines'] = [
#                         inline for inline in context['inlines']
#                         if inline not in (DocumentoDetalleProductoNCHtmxCRUD, DocumentoDetalleProductoNOHtmxCRUD)
#                     ]
#                 if(self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO):
#                     if(DocumentoDetalleReprocesoHtmxCRUD not in context['inlines']):
#                         context['inlines'].append(DocumentoDetalleReprocesoHtmxCRUD)
#                 else:
#                     if(DocumentoDetalleReprocesoHtmxCRUD in context['inlines']):
#                         context['inlines'].remove(DocumentoDetalleReprocesoHtmxCRUD)
#                 return context
#
#             def form_valid(self, form):
#                 try:
#                     with transaction.atomic():
#                         doc = self.model_id
#
#                         # Validación según el tipo de operación del documento.
#                         existencia = (
#                             None if doc.tipodocumento.operacion == OperacionDocumento.ENTRADA
#                             else valida_existencia_producto(
#                                     doc,
#                                     form.cleaned_data['producto'],
#                                     form.cleaned_data['estado'],
#                                     form.cleaned_data['cantidad'], -1
#                             )
#                         )
#                         if doc.tipodocumento.operacion == OperacionDocumento.SALIDA and existencia is None:
#                             mess_error = "No se puede dar salida a esa cantidad"
#                             form.add_error(None, mess_error)
#                             return self.form_invalid(form)
#
#                         # Si estamos en UPDATE obtenemos la instancia original para comparar el producto
#                         old_instance = None
#                         if hasattr(self, 'object') and self.object.pk:
#                             old_instance = self.object.__class__.objects.get(pk=self.object.pk)
#
#                         # Guardamos el objeto (ya sea en creación o actualización)
#                         self.object = form.save(commit=False, doc=doc, existencia=existencia)
#                         setattr(self.object, self.inline_field, self.model_id)
#
#                         # Si es actualización y el producto ha cambiado, eliminar los registros anteriores
#                         if old_instance and (old_instance.producto != self.object.producto):
#                             DocumentoDetalleProductoNC.objects.filter(documentodetalle=old_instance).delete()
#
#                         self.object.save()
#
#                         # Si el documento es "Recepción de Producción", generar o actualizar los registros asociados
#                         if self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION:
#                             if old_instance and (old_instance.producto != self.object.producto):
#                                 aaaa = 1
#                             producto_documento = self.object.producto  # producto actual del DocumentoDetalle
#                             normas_consumo = NormaConsumo.objects.filter(
#                                 producto=producto_documento,
#                                 activa=True,
#                                 confirmada=True
#                             ).prefetch_related('normaconsumodetalle_normaconsumo').first()  # optimización
#                             sum_NO_cantidad = DocumentoDetalleProductoNO.objects.filter(
#                                 documentodetalle=self.object
#                             ).aggregate(total=Coalesce(Sum('cantidad'), Decimal('0')))['total']
#                             if normas_consumo:
#                                 for detalle_norma in normas_consumo.normaconsumodetalle_normaconsumo.all():
#                                     base_norma = normas_consumo.cantidad
#                                     if base_norma <= 0:
#                                         raise ValueError(f'La cantidad base de la norma {normas_consumo.id} no puede ser cero')
#                                     cant = self.object.cantidad
#                                     if(detalle_norma.operativo):
#                                         cant = cant-sum_NO_cantidad
#                                     cantidad_calculada = (
#                                         Decimal(cant) *
#                                         detalle_norma.norma_ramal /
#                                         Decimal(base_norma)
#                                     ).quantize(Decimal('0.000000'))
#                                     precio_producto = dame_precio_salida(detalle_norma.producto, self.object.estado,
#                                                                          self.object.documento)
#                                     existencia = valida_existencia_producto(self.object.documento,
#                                                                             detalle_norma.producto,
#                                                                             self.object.estado, cantidad_calculada, -1)
#                                     if not existencia:
#                                         form.add_error(None,
#                                                        f"No hay existencias de materia prima para producir {self.object.cantidad:,.2f} del producto {self.object.producto}")
#                                         return self.form_invalid(form)
#                                     #aquiiii
#                                     DocumentoDetalleProductoNC.objects.update_or_create(
#                                         documentodetalle=self.object,
#                                         normaconsumodetalles=detalle_norma,
#                                         defaults={
#                                             'existencia': existencia,
#                                             'estado': self.object.estado,
#                                             'precio': precio_producto,
#                                             'cantidad': cantidad_calculada,
#                                             'importe': cantidad_calculada * precio_producto,
#                                         }
#                                     )
#                             else:
#                                 precio_producto = dame_precio_salida(producto_documento, self.object.estado,
#                                                                      self.object.documento)
#                                 self.object.precio = precio_producto
#                                 self.object.importe = precio_producto * self.object.cantidad
#                 except IntegrityError as e:
#                     # Maneja el error de integridad (duplicación de campos únicos)
#                     mess_error = self.integrity_error
#
#                 return super().form_valid(form)
#
#         return OEditView
#
#     def get_delete_view(self):
#         delete_view = super().get_delete_view()
#
#         class DeleteView(delete_view):
#
#             def get_context_data(self, **kwargs):
#                 context = super(DeleteView, self).get_context_data(**kwargs)
#                 context['base_model'] = self.model_id
#                 context['inline_model'] = self.object
#                 context['name'] = self.name
#                 context['views_available'] = self.views_available
#                 if self.model_id:
#                     url_father = self.base_model.get_absolute_url(self=self.model_id)
#                 else:
#                     url_father = self.get_success_url()
#                 context['url_father'] = url_father
#                 return context
#
#             def get(self, request, *args, **kwargs):
#                 self.model_id = get_object_or_404(
#                     self.base_model, pk=kwargs['model_id'])
#                 return super().get(self, request, *args, **kwargs)
#
#             def get_success_url(self):
#                 return super().get_success_url()
#
#             def post(self, request, *args, **kwargs):
#                 self.model_id = get_object_or_404(
#                     self.base_model, pk=kwargs['model_id']
#                 )
#                 doc = self.model_id
#                 detalle = DocumentoDetalle.objects.get(pk=self.kwargs['pk'])
#                 producto = detalle.producto
#                 estado = detalle.estado
#                 cantidad = detalle.cantidad
#                 existencia = detalle.existencia
#                 operacion = detalle.operacion
#                 existencia_product = existencia - (cantidad * operacion)
#                 actualiza_existencias_documentos(doc, producto, estado, existencia_product)
#                 return super().post(request, *args, **kwargs)
#
#         return DeleteView
#
#     def get_detail_view(self):
#         detail = super().get_detail_view()
#
#         class DetailView(detail):
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "doc": self.model_id,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 if self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION:
#                     base_filter = DocumentoDetalleProductoNC.objects.filter(
#                         documentodetalle=self.object,
#                         normaconsumodetalles__normaconsumo__producto=self.object.producto.id
#                     )
#
#                     normac = base_filter.exists()
#                     normaop = base_filter.filter(normaconsumodetalles__operativo=True).exists()
#
#                     context['fecha_normaoperativa'] = get_DateNormaOperativa(self.object)
#
#                     inlines = context['inlines'].copy()  # Trabajamos con una copia para evitar efectos secundarios
#
#                     # Manejo de NC (siempre primero)
#                     nc_en_lista = DocumentoDetalleProductoNCHtmxCRUD in inlines
#
#                     if normac:
#                         if not nc_en_lista:
#                             inlines.insert(0, DocumentoDetalleProductoNCHtmxCRUD)  # NC siempre primero
#                         elif inlines[0] != DocumentoDetalleProductoNCHtmxCRUD:  # Asegurar posición
#                             inlines.remove(DocumentoDetalleProductoNCHtmxCRUD)
#                             inlines.insert(0, DocumentoDetalleProductoNCHtmxCRUD)
#
#                         # Manejo de NO (después de NC)
#                         no_en_lista = DocumentoDetalleProductoNOHtmxCRUD in inlines
#                         if normaop and not no_en_lista:
#                             inlines.append(DocumentoDetalleProductoNOHtmxCRUD)  # NO se agrega al final
#                         elif not normaop and no_en_lista:
#                             inlines.remove(DocumentoDetalleProductoNOHtmxCRUD)
#                     else:
#                         # Eliminar ambos si no hay normac
#                         if nc_en_lista:
#                             inlines.remove(DocumentoDetalleProductoNCHtmxCRUD)
#                         if DocumentoDetalleProductoNOHtmxCRUD in inlines:
#                             inlines.remove(DocumentoDetalleProductoNOHtmxCRUD)
#
#                     context['inlines'] = inlines  # Actualizar contexto
#                 else:
#                     # Eliminamos ambos cuando no es el tipo de documento adecuado
#                     context['inlines'] = [
#                         inline for inline in context['inlines']
#                         if inline not in (DocumentoDetalleProductoNCHtmxCRUD, DocumentoDetalleProductoNOHtmxCRUD)
#                     ]
#
#                 if(self.model_id.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO):
#                     if(DocumentoDetalleReprocesoHtmxCRUD not in context['inlines']):
#                         context['inlines'].append(DocumentoDetalleReprocesoHtmxCRUD)
#                 else:
#                     if(DocumentoDetalleReprocesoHtmxCRUD in context['inlines']):
#                         context['inlines'].remove(DocumentoDetalleReprocesoHtmxCRUD)
#                 return context
#
#         return DetailView
#
#
# # ------ Documento / CRUD ------
# class DocumentoCRUD(CommonCRUDView):
#     model = Documento
#
#     template_name_base = 'app_index/flujo'
#
#     partial_template_name_base = 'app_index/flujo/partials'
#
#     namespace = 'app_index:flujo'
#
#     fields = [
#         'fecha',
#         'numerocontrol',
#         'numeroconsecutivo',
#         'suma_importe',
#         'observaciones',
#         'estado',
#         'reproceso',
#         'editar_nc',
#         'comprob',
#         'departamento',
#         'tipodocumento',
#         'ueb',
#     ]
#
#     add_form = DocumentoForm
#     update_form = DocumentoForm
#     detail_form = DocumentoDetailForm
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     views_available = ['list', 'update', 'create', 'delete', 'detail']
#     view_type = ['list', 'update', 'create', 'delete', 'detail']
#
#     filterset_class = DocumentoFilter
#
#     # Table settings
#     paginate_by = 25
#     table_class = DocumentoTable
#
#     inlines = [DocumentoDetalleHtmxCRUD]
#
#     # htmx
#     hx_target = '#table_content_documento_swap'
#     hx_swap = 'outerHTML'
#     hx_form_target = '#dialog'
#     hx_form_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#
#     def get_create_view(self):
#         view = super().get_create_view()
#
#         class OCreateView(view):
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 departamento = self.request.GET.get('departamento', None)
#                 if not departamento and 'departamento' in self.request.POST.keys():
#                     departamento = self.request.POST.get('departamento')
#
#                 dpto = Departamento.objects.get(pk=departamento)
#                 fecha_procesamiento = dame_fecha(ueb=self.request.user.ueb, departamento=dpto) if dpto else ''
#                 if not fecha_procesamiento:
#                     fecha_procesamiento = date.today().replace(day=1)
#
#                 tipo_doc = self.request.GET.get('tipo_doc', None)
#                 if not tipo_doc and 'tipodocumento' in self.request.POST.keys():
#                     tipo_doc = self.request.POST.get('tipodocumento')
#                 form_kwargs.update(
#                     {
#                         "user": self.request.user,
#                         "departamento": departamento,
#                         "tipo_doc": tipo_doc,
#                         "fecha_procesamiento": fecha_procesamiento,
#                     }
#                 )
#                 return form_kwargs
#
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data(**kwargs)
#                 params_hx = ''
#                 if self.request.method == 'GET':
#                     dep = self.request.GET.get('departamento', None)
#                     tipo_doc = self.request.GET.get('tipo_doc', None)
#                 elif self.request.method == 'POST':
#                     dep = self.request.POST.get('departamento', None)
#                     tipo_doc = self.request.POST.get('tipodocumento', None)
#                 departamento = Departamento.objects.get(pk=dep) if dep else None
#                 tipodocumento = TipoDocumento.objects.get(pk=tipo_doc) if tipo_doc else None
#                 title = 'Departamento: %s | Documento: %s' % (departamento, tipodocumento)
#                 if self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
#                     params_hx = '?' + self.request.htmx.current_url_abs_path.split('?')[1]
#                 ctx.update({
#                     'modal_form_title': title,
#                     "hx_target": '#table_content_documento_swap',
#                     'max_width': '1250px',
#                     'getparams_hx': params_hx,
#                 })
#                 return ctx
#
#             def get_success_url(self):
#                 return super().get_success_url()
#
#             def form_valid(self, form):
#                 try:
#                     return super().form_valid(form)
#                 except IntegrityError as e:
#                     # Maneja el error de integridad (duplicación de campos únicos)
#                     mess_error = NumeracionDocumentos.objects_cache.get_cached_data()[
#                             TipoNumeroDoc.NUMERO_CONSECUTIVO if e.args[0].find(
#                                 'numeroconsecutivo') > 0 else TipoNumeroDoc.NUMERO_CONTROL]['mensaje_error']
#                     form.add_error(None, mess_error)
#                     return self.form_invalid(form)
#                 except Exception as e:
#                     form.add_error(None, 'Existe un error al salvar los datos')
#                     return self.form_invalid(form)
#
#             def form_invalid(self, form, **kwargs):
#                 tipodocumento = form.cleaned_data['tipodocumento']
#                 if tipodocumento.id == ChoiceTiposDoc.TRANSFERENCIA_EXTERNA:
#                     form.fields['ueb_destino'].widget.attrs.update({
#                         'style': 'width: 100%; display: block;'
#                     })
#                     form.fields['departamento_destino'].widget.attrs['style'] = 'width: 100%; display: block;'
#
#                 return super().form_invalid(form, **kwargs)
#
#         return OCreateView
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             dep = None
#             fecha_procesamiento = None
#             fecha_procesamiento_range = None
#
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 error_msg = ""
#                 no_data_msg = ""
#                 dep_queryset = context['form'].fields['departamento'].queryset
#                 ueb = self.request.user.ueb
#                 dep_queryset = dep_queryset.filter(unidadcontable=ueb)
#                 context['form'].fields['departamento'].queryset = dep_queryset
#                 tiposdoc = TipoDocumento.objects.filter(generado=False)
#                 tipo_doc_entrada = tiposdoc.filter(operacion=OperacionDocumento.ENTRADA)
#                 tipo_doc_salida = tiposdoc.filter(operacion=OperacionDocumento.SALIDA)
#                 dpto = dep_queryset.get(pk=self.dep) if self.dep else None
#                 htmx_departamento_trigger = False
#                 fecha_procesamiento = dame_fecha(ueb, dpto) if dpto else ''
#                 if fecha_procesamiento:
#                     context['form'].fields['rango_fecha'].widget.picker_options['custom_ranges'] = {
#                         'Fecha procesamiento': (
#                             fecha_procesamiento.strftime('%d/%m/%Y'), fecha_procesamiento.strftime('%d/%m/%Y')),
#                     }
#                     context['form'].initial['rango_fecha'] = (
#                         fecha_procesamiento.strftime('%d/%m/%Y'), fecha_procesamiento.strftime('%d/%m/%Y'))
#                 if self.request.htmx.trigger_name == 'departamento':
#                     htmx_departamento_trigger = True
#                 inicializado = False if not self.dep else dpto.inicializado(ueb)
#                 if not inicializado:
#                     tipo_doc_entrada = tipo_doc_entrada.filter(pk=ChoiceTiposDoc.CARGA_INICIAL)
#                 else:
#                     tipo_doc_entrada = tipo_doc_entrada.exclude(pk=ChoiceTiposDoc.CARGA_INICIAL)
#
#                 tableversat = DocumentosVersatTable([])
#                 url_docversat = None
#                 if not inicializado and self.dep:
#                     tableversat.empty_text = 'El departamento "%s" no se ha inicializado' % dpto
#
#                 if not self.dep:
#                     tableversat.empty_text = "Seleccione un departamento"
#
#                 if self.dep and inicializado:
#                     dpto = self.request.GET.get('departamento', None)
#                     datostableversat = dame_documentos_versat(self.request, dpto if dpto else self.dep)
#                     tableversat = DocumentosVersatTable([]) if datostableversat is None else DocumentosVersatTable(
#                         datostableversat)
#                     if 'actions' in tableversat.col_vis:
#                         tableversat.col_vis.remove('actions')
#
#                     tableversat.empty_text = "Error de conexión con la API Versat para obtener los datos" if datostableversat == None else "No hay datos para mostrar"
#                     DepartamentoDocumentosForm(initial={'departamento': self.dep})
#                     url_docversat = reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:'))
#
#                 tipo_doc_entrada = tipo_doc_entrada.filter(departamento_documentosentrada__id = self.dep)
#                 tipo_doc_salida = tipo_doc_salida.filter(departamento_documentossalida__id = self.dep)
#                 context.update({
#                     'filter': False,
#                     'select_period': True,
#                     'period_form': DepartamentoDocumentosForm(initial={'departamento': self.dep}),
#                     'tableversat': tableversat if tableversat else None,
#                     "hx_get": reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
#                     "hx_target": '#table_content_documento_swap',
#                     "hx_swap":'outerHTML',
#                     "col_vis_hx_include": "[name='departamento'], [name='rango_fecha']",
#                     'create_link_menu': True,
#                     'url_docversat': url_docversat,
#                     'hay_departamento': not self.dep is None,
#                     'tipo_doc_entrada': tipo_doc_entrada,
#                     'tipo_doc_salida': tipo_doc_salida,
#                     'hay_documentos': tipo_doc_salida or tipo_doc_entrada,
#                     'inicializado': inicializado,
#                     'confirm': True,
#                     'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
#                     'texto_generatransferencia': "Se generará un documento de transferencia con los productos de este documento",
#                     'texto_inicializar': "Una vez inicializado el departamento, podrá realizar acciones en él.",
#                     'fecha_procesamiento': fecha_procesamiento,
#                     'htmx_departamento_trigger': htmx_departamento_trigger,
#                 })
#                 return context
#
#             def get_queryset(self):
#                 qdict = {}
#                 queryset = super().get_queryset()
#                 formating = '%d/%m/%Y'
#                 ueb = self.request.user.ueb
#                 self.dep = self.request.GET.get('departamento', None)
#                 dpto = Departamento.objects.get(pk=self.dep) if self.dep else None
#                 rango_fecha = self.request.GET.get('rango_fecha', None)
#                 queryset = queryset.filter(ueb=ueb)
#                 if self.dep == '' or self.dep is None:
#                     return self.model.objects.none()
#                 return queryset
#
#             def get(self, request, *args, **kwargs):
#                 ueb = self.request.user.ueb
#                 self.dep = self.request.GET.get('departamento', None)
#                 rango_fecha = self.request.GET.get('rango_fecha', "")
#                 dpto = Departamento.objects.get(pk=self.dep) if self.dep else None
#                 self.fecha_procesamiento_range = ''
#                 self.fecha_procesamiento = dame_fecha(ueb, dpto) if dpto else ''
#                 if self.fecha_procesamiento:
#                     self.fecha_procesamiento_range = self.fecha_procesamiento.strftime(
#                         '%d/%m/%Y') + ' - ' + self.fecha_procesamiento.strftime(
#                         '%d/%m/%Y')
#
#                 trigger_name = self.request.htmx.trigger_name
#                 if self.request.htmx.triggering_event:
#                     triggering_event = self.request.htmx.triggering_event['type'] if 'type' in self.request.htmx.triggering_event else None
#
#                 request.GET = request.GET.copy()
#                 if trigger_name == 'departamento':
#                     request.GET['rango_fecha'] = self.fecha_procesamiento_range
#                 if (trigger_name == 'rango_fecha' and rango_fecha == "") or (trigger_name == 'rango_fecha' and triggering_event == "process_date"):
#                     request.GET['rango_fecha'] = self.fecha_procesamiento_range
#                 return super().get(request, *args, **kwargs)
#
#         return OFilterListView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#
#             def get_context_data(self, **kwargs):
#                 ctx = super(OEditView, self).get_context_data(**kwargs)
#                 if self.inlines:
#                     for inline in self.inlines:
#                         if 'actions' in inline.table_class.col_vis:
#                             inline.table_class.col_vis.remove('actions')
#                 title = 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
#                 ctx.update({
#                     'modal_form_title': title,
#                     'max_width': '1250px',
#                     'hx_target': '#table_content_documento_swap',
#                     'confirm': True,
#                     'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
#                     'object_model': self.model,
#                 })
#                 return ctx
#
#             def form_valid(self, form):
#                 try:
#                     return super().form_valid(form)
#                 except IntegrityError as e:
#                     # Maneja el error de integridad (duplicación de campos únicos)
#                     mess_error = NumeracionDocumentos.objects_cache.get_cached_data()[
#                         TipoNumeroDoc.NUMERO_CONSECUTIVO if e.args[0].find(
#                             'numeroconsecutivo') > 0 else TipoNumeroDoc.NUMERO_CONTROL]['mensaje_error']
#                     form.add_error(None, mess_error)
#                     return self.form_invalid(form)
#
#         return OEditView
#
#     def get_delete_view(self):
#         view = super().get_delete_view()
#
#         class ODeleteView(view):
#
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data(**kwargs)
#                 ctx.update({
#                     'hx_target': '#table_content_documento_swap',
#                     'hx-swap': 'outerHTML',
#                 })
#
#                 return ctx
#
#             @transaction.atomic
#             def post(self, request, *args, **kwargs):
#                 self.object = self.get_object()
#                 get_params = request.META.get('QUERY_STRING', '')
#                 try:
#                     doc = self.object
#                     control = doc.get_numerocontrol()
#                     consecutivo = doc.numeroconsecutivo
#                     self.object.delete()
#                     transaction.on_commit(lambda: renumerar_documentos(doc.ueb, doc.departamento, consecutivo, control))
#                     transaction.on_commit(lambda: actualiza_numeros(doc.ueb, doc.departamento, None, control, None))
#                 except ProtectedError as e:
#                     protected_details = ", ".join([str(obj) for obj in e.protected_objects])
#                     title = 'No se puede eliminar '
#                     text = 'Este elemento contiene o está relacionaco con: \n'
#                     message_error(self.request,
#                                   title + self.object.__str__() + '!',
#                                   text=text + protected_details)
#                     sweetify.error(self.request, title + self.object.__str__() + '!', text=text + protected_details,
#                                    persistent=True)
#                     return HttpResponseRedirect(self.get_success_url())
#                 if self.success_message:
#                     sweetify.success(self.request, self.success_message)
#                 return HttpResponseLocation(
#                     reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + "?" + get_params,
#                     target='#table_content_documento_swap',
#                     headers={
#                         'HX-Trigger': request.htmx.trigger,
#                         'HX-Trigger-Name': request.htmx.trigger_name,
#                         'event_action': 'confirmed',
#                     }
#                 )
#         return ODeleteView
#
#     def get_detail_view(self):
#         view = super().get_detail_view()
#
#         class ODetailView(view):
#             hx_target = self.hx_target
#             hx_swap = self.hx_swap
#             hx_form_target = self.hx_form_target
#             hx_form_swap = self.hx_form_swap
#             modal = self.modal
#
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data()
#                 if self.inlines:
#                     for inline in self.inlines:
#                         if 'actions' in inline.table_class.col_vis:
#                             inline.table_class.col_vis.remove('actions')
#                 title = 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
#                 ctx.update({
#                     'modal_form_title': title,
#                     'max_width': '1250px',
#                     'hx_target': '#table_content_documento_swap',
#                     'object_model': self.model,
#                 })
#                 return ctx
#
#         return ODetailView
#
#
# @transaction.atomic
# def confirmar_documento(request, pk):
#     # Para confirmar un documento se valida:
#     #  - que contenga detalles
#     #  - que no existan documentos en edición anteriores a él, que el umtimo consecutivo confirmado sea el anterior a su numero
#     # Procedimiento
#     #  - Despues de validar y todo ok se procede a la confirmación
#     #  - Si actualizan las existencias
#     #  - Si es un documento de entrada se actualiza el precio
#     #  - Si el documento lo requiere se genera el documento en el destino
#     get_params = request.META.get('QUERY_STRING', '')
#     obj = Documento.objects.select_for_update().get(pk=pk)
#     departamento = obj.departamento
#     ueb = obj.ueb
#     detalles = obj.documentodetalle_documento.all()
#     detalles_count = detalles.count()
#     if detalles_count > 0 and not existen_documentos_sin_confirmar(obj) and not obj.error:
#         valido = True
#         detalles_transf = None
#         otros_detalles = []
#         otros_detalles_nc = []
#         detalles_transf = []
#         match obj.tipodocumento.pk:
#             case ChoiceTiposDoc.CAMBIO_PRODUCTO:
#                 otros_detalles = DocumentoDetalleProducto.objects.filter(documentodetalle__documento=obj)
#             case ChoiceTiposDoc.CAMBIO_ESTADO:
#                 otros_detalles = DocumentoDetalleEstado.objects.filter(documentodetalle__documento=obj)
#             case ChoiceTiposDoc.TRANSF_HACIA_DPTO:
#                 new_tipo = ChoiceTiposDoc.TRANSF_DESDE_DPTO
#                 departamento = obj.documentotransfdepartamento_documento.get().departamento
#                 new_doc = crea_documento_generado(ueb, departamento, new_tipo)
#                 DocumentoTransfDepartamentoRecibida.objects.create(documento=new_doc, documentoorigen=obj)
#                 # crear el documento de entrada en el destino
#                 crea_detalles_generado(new_doc, detalles)
#                 detalles_transf = obj.documentodetalle_documento.all()
#             case ChoiceTiposDoc.RECEPCION_PRODUCCION:
#                 existen_no = dame_noperativa_sispax(request, '2024-01-29')
#                 if not existen_no:
#                     mensaje_error = "Error del conexión con el sistema Sispax. No se han podido verificar las Normas Operativas"
#                     valido = False
#                 else:
#                     otros_detalles_nc = DocumentoDetalleProductoNC.objects.filter(
#                         documentodetalle__documento=obj,
#                         cantidad__gt=0)
#                     valido, errores = valida_recepcion_produccion(otros_detalles_nc.filter(normaconsumodetalles__operativo=True))
#                     mensaje_error = f"<ul style='text-align: left;'>{''.join(errores)}</ul>"
#                     if valido:
#                         otros_detalles = DocumentoDetalleProductoNO.objects.filter(documentodetalle__documento=obj,
#                                                                                cantidad__gt=0)
#         if valido:
#             obj.estado = EstadosDocumentos.CONFIRMADO  # Confirmado
#             obj.save()
#             actualizar_existencias(ueb, departamento, detalles, obj.fecha.year, obj.fecha.month)
#
#             if detalles_transf:
#                 actualizar_existencias(ueb, obj.departamento, obj.documentodetalle_documento.all(), obj.fecha.year, obj.fecha.month)
#
#             if otros_detalles:
#                 actualizar_existencias(ueb, departamento, otros_detalles, obj.fecha.year, obj.fecha.month, True)
#
#             if otros_detalles_nc:
#                 actualizar_existencias(ueb, departamento, otros_detalles_nc, obj.fecha.year, obj.fecha.month)
#
#             title = 'Confirmación terminada'
#             text = 'El Documento %s - %s se confirmó satisfactoriamente !' % (obj.numeroconsecutivo, obj.tipodocumento)
#             sweetify.success(request, title, text=text, persistent=True)
#         else:
#             title = 'No puede ser confirmado el documento '
#             sweetify.error(
#                 request,
#                 title,
#                 persistent=True,
#                 html=mensaje_error,
#             )
#     else:
#         title = 'No puede ser confirmado el documento '
#         text = 'No tiene productos asociados' if detalles_count <= 0 else 'Existen documentos anteriores a él sin Confirmar'
#         text = 'Este documento contiene errores' if obj.error else text
#         sweetify.error(request, title + obj.__str__() + ' (' + str(obj.numeroconsecutivo) + ') ' + '!', text=text,
#                        persistent=True)
#     return HttpResponseLocation(
#         reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + "?" + get_params,
#         target='#table_content_documento_swap',
#         headers={
#             'HX-Trigger': request.htmx.trigger,
#             'HX-Trigger-Name': request.htmx.trigger_name,
#             'event_action': 'confirmed',
#         }
#     )
#
# @transaction.atomic
# def crear_transf_produccion(kwargs):
#     """
#     Crear documento de transferencia
#     """
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'El documento fue creado',
#         'error_title': 'El documento no fue creado',
#         'persistent': True,
#     }
#     iddocumento = kwargs['iddocumento']
#     departamento_destino = kwargs['departamento_destino']
#
#     detalles = DocumentoDetalle.objects.filter(documento=iddocumento)
#
#     request = kwargs['request']
#
#     departamento = ''
#     if request.htmx.current_url_abs_path and 'departamento' in request.htmx.current_url_abs_path:
#         departamento = request.htmx.current_url_abs_path.split('&')[1].split('=')[1] #este es el id del dpto
#
#     detalles_generados = []
#
#     new_tipo = ChoiceTiposDoc.TRANSF_HACIA_DPTO
#     departamento = detalles[0].documento.departamento
#
#     claseproducto, tipoproducto = dame_productos_departamento(departamento_destino, OperacionDocumento.ENTRADA)
#
#     productos_transf = detalles.filter(Q(producto__productoflujoclase_producto__clasemateriaprima_id__in=claseproducto) | Q(
#         producto__tipoproducto__in=tipoproducto))
#
#     if len(productos_transf) == 0:
#         func_ret.update({
#             'success': False,
#             'error_title': 'El documento no fue creado, los productos a transferir no se admiten en el departamento destino',
#         })
#         return func_ret
#
#     if len(productos_transf) != len(detalles):
#         func_ret.update({
#             'success_title': 'El documento fue creado, pero algunos productos a transferir no se admiten en el departamento destino',
#         })
#
#     new_doc = crea_documento_generado(request.user.ueb, departamento, new_tipo, True)
#     for p in productos_transf:
#         precio = dame_precio_salida(p.producto, p.estado, p.documento)
#         importe = Decimal(precio) * Decimal(p.cantidad)
#         detalles_generados.append(DocumentoDetalle(cantidad=p.cantidad,
#                                                    precio=precio,
#                                                    importe=importe,
#                                                    documento=new_doc,
#                                                    estado=p.estado,
#                                                    producto=p.producto
#                                                    ))
#     crea_detalles_generado(new_doc, detalles_generados)
#     DocumentoTransfDepartamento.objects.create(documento=new_doc, departamento=Departamento.objects.get(pk=departamento_destino.pk))
#
#     return func_ret
#
# class ObtenerDepartamentoDestinoModalFormView(BaseModalFormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = DameDptoATransfForm
#     father_view = 'app_index:flujo:flujo_documento_list'
#
#     funcname = {
#         'submitted': crear_transf_produccion,
#     }
#
#     hx_target = '#table_content_documento_swap'
#     hx_swap = 'outerHTML'
#     hx_form_target = '#dialog'
#     hx_form_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#     modal_form_title = 'Departamento Destino'
#     max_width = '850px'
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx.update({
#             'btn_aceptar': 'Generar Documento de Transferencia',
#         })
#         return ctx
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         iddocumento = self.request.GET.get('documento')
#         kwargs['initial'].update({
#             "iddocumento": iddocumento,
#         })
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         kw.update({
#             'request': self.request,
#             'departamento_destino': form.cleaned_data['departamento'],
#             'iddocumento': form.cleaned_data['iddocumento'],
#         })
#         return kw
#
# def valida_recepcion_produccion(detalles_nc):
#     """
#         Valida que para cada DocumentoDetalleProductoNC con norma operativa (operativo=True)
#         exista un DocumentoDetalleProductoNO correspondiente con cantidad > 0.
#
#         Args:
#             detallesnc: DocumentoDetalleProductoNC
#
#         Returns:
#             tuple: (bool, list) - (True si todo es válido, False si hay errores, lista de mensajes de error)
#         """
#     errores = []
#     valido = True
#
#     #TODO
#     # ver lo de la validacion de las Normas Operativas en el edocumento
#     # Se propone:
#     # Si al producto a producir hay asociada una NO o mas de una la suma de cada producto de la NO de las cantidades debe ser = a la cantidad a producir
#     # Si no tiene asociada una NO, buscar si hay NO definidas para el dia del documento y si hay emitir mensaje de error
#     # for detalle_nc in detalles_nc:
#     #     # Buscar si existe un detalle NO para esta norma operativa
#     #     detalles_no = DocumentoDetalleProductoNO.objects.filter(
#     #         documentodetalle=detalle_nc.documentodetalle
#     #     )
#     #
#     #     suma_cantidad = DocumentoDetalleProductoNO.objects.filter(
#     #         documentodetalle=detalle_nc.documentodetalle
#     #     ).aggregate(
#     #         total=Coalesce(Sum('cantidad'), Value(0, output_field=DecimalField()))
#     #     )['total']
#     #     if suma_cantidad == 0:
#     #         # Obtener información del producto para el mensaje de error
#     #         producto = detalle_nc.normaconsumodetalles.producto.descripcion
#     #         errores.append(
#     #             f"<li>Producto <strong>{producto}</strong>: Requiere norma operativa con cantidad > 0</li>")
#     #         valido = False
#     #     else:
#     #         #Buscar si hay NO definidas para ese día y producto.
#     #
#     #         if NormaOperativaDetalle.objects.filter(
#     #                 normaoperativaproducto__normaoperativa__fecha=detalle_nc.documentodetalle.documento.fecha,
#     #                 normaoperativaproducto__producto=detalle_nc.documentodetalle.producto
#     #             ).select_related(
#     #                 "normaoperativaproducto",
#     #                 "normaoperativaproducto__normaoperativa",
#     #                 "normaoperativaproducto__producto"
#     #             ).exists():
#     #             errores.append(
#     #                 f"<li>Existen Normas Operativas para el producto <strong>{detalle_nc.documentodetalle.producto}</strong>: que no han sido cargadas en el documento</li>")
#     #             valido = False
#     #
#     #     # Si existe, asegurarse de que el error esté marcado como False
#     #     detalle_nc.error = not valido
#     #     detalle_nc.save()
#     return valido, errores
#
# #Actualiza la tabla ExistenciaDpto
# @transaction.atomic
# def actualizar_existencias(ueb, departamento, productos, anno, mes, noperativa=False):
#     exist_dpto = ExistenciaDpto.objects.select_for_update().filter(departamento=departamento, ueb=ueb,
#                                                                    anno=anno, mes=mes)
#     actualizar_existencia = []
#     for d in productos:
#         producto = d.producto
#         estado = d.estado
#         exist = exist_dpto.filter(producto=producto, estado=estado).first()
#         inicial_exist = 0 if not exist else exist.cantidad_inicial
#         entradas_exist = 0 if not exist else exist.cantidad_entrada
#         salidas_exist = 0 if not exist else exist.cantidad_salida
#         cantidad_final_exist = 0 if not exist else exist.cantidad_final
#         operacion = 'E' if d.operacion == 1 else 'S'
#
#         precio = d.precio if not exist else exist.precio
#         cantidad = d.cantidad if not noperativa else d.cantidad_usada
#
#         if operacion == OperacionDocumento.ENTRADA and exist:  # calcular el precio promedio
#             importe = d.cantidad * d.precio
#             importe_exist = 0 if not exist else (exist.cantidad_final * exist.precio)
#             importe_t = importe + importe_exist
#             cantidad_t = cantidad + cantidad_final_exist
#             precio = importe_t / cantidad_t
#
#         cantidad_entrada = cantidad + entradas_exist if operacion == OperacionDocumento.ENTRADA else entradas_exist
#         cantidad_salida = cantidad + salidas_exist if operacion == OperacionDocumento.SALIDA else salidas_exist
#         cantidad_final = inicial_exist + cantidad_entrada - cantidad_salida
#
#         importe = cantidad_final * precio
#
#         actualizar_existencia.append(
#             ExistenciaDpto(ueb=ueb, departamento=departamento, producto=producto, estado=estado,
#                            cantidad_entrada=cantidad_entrada, cantidad_salida=cantidad_salida,
#                            cantidad_final=cantidad_final, importe=importe,
#                            precio=precio, anno=anno, mes=mes))
#
#     ExistenciaDpto.objects.bulk_update_or_create(actualizar_existencia,
#                                                  ['cantidad_entrada', 'cantidad_salida', 'precio',
#                                                   'cantidad_final', 'importe'],
#                                                  match_field=['ueb', 'departamento', 'producto', 'estado',
#                                                               'anno', 'mes'])
#     return
#
#
# def crea_documento_generado(ueb, departamento, tipodoc, rep_prod=None):
#     dicc_conf = NumeracionDocumentos.objects_cache.get_cached_data()
#     numeracion_doc_conf_consecutivo = dicc_conf[TipoNumeroDoc.NUMERO_CONSECUTIVO]
#     numeracion_doc_conf_control = dicc_conf[TipoNumeroDoc.NUMERO_CONTROL]
#     numeros = genera_numero_doc(departamento, ueb, tipodoc, numeracion_doc_conf_consecutivo, numeracion_doc_conf_control, rep_prod)
#     numerocontrol = str(numeros[1][0]) if not numeros[1][2] else  str(numeros[1][2]) + '/' + str(numeros[1][0])
#     numeroconsecutivo = numeros[0][0]
#
#     fecha = dame_fecha(ueb, departamento)
#     confconsec = ConfigNumero.DEPARTAMENTO if numeros[0][3]['departamento'] == True else ConfigNumero.UNICO
#     confcontrol = ConfigNumero.DEPARTAMENTO if numeros[1][3]['departamento'] == True else ConfigNumero.UNICO
#
#     return Documento.objects.create(fecha=fecha, numerocontrol=numerocontrol,
#                                     numeroconsecutivo=numeroconsecutivo,
#                                     departamento=departamento, tipodocumento=TipoDocumento.objects.get(pk=tipodoc),
#                                     confconsec=confconsec,
#                                     confcontrol=confcontrol, ueb=ueb)
#
#
# @transaction.atomic
# def crea_detalles_generado(doc, detalles):
#     operacion = doc.operacion
#     dicc = {'documento__estado': EstadosDocumentos.EDICION,
#             'documento__departamento': doc.departamento, 'documento__ueb': doc.ueb}
#     docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)
#     detalles_new = []
#     doc_error = False
#     for d in detalles:
#         existencia_product, hay_error = existencia_producto(
#             d.documento,
#             d.producto,
#             d.estado,
#             d.cantidad,
#             operacion)
#         d.existencia = existencia_product
#         d.error = hay_error
#         doc_error = True if hay_error else doc_error
#         d.id = uuid.uuid4()
#         d.documento = doc
#         d.operacion = operacion
#         detalles_new.append(d)
#
#     DocumentoDetalle.objects.bulk_create(detalles_new)
#     doc.error = doc_error
#     if doc_error:
#         doc.estado = EstadosDocumentos.ERRORES
#     doc.save()
#     return
#
#
# def existen_documentos_sin_confirmar(obj):
#     conf = NumeracionDocumentos.objects_cache.get_cached_data()[TipoNumeroDoc.NUMERO_CONSECUTIVO]
#     departamento = obj.departamento
#     ueb = obj.ueb
#     tipodoc = obj.tipodocumento
#     numeroconsecutivo = obj.numeroconsecutivo
#
#     docs = Documento.objects.filter(ueb=ueb, numeroconsecutivo__lt=numeroconsecutivo,
#                                     estado__in=[EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES])
#
#     if conf['departamento']:
#         doc = docs.filter(departamento=departamento)
#     else:
#         doc = docs
#
#     numero = doc.aggregate(numconsec=Max('numeroconsecutivo'))['numconsec']
#     numero = numero if numero else 0
#
#     return numero > 0
#
#
# @transaction.atomic
# def inicializar_departamento(request, pk):
#     docs = Documento.objects.filter(departamento=pk, ueb=request.user.ueb).exclude(
#         estado__in=[EstadosDocumentos.CONFIRMADO, EstadosDocumentos.CANCELADO])
#     departamento = Departamento.objects.get(pk=pk)
#     params = '?' + request.htmx.current_url_abs_path.split('?')[1]
#
#     if not docs.exists():
#         fecha_inicio, created = FechaInicio.objects.get_or_create(
#             fecha=date.today().replace(day=1),
#             departamento=departamento,
#             ueb=request.user.ueb,
#         )
#         if created:
#             cant_dias = calendar.monthrange(int(date.today().year), int(date.today().month))[1]
#             fecha_inicio, created = FechaPeriodo.objects.get_or_create(
#                 fecha=date.today().replace(day=1),
#                 departamento=departamento,
#                 ueb=request.user.ueb,
#             )
#
#             title = 'El departamento %s se inicializó correctamente para %s!' % (departamento, request.user.ueb)
#             text = 'Con fecha de inicio: %s' % date.today().replace(day=1)
#             sweetify.success(request, title, text=text, persistent=True)
#         else:
#             title = 'El departamento %s para %s ya ha sido inicializado anteriormente' % (
#                 departamento, request.user.ueb)
#             text = ''
#             sweetify.info(request, title, text=text, persistent=True)
#     else:
#         title = 'No se completó la incialización'
#         text = 'Existen documentos sin Confirmar, el departamento %s para %s no se puede inicializar' % (
#             departamento, request.user.ueb)
#         sweetify.warning(request, title, text=text, persistent=True)
#
#     return HttpResponseLocation(
#         reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + params,
#         target='#table_content_documento_swap',
#         headers={
#             'HX-Trigger': request.htmx.trigger,
#             'HX-Trigger-Name': request.htmx.trigger_name,
#             'initialized': 'true',
#         }
#     )
#
# def dame_documentos_versat(request, dpto):
#     unidadcontable = request.user.ueb
#
#     title_error = _("Couldn't connect")
#     text_error = _('Connection error to Versat API')
#
#     try:
#         dpto = Departamento.objects.get(pk=dpto)
#         if not dpto.inicializado(unidadcontable):
#             return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))
#
#         fecha_periodo = dame_fecha(unidadcontable, dpto)
#         fecha_mes_procesamiento = fecha_periodo.replace(day=1).strftime('%Y-%m-%d')
#
#         params = {'fecha_desde': fecha_mes_procesamiento,
#                   'fecha_hasta': fecha_periodo.strftime('%Y-%m-%d'),
#                   'unidad': unidadcontable.codigo,
#                   'centro_costo': dpto.centrocosto.clave
#                   }
#         response = getAPI('documentogasto', ueb=request.user.ueb.codigo, params=params)
#
#         if response and response.status_code == 200:
#             datos = response.json()['results']
#             ids = ids_documentos_versat_procesados(fecha_mes_procesamiento, fecha_periodo, dpto,
#                                                    unidadcontable) if datos else []
#             datos = list(filter(lambda x: x['iddocumento'] not in ids, datos))
#             [datos[x].update({'json_data': literal_eval(json.dumps(datos[x]))}) for x in range(len(datos))]
#             return datos
#     except Exception as e:
#         return None
#
#
# @transaction.atomic
# def valida_existencia_producto(doc, producto, estado_producto, cantidad, operacion):
#     existencia_product, hay_error = existencia_producto(doc, producto, estado_producto, cantidad, operacion)
#     return None if existencia_product < 0 else existencia_product
#
# def precioproducto(request):
#     producto = request.GET.get('producto')
#     pk_doc = request.GET.get('documento_hidden')
#     documento = Documento.objects.get(pk=pk_doc)
#     estado = request.GET.get('estado')
#     if estado and not producto:
#         producto = request.GET.getlist('producto')[0]
#
#     precio = 0.00
#     if producto and estado and (documento.tipodocumento.operacion == OperacionDocumento.SALIDA or documento.tipodocumento.pk == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO):
#         precio = dame_precio_salida(producto, estado, documento)
#
#     data = {
#         'producto': producto,
#         'precio': precio,
#         'doc': documento
#     }
#     form = DocumentoDetalleForm(data) if documento.tipodocumento.pk != ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO else DocumentoDetalleReprocesoForm(data)
#
#     response = HttpResponse(
#         as_crispy_field(form['precio']).replace('is-invalid', ''),
#         content_type='text/html'
#     )
#     return response
#
#
# @transaction.atomic
# def aceptar_documento_versat(kwargs):
#     """
#     Aceptar un documento
#     """
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'El documento fue aceptado',
#         'error_title': 'El documento no fue aceptado. Existen productos que no están en el sistema, o no coinciden las unidades de medida',
#     }
#     detalles = kwargs['detalles']
#
#     no_existen = [d for d in detalles if not d['existe_sistema']]
#     if len(no_existen) > 0:
#         func_ret.update({
#             'success': False
#         })
#     else:
#         iddocumento = kwargs['iddocumento']
#         request = kwargs['request']
#         json_data = literal_eval(kwargs['json_data'])
#         departamento = ''
#         if request.htmx.current_url_abs_path and 'departamento' in request.htmx.current_url_abs_path:
#             departamento = request.htmx.current_url_abs_path.split('&')[1].split('=')[1] #este es el id del dpto
#         dicc_detalle = {}
#         detalles_generados = []
#         for p in detalles:
#             dicc_detalle[p['producto_codigo']] = {'cantidad': p['cantidad'], 'um': p['medida_clave'].strip(),
#                                                   'precio': p['precio']}
#
#         prods = ProductoFlujo.objects.filter(codigo__in=list(dicc_detalle.keys()))
#
#         new_tipo = ChoiceTiposDoc.ENTRADA_DESDE_VERSAT
#         departamento = Departamento.objects.get(pk=departamento)
#         new_doc = crea_documento_generado(request.user.ueb, departamento, new_tipo)
#
#         for p in prods:
#             detalles_generados.append(DocumentoDetalle(cantidad=dicc_detalle[p.codigo]['cantidad'],
#                                                        precio=dicc_detalle[p.codigo]['precio'],
#                                                        importe=round(float(dicc_detalle[p.codigo]['cantidad']) *
#                                                            float(dicc_detalle[p.codigo]['precio']), 2),
#                                                        documento=new_doc,
#                                                        estado=EstadoProducto.BUENO,
#                                                        producto=p
#                                                        ))
#         crea_detalles_generado(new_doc, detalles_generados)
#         fecha = kwargs['iddocumento_fecha']
#         partes = fecha.split('/')
#         partes.reverse()
#         fecha_doc = '-'.join(partes)
#         DocumentoOrigenVersat.objects.create(documentoversat=iddocumento, documento=new_doc,
#                                              fecha_documentoversat=fecha_doc, documento_origen=json_data)
#
#     return func_ret
#
#
# @transaction.atomic
# def rechazar_documento_versat(kwargs):
#     """
#     Rechazar un documento
#     """
#
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'El documento fue rechazado',
#         'error_title': 'El documento no pudo ser rechazado. Por favor, revise',
#     }
#
#     iddocumento = kwargs['iddocumento']
#     request = kwargs['request']
#     fecha = kwargs['iddocumento_fecha']
#     partes = fecha.split('/')
#     partes.reverse()
#     fecha_doc = '-'.join(partes)
#     json_data = literal_eval(kwargs['json_data'])
#     DocumentoVersatRechazado.objects.create(documentoversat=iddocumento, fecha_documentoversat=fecha_doc,
#                                             documento_origen=json_data, ueb=request.user.ueb)
#
#     return func_ret
#
# @transaction.atomic
# def rechazar_documento(request, pk):
#     """
#     Rechazar un documento
#     """
#
#     there_is_htmx_params = request.htmx.current_url_abs_path.split('?').__len__() > 1
#     getparams_hx = '?' + request.htmx.current_url_abs_path.split('?')[1] if there_is_htmx_params else ''
#
#     doc = Documento.objects.select_for_update().get(pk=pk)
#     doc.estado = EstadosDocumentos.RECHAZADO
#     doc.save()
#
#     detalles = doc.documentodetalle_documento.all()
#
#     for d in detalles:
#         producto = d.producto
#         cantidad = d.cantidad
#         existencia = d.existencia
#         estado = d.estado
#         operacion = d.operacion
#         existencia_product = existencia - (cantidad * operacion)
#         actualiza_existencias_documentos(doc, producto, estado, existencia_product)
#
#     if doc.tipodocumento.pk != ChoiceTiposDoc.ENTRADA_DESDE_VERSAT:
#         # Si al rechazar un documento este genera otro documento
#         # Para los tipos de documentos
#         # -Transferencia desde departamento, Devolución Recibida (si se rechaza genera Devolución Recibida en el dpto que realizó la transf o dev)
#         ueb = doc.ueb
#         match doc.tipodocumento.pk:
#             case ChoiceTiposDoc.TRANSF_DESDE_DPTO:
#                 departamento_destino = doc.documentotransfdepartamentorecibida_documento.get().documentoorigen.departamento
#             case ChoiceTiposDoc.DEVOLUCION_RECIBIDA:
#                 origen = doc.documentodevolucionrecibida_documento.get()
#                 departamento_destino = origen.documentoorigen.departamento
#                 ueb = origen.documentoorigen.ueb
#             case ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA:
#                 ueb = doc.documentotransfextrecibida_documento.get().unidadcontable
#                 destino = doc.documentotransfextrecibidadocorigen_documento.get()
#                 departamento_destino = destino.documentoorigen.departamento if destino else destino
#
#         new_tipo = ChoiceTiposDoc.DEVOLUCION_RECIBIDA
#         new_doc = crea_documento_generado(ueb, departamento_destino, new_tipo)
#         crea_detalles_generado(new_doc, detalles)
#         DocumentoDevolucionRecibida.objects.create(documento=new_doc, documentoorigen=doc)
#
#     title = 'Documento rechazado'
#     text = 'El Documento %s - %s se rechazó satisfactoriamente !' % (doc.numeroconsecutivo, doc.tipodocumento)
#     sweetify.success(request, title, text=text, persistent=True)
#
#     return HttpResponseLocation(
#         reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + getparams_hx,
#         target='#table_content_documento_swap',
#         headers={
#             'HX-Trigger': request.htmx.trigger,
#             'HX-Trigger-Name': request.htmx.trigger_name,
#             'event_action': 'refused',
#         }
#     )
#
#
# class ObtenerDocumentoVersatModalFormView(BaseModalFormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = ObtenerDocumentoVersatForm
#     father_view = 'app_index:flujo:flujo_documento_list'
#
#     funcname = {
#         'submitted': aceptar_documento_versat,
#         'refused': rechazar_documento_versat,
#     }
#     inline_tables = [{
#         "table": DocumentosVersatDetalleTable([]),
#         "name": "documentosversatdetalletable",
#         "visible": True,
#     }]
#     hx_target = '#table_content_documento_swap'
#     hx_swap = 'outerHTML'
#     hx_form_target = '#dialog'
#     hx_form_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#     modal_form_title = 'Obtener Documento del Versat'
#     max_width = '1150px'
#
#     def get_context_data(self, **kwargs):
#         detalle = self.request.GET.get('detalle', None)
#         json_data = self.request.GET.get('json_data', None)
#         if detalle:
#             detalle = literal_eval(detalle)
#             json_data = literal_eval(json_data)
#             codigos_versat = [p['producto_codigo'] for p in detalle]
#             productos = ProductoFlujo.objects.values('codigo', 'medida__clave').filter(codigo__in=codigos_versat).all()
#             codigos_sistema = [(p['codigo'], p['medida__clave'].strip()) for p in productos]
#             for d in detalle:
#                 d['existe_sistema'] = (d['producto_codigo'], d['medida_clave'].strip()) in codigos_sistema
#
#         self.inline_tables[0].update({
#             "table": DocumentosVersatDetalleTable(detalle),
#         })
#         ctx = super().get_context_data(**kwargs)
#         ctx.update({
#             'btn_rechazar': 'Rechazar Documento',
#             'btn_aceptar': 'Aceptar Documento',
#             'inline_tables': self.inline_tables,
#         })
#         return ctx
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         iddocumento = self.request.GET.get('iddocumento')
#         iddocumento_numero = self.request.GET.get('iddocumento_numero')
#         iddocumento_numctrl = self.request.GET.get('iddocumento_numctrl')
#         iddocumento_fecha = self.request.GET.get('iddocumento_fecha')
#         iddocumento_fecha_hidden = self.request.GET.get('iddocumento_fecha')
#         iddocumento_concepto = self.request.GET.get('iddocumento_concepto')
#         iddocumento_almacen = self.request.GET.get('iddocumento_almacen')
#         iddocumento_sumaimporte = self.request.GET.get('iddocumento_sumaimporte')
#         json_data = self.request.GET.get('json_data')
#         kwargs['initial'].update({
#             "iddocumento": iddocumento,
#             "iddocumento_numero": iddocumento_numero,
#             "iddocumento_numctrl": iddocumento_numctrl,
#             "iddocumento_fecha": iddocumento_fecha,
#             "iddocumento_fecha_hidden": iddocumento_fecha_hidden,
#             "iddocumento_concepto": iddocumento_concepto,
#             "iddocumento_almacen": iddocumento_almacen,
#             "iddocumento_sumaimporte": iddocumento_sumaimporte,
#             "json_data": json_data,
#         })
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         kw.update({
#             'request': self.request,
#             'iddocumento': form.cleaned_data['iddocumento'],
#             'iddocumento_fecha': form.cleaned_data['iddocumento_fecha_hidden'],
#         })
#         if self.request.POST['event_action'] in ['submitted', 'refused']:
#             kw.update(
#                 {'detalles': self.inline_tables[0]['table'].data.data, 'json_data': form.cleaned_data['json_data']})
#         return kw
#
#
# def departamentosueb(request):
#     ueb = request.GET.get('ueb_destino')
#     unidad = None if not ueb else UnidadContable.objects.get(pk=ueb)
#     departamento = Departamento.objects.filter(unidadcontable=unidad)
#     dptos_no_inicializados = [x.pk for x in departamento if
#                               not x.fechainicio_departamento.filter(
#                                   ueb=ueb).all().exists()]
#
#     departamento = departamento.exclude(pk__in=dptos_no_inicializados)
#     data = {
#         'departamento_destino': departamento,
#     }
#     form = DocumentoForm(data)
#     form.fields['departamento_destino'].widget.attrs.update({
#         'style': 'display: block;',
#     })
#     form.fields['departamento_destino'].label = 'Departamento Destino'
#     form.fields['departamento_destino'].required = True
#     form.fields['departamento_destino'].queryset = departamento
#     form.fields["departamento_destino"].widget.attrs = {
#         'hx-get': reverse_lazy('app_index:flujo:departamentosueb'),
#         'hx-target': '#div_id_departamento_destino',
#         'hx-trigger': 'change from:#div_id_ueb_destino',
#         'hx-include': '[name="ueb_destino"]',
#     }
#
#     response = HttpResponse(
#         as_crispy_field(form['departamento_destino']).replace('is-invalid', ''),
#         content_type='text/html'
#     )
#     return response
#
#
# def productosdestino(request):
#     producto_origen = request.GET.get('producto')
#     estado_origen = request.GET.get('estado')
#     pk_doc = request.GET.get('documento_hidden')
#     documento = Documento.objects.get(pk=pk_doc)
#
#     prod_d = CambioProducto.objects.filter(productoo=producto_origen).values(
#         'productod') if producto_origen and estado_origen else []
#     producto_destino = ProductoFlujo.objects.filter(pk__in=prod_d)
#
#     data = {
#         'producto_destino': producto_destino,
#         'doc': documento
#     }
#
#     form = DocumentoDetalleForm(data)
#     form.fields['producto_destino'].widget.attrs.update({
#         'style': 'display: block;',
#     })
#
#     form.fields['producto_destino'].label = 'Departamento Destino'
#     form.fields['producto_destino'].required = True
#     form.fields['producto_destino'].queryset = producto_destino
#
#     form.fields["producto_destino"].widget.attrs = {
#         'hx-get': reverse_lazy('app_index:flujo:productosdestino'),
#         'hx-target': '#div_id_producto_destino',
#         'hx-trigger': 'change from:#div_id_producto, change from:#div_id_estado',
#         'hx-include': '[name="producto"], [name="estado"], [name="documento_hidden"]',
#         'readonly': True}
#
#     response = HttpResponse(
#         as_crispy_field(form['producto_destino']).replace('is-invalid', ''),
#         content_type='text/html'
#     )
#     return response
#
#
# def estadodestino(request):
#     estado_origen = request.GET.get('estado')
#     pk_doc = request.GET.get('documento_hidden')
#     documento = Documento.objects.get(pk=pk_doc)
#
#     estado_destino = int(estado_origen) if estado_origen else EstadoProducto.BUENO
#
#     data = {
#         'estado_destino': estado_destino,
#         'doc': documento
#     }
#
#     form = DocumentoDetalleForm(data)
#     form.fields['estado_destino'].widget.attrs.update({
#         'style': 'display: block;',
#     })
#
#     form.fields['estado_destino'].label = 'Estado'
#     form.fields['estado_destino'].required = True
#     form.fields['estado_destino'].queryset = estado_destino
#
#     form.fields["estado_destino"].widget.attrs = {
#         'hx-get': reverse_lazy('app_index:flujo:estadodestino'),
#         'hx-target': '#div_id_estado_destino',
#         'hx-trigger': 'change from:#div_id_estado',
#         'hx-include': '[name="estado"], [name="documento_hidden"]',
#         'readonly': True}
#
#     response = HttpResponse(
#         as_crispy_field(form['estado_destino']).replace('is-invalid', ''),
#         content_type='text/html'
#     )
#     return response
#
#
# @transaction.atomic
# def cierremes(kwargs):
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'El cambio fue realizado',
#         'error_title': '',
#     }
#
#     # la ueb debe venir por parametro
#     ueb = kwargs['request'].user.ueb
#
#     fecha = kwargs['fecha']
#
#     cierres = FechaCierreMes.objects.filter(ueb=ueb, fecha__month=fecha.month, fecha__year=fecha.year).all()
#
#     no_cerrar = False
#     if cierres.exists():
#         no_cerrar = True
#         error_title = 'Ya este mes fue cerrado'
#     else:
#         fechas = FechaPeriodo.objects.filter(ueb=ueb).all()
#         fechas_despues = fechas.filter(fecha__month=fecha.month, fecha__year=fecha.year,
#                                        fecha__day__gt=fecha.day).all()
#         if fechas_despues.exists():
#             no_cerrar = True
#             cad = '\n'.join([x.departamento.descripcion for x in fechas_despues])
#             error_title = 'Departamentos que tienen período posterior al cierre.\n' + cad
#
#     if not no_cerrar:
#         docs_no_confirm = Documento.objects.filter(
#             estado__in=[EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES],
#             ueb=ueb
#         ).order_by('departamento__id').distinct('departamento')
#
#         if docs_no_confirm.exists():
#             cad = '\n'.join([x.departamento.descripcion for x in docs_no_confirm])
#             error_title = 'No se puede cerrar el mes, existen documentos sin confirmar en los Departamentos \n' + cad
#             no_cerrar = True
#         else:
#             # buscar documentos versat del periodo
#             departamentos = Departamento.objects.filter(unidadcontable=ueb)
#
#             noinicializado = [x for x in departamentos if not x.inicializado(ueb)]
#
#             if noinicializado:
#                 cad = '\n'.join([x.descripcion for x in noinicializado])
#                 error_title = 'No se puede cerrar el mes, existen departamentos no inicializados \n' + cad
#                 no_cerrar = True
#             else:
#                 # Obtener los centros de costo únicos
#                 centros_costos = CentroCosto.objects.filter(
#                     departamento_centrocosto__in=departamentos
#                 ).distinct()
#                 fecha_desde = fecha.replace(day=1)
#                 cant_dias = calendar.monthrange(fecha.year, fecha.month)[1]
#                 fecha_hasta = fecha.replace(day=cant_dias)
#                 cc = [x.clave for x in centros_costos]
#                 cc = ','.join(cc)
#                 params = {'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),
#                           'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d'),
#                           'unidad': ueb.codigo,
#                           'centro_costo': cc
#                           }
#                 try:
#                     error_title = 'Hay problemas de conexión con la API Versat, \n ' \
#                                   'no se ha podido verificar si existen documentos en el Versat pendientes de procesar'
#
#                     response = getAPI('documentogasto', ueb=ueb.codigo, params=params)
#
#                     if response and response.status_code == 200:
#                         datos = response.json()['results']
#                         ids = ids_documentos_versat_procesados(fecha_desde, fecha_hasta, None,
#                                                                ueb) if datos else []
#                         datos = list(filter(lambda x: x['iddocumento'] not in ids, datos))
#
#                         if datos:
#                             # Obtener valores únicos de la llave 'centrocosto_descripcion'
#                             valores_unicos = set(item["centrocosto_descripcion"] for item in datos)
#                             cad = '\n'.join([x for x in valores_unicos])
#                             # Convertir a lista si se necesita
#                             valores_unicos = list(valores_unicos)
#                             error_title = 'Existen documentos en el Versat \n que constituyen salida hacia el flujo productivo \n y no han sido procesados en los Centros de Costo \n' + cad
#                             no_cerrar = True
#                     else:
#                         no_cerrar = True
#                 except Exception as e:
#                     no_cerrar = True
#
#     if no_cerrar:
#         func_ret.update({
#             'success': False,
#             'error_title': error_title
#         })
#         return func_ret
#
#     FechaCierreMes.objects.update_or_create(ueb=ueb, defaults={"fecha": fecha})
#
#     fechaperiodo = fecha_hasta + timedelta(days=1)
#     FechaPeriodo.objects.filter(ueb=ueb).update(fecha=fechaperiodo)
#
#     NumeroDocumentos.objects.filter(ueb=ueb, tiponumero=TipoNumeroDoc.NUMERO_CONSECUTIVO).update(numero=0)
#
#     existencias = ExistenciaDpto.objects.filter(ueb=ueb, mes=fecha.month, anno=fecha.year).all()
#     nuevas_existencias = []
#     for e in existencias:
#         nuevas_existencias.append(
#             ExistenciaDpto(
#                 producto=e.producto,
#                 estado=e.estado,
#                 cantidad_inicial=e.cantidad_final,
#                 cantidad_final=e.cantidad_final,
#                 precio=e.precio,
#                 importe=e.importe,
#                 departamento=e.departamento,
#                 ueb=e.ueb,
#                 anno=fechaperiodo.year,
#                 mes=fechaperiodo.month
#             )
#         )
#     ExistenciaDpto.objects.bulk_create(nuevas_existencias)
#     return func_ret
#
#
# class DameFechaModalFormView(BaseModalFormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = ObtenerFechaForm
#     father_view = 'app_index:index'
#     hx_target = '#body'
#     hx_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#     modal_form_title = 'Obtener Fecha'
#     max_width = '500px'
#     funcname = {
#         'submitted': cierremes,
#     }
#     close_on_error = True
#
#     def get_context_data(self, **kwargs):
#         fecha = self.request.GET.get('fecha', None)
#         ctx = super().get_context_data(**kwargs)
#         fecha_max = ctx['form'].initial['fecha']
#         fecha_min = fecha_max.replace(day=1) if fecha_max else None
#
#         ctx['form'].fields['fecha'].widget.picker_options['minDate'] = fecha_min.strftime('%d/%m/%Y') if fecha_min else ''
#         ctx['form'].fields['fecha'].widget.picker_options['maxDate'] = fecha_max.strftime('%d/%m/%Y') if fecha_max else ''
#         return ctx
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         fecha = self.request.GET.get('fecha')
#         fecha_ini, fecha_fin = dame_fecha_cierre_mes(ueb=self.request.user.ueb)
#         kwargs['initial'].update({
#             "fecha": fecha_fin,
#             "fecha_ini": fecha_ini
#         })
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         kw.update({
#             'request': self.request,
#             'fecha': form.cleaned_data['fecha'],
#         })
#         if self.request.POST['event_action'] in ['submitted']:
#             kw.update(
#                 {'fecha': form.cleaned_data['fecha']})
#         return kw
#
#
# def obtener_fecha_procesamiento(request):
#     ueb = request.user.ueb
#     dep = request.GET.get('departamento', None)
#     dpto = Departamento.objects.get(pk=dep) if dep else None
#     rango_fecha = request.GET.get('rango_fecha', "")
#     fecha_procesamiento = dame_fecha(ueb, dpto)
#
#     data = {
#         'departamento': dep,
#     }
#
#     if fecha_procesamiento:
#         data.update({
#             'rango_fecha': fecha_procesamiento.strftime('%d/%m%Y') + ' - ' + fecha_procesamiento.strftime('%d/%m%Y')
#         })
#
#     form = DocumentoFormFilter(data)
#
#     response = HttpResponse(
#         as_crispy_field(form['rango_fecha']).replace('is-invalid', ''),
#         content_type='text/html'
#     )
#     return trigger_client_event(
#         response=response,
#         name='change',
#         params={
#             'departamento': dep,
#             'rango_fecha': rango_fecha,
#         }
#     )
#
#
# @transaction.atomic
# def cambioperiodo(kwargs):
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'Se ha cambiado el período satisfactoriamente',
#         'error_title': '',
#     }
#
#     hay_error = False
#
#     # la ueb debe venir por parametro
#     ueb = kwargs['request'].user.ueb
#
#     fecha = kwargs['fecha']
#
#     departamento = Departamento.objects.get(pk=kwargs['request'].POST.get('departamento'))
#     # se realizan las validaciones para hacer el cambio de periodo.
#     # que no existan documentos en edición o con errores dentro del departamento
#     # que en el versat no existan documentos por traer en ese mes. TODO si esto se hace diario o el último día del mes
#     # está hecho para el último día del mes.
#
#     fecha_actual = dame_fecha(ueb=ueb, departamento=departamento)
#     docs = Documento.objects.filter(ueb=ueb, departamento=departamento, \
#                                     estado__in=[EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES])
#     # cambiomes = False
#     if docs.exists():
#         hay_error = True
#         func_ret.update({
#             'success': False,
#             'error_title': "Existen documentos sin Confirmar"
#         })
#
#     if not hay_error:
#         FechaPeriodo.objects.update_or_create(ueb=ueb, departamento=departamento, defaults={"fecha": fecha})
#         Documento.objects.filter(ueb=ueb, departamento=departamento, fecha=fecha_actual).update(cerrado=True)
#         fproc = FechaPeriodo.objects.get_cached_data()
#         fecha_ant = fproc[ueb][departamento]['fecha_procesamiento']
#     return func_ret
#
#
# class DameFechaCambioPeriodoModalFormView(DameFechaModalFormView):
#     father_view = 'app_index:flujo:flujo_documento_list'
#     hx_target = '#table_content_documento_swap'
#     hx_swap = 'outerHTML'
#
#     modal_form_title = 'Cambiar Fecha del Período Actual'
#
#     funcname = {
#         'submitted': cambioperiodo,
#     }
#
#     def get_context_data(self, **kwargs):
#         fecha = self.request.GET.get('fecha', None)
#         ctx = super().get_context_data(**kwargs)
#         fecha_min = ctx['form'].initial['fecha']
#         cant_dias = calendar.monthrange(fecha_min.year, fecha_min.month)[1]
#         fecha_max = fecha_min.replace(day=cant_dias)
#         ctx['form'].fields['fecha'].widget.picker_options['minDate'] = fecha_min.strftime('%d/%m/%Y')
#         ctx['form'].fields['fecha'].widget.picker_options['maxDate'] = fecha_max.strftime('%d/%m/%Y')
#         ctx['hx_target'] = self.hx_target
#         ctx['hx_swap'] = self.hx_swap
#         return ctx
#
#     def get_form_kwargs(self):
#         fecha = self.request.GET.get('fecha')
#         departamento = self.request.GET.get(
#             'departamento') if 'departamento' in self.request.GET else self.request.POST.get('departamento')
#         fecha_ini, fecha_fin = dame_fecha_periodo(ueb=self.request.user.ueb, departamento=departamento)
#         kwargs = super().get_form_kwargs()
#         kwargs['initial'].update({
#             "fecha": fecha_ini,
#             "departamento": departamento,
#         })
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         kw.update({
#             'request': self.request,
#             'fecha': form.cleaned_data['fecha'],
#         })
#         if self.request.POST['event_action'] in ['submitted']:
#             kw.update(
#                 {'fecha': form.cleaned_data['fecha']})
#         return kw
#
#
# def dame_fecha_periodo(ueb, departamento):
#     fecha = dame_fecha(ueb, Departamento.objects.get(
#         pk=departamento))  # FechaPeriodo.objects.filter(**dicc).order_by('-fecha').first()
#
#     fecha_actual = fecha
#     fecha_ini = fecha_actual
#     day = fecha.day
#     cant_dias = calendar.monthrange(fecha.year, fecha.month)[1]
#     if day < cant_dias:
#         fecha_ini = fecha_actual + timedelta(days=1)
#
#     fecha_str = str(fecha_ini.day) + '/' + str(fecha_ini.month) + '/' + str(fecha_ini.year)
#     datetime.strptime(fecha_str, "%d/%m/%Y").date()
#
#     fecha_fin = fecha_ini.replace(day=cant_dias)
#
#     return fecha_ini, fecha_fin
#
#
# def dame_fecha_cierre_mes(ueb):
#     fecha = FechaPeriodo.objects.filter(ueb=ueb).order_by('-fecha').first()
#     if not fecha:
#         return None, None
#     mes = fecha.fecha.month
#     anno = fecha.fecha.year
#
#     fecha_str = '01/' + str(mes) + '/' + str(anno)
#     fecha_ini = datetime.strptime(fecha_str, "%d/%m/%Y").date()
#     cant_dias = calendar.monthrange(anno, mes)[1]
#     fecha_fin = fecha_ini.replace(day=cant_dias)
#
#     return fecha_ini, fecha_fin
#
#
# def dame_noperativa_sispax(request, fecha):
#     try:
#         # Construir la URL con reverse y pasar el parámetro `fecha`
#         url = request.build_absolute_uri(
#             reverse('app_index:appexternas:no_appsispax', kwargs={'fecha': fecha})
#         )
#
#         cookies = request.COOKIES
#         response = requests.get(url, cookies=cookies, allow_redirects=False)
#
#         return not(response.status_code == 302 and "error=1" in response.headers.get("Location", ""))
#
#     except Exception as e:
#         return {'error': str(e)}
#
# def get_DateNormaOperativa(doc):
#     fecha = DocumentoDetalleProductoNO.objects.filter(
#         documentodetalle=doc.id
#     ).select_related(
#         'normaoperativadetalle__normaoperativaproducto__normaoperativa'
#     ).order_by(
#         '-normaoperativadetalle__normaoperativaproducto__normaoperativa__fecha'
#     ).values_list(
#         'normaoperativadetalle__normaoperativaproducto__normaoperativa__fecha',
#         flat=True
#     ).first()
#
#     if(fecha==None):
#         fecha=doc.documento.fecha
#     return fecha
#
# @csrf_exempt
# def guardar_cantidad_norma_operativa(request, pk):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             cantidad = Decimal(data.get('cantidad'))
#             norma = Decimal(data.get('norma'))
#
#             if cantidad is None:
#                 return JsonResponse({'error': 'Cantidad no proporcionada'}, status=400)
#
#             obj = DocumentoDetalleProductoNO.objects.get(pk=pk)
#
#             detalle = obj.documentodetalle.id
#             # if Decimal(cantidad) != obj.cantidad:
#             obj.cantidad = cantidad
#
#             normao_base = obj.normaoperativadetalle.normaoperativaproducto.cantidad
#             cantidad_usada = Decimal('0.0')
#             if normao_base != Decimal('0.0'):
#                 cantidad_usada = (cantidad * norma) / normao_base
#             obj.cantidad_usada = cantidad_usada
#             cantidad_total = obj.documentodetalle.cantidad
#             obj.importe = cantidad_usada * obj.precio
#
#             obj.save()
#
#             sum_NO_cantidad = DocumentoDetalleProductoNO.objects.filter(
#                 documentodetalle=detalle
#             ).aggregate(total=Coalesce(Sum('cantidad'), Decimal('0')))['total']
#
#             cantidad_new = cantidad_total - sum_NO_cantidad
#
#              # Obtener todos los registros NC relacionados
#             nc = DocumentoDetalleProductoNC.objects.filter(
#                 documentodetalle=detalle,
#                 normaconsumodetalles__producto=obj.normaoperativadetalle.producto
#             ).select_related(
#                 'normaconsumodetalles',
#                 'normaconsumodetalles__normaconsumo'
#             ).first()
#
#             # Calcular nueva cantidad para cada NC
#             if nc:
#                 try:
#                     norma_ramal = nc.normaconsumodetalles.norma_ramal
#                     norma_base = nc.normaconsumodetalles.normaconsumo.cantidad
#                 except (AttributeError, TypeError):
#                     # Manejar casos donde las relaciones están vacías
#                     pass
#
#                 produccion = cantidad_new
#                 if norma_base != Decimal('0.0'):
#                     new_cantidad = (produccion * norma_ramal) / norma_base
#                 else:
#                     new_cantidad = Decimal('0.0')
#
#                 nc.cantidad = new_cantidad
#                 nc.cantidad = new_cantidad
#                 existencia_product, hay_error = existencia_producto(nc.documentodetalle.documento, nc.normaconsumodetalles.producto,
#                                                                     nc.estado, new_cantidad, nc.operacion)
#                 nc.existencia = existencia_product
#                 nc.error = hay_error
#                 nc.save()
#
#                 ultima_existencia, datos = atualiza_existencias_no(obj.normaoperativadetalle.producto, obj.documentodetalle, existencia_product)
#
#                 actualiza_existencias_documentos(nc.documentodetalle.documento, nc.normaconsumodetalles.producto, nc.estado, ultima_existencia)
#
#             return JsonResponse({
#                 'status': 'ok',
#                 # 'id': str(pk),
#                 # 'detalle': detalle,
#                 # 'cantidad': cantidad,
#                 # 'existencia': ultima_existencia,
#                 'datos': datos
#             })
#         except DocumentoDetalleProductoNO.DoesNotExist:
#             return JsonResponse({'error': 'Objeto no encontrado'}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
#         except Exception as e:
#             # Registra el error para depuración
#             import logging
#             logging.error(f"Error al guardar cantidad: {str(e)}")
#             return JsonResponse({'error': 'Error interno del servidor'}, status=500)
#
#     return JsonResponse({'error': 'Método no permitido'}, status=405)
#
# def atualiza_existencias_no(producto, detalle, existencia_anterior):
#     otras_no = DocumentoDetalleProductoNO.objects.\
#         filter(documentodetalle=detalle, normaoperativadetalle__producto=producto).\
#         order_by('orden')
#
#     new_existencia = existencia_anterior
#     datos = []
#     for o in otras_no:
#         cantidad_usada = o.cantidad_usada
#         new_existencia = new_existencia + (cantidad_usada * o.operacion) if cantidad_usada > 0 else new_existencia
#         o.existencia = new_existencia if cantidad_usada > 0 else 0
#         o.error = new_existencia<0
#         datos.append({
#             'id': o.id,
#             'detalle': o.documentodetalle.id,
#             'cantidad': o.cantidad,
#             'cantidad_usada': o.cantidad_usada,
#             'existencia': o.existencia
#         })
#         o.save()
#     return new_existencia, datos
#
# # ------ NormaOperativa / CRUD ------
# class NormaOperativaCRUD(CommonCRUDView):
#     model = NormaOperativa
#     env = {
#         'normaoperativaproducto': NormaOperativaProducto
#     }
#     namespace = 'app_index:flujo'
#
#     fields = [
#         'fecha',
#     ]
#
#     search_fields = [
#         'fecha',
#     ]
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     filterset_class = NormaOperativaFilter
#
#     # htmx
#     hx_form_target = '#main_content_swap'
#     hx_swap = 'outerHTML'
#     hx_target = '#dialog'
#     hx_form_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#
#     # Table settings
#     paginate_by = 25
#     table_class = NormaOperativaTable
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 context.update({
#                     'url_apiversat_no': 'app_index:flujo:obtener_no',
#                     'sistema': 'Sispax',
#                     'url_exportar': True,
#                     'object2': self.env['normaoperativaproducto'],
#                     'return_url': None,
#                     'noexport_excel': True,
#                     'hx_target': self.hx_target,
#                     'hx_form_target': self.hx_form_target,
#                     'hx_swap': self.hx_swap,
#                     "hx_get": reverse_lazy('app_index:flujo:obtener_no'),
#                 })
#
#                 return context
#
#             def get_queryset(self):
#                 queryset = super().get_queryset()
#                 queryset = queryset.filter(ueb=self.request.user.ueb).order_by('-fecha')
#                 return queryset
#
#         return OFilterListView
#
# # ------ NormaOperativa / CRUD ------
# class NormaOperativaProductoCRUD(CommonCRUDView):
#     model = NormaOperativaProducto
#
#     namespace = 'app_index:flujo'
#
#     fields = [
#         'producto',
#         'cantidad',
#         'medida',
#     ]
#
#     search_fields = [
#         'cantidad__contains',
#         'medida__descripcion__icontains',
#         'producto__descripcion__icontains',
#     ]
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     views_available = ['list', 'detail']
#
#     detail_form = NormaOperativaDetalleDetailForm
#
#     filterset_class = NormaOperativaProductoFilter
#
#     # Table settings
#     paginate_by = 15
#     table_class = NormaOperativaProductoTable
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return_url = reverse_lazy(
#                     crud_url_name(NormaOperativa, 'list', 'app_index:flujo:'))
#                 context.update({
#                     'return_url': return_url,
#                     'return_text': 'normas operativas',
#                 })
#
#                 return context
#
#             def get_queryset(self):
#                 queryset = super(OFilterListView, self).get_queryset()
#
#                 qfilter = {}
#                 clave = self.request.GET.get('Claven', None)
#
#                 if clave is not None:
#                     qfilter.update({
#                         'normaoperativa_id': clave,
#                     })
#                     queryset = queryset.filter(**qfilter)
#
#                 return queryset
#
#         return OFilterListView
#
# # ------ NormaConsumoDetalle / HtmxCRUD ------
# class NormaOperativaDetalleHtmxCRUD(InlineHtmxCRUD):
#     model = NormaOperativaDetalle
#     base_model = NormaOperativaDetalle
#     namespace = 'app_index:flujo'
#     inline_field = 'normaoperativa'
#     add_form = NormaOperativaDetalleForm
#     update_form = NormaOperativaDetalleForm
#     detail_form = NormaOperativaDetalleDetailForm
#     list_fields = [
#         'producto',
#         'medida',
#         'norma',
#     ]
#
#     views_available = [
#         'list',
#         'detail',
#     ]
#
#     hx_retarget = '#edit_modal_inner'
#
#     title = "Detalles de norma operativas"
#     table_class = NormaOperativaDetalleTable
#     url_father = None
#
#     def get_filter_list_view(self):
#         filter_list_view = super().get_filter_list_view()
#
#         class FilterListView(filter_list_view):
#             inline_field = self.inline_field
#             base_model = self.base_model
#             name = self.name
#             views_available = self.views_available[:]
#
#             def get_context_data(self, **kwargs):
#                 context = super(FilterListView, self).get_context_data(**kwargs)
#                 return context
#
#             def get_queryset(self):
#                 queryset = super(FilterListView, self).get_queryset()
#                 return queryset
#
#             def get(self, request, *args, **kwargs):
#                 return filter_list_view.get(self, request, *args, **kwargs)
#
#         return FilterListView
#
# class DameFechaNOModalFormView(BaseModalFormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = DameFechaNOModalForm
#     viewname = {'submitted': 'app_index:appexternas:no_appsispax'}
#     hx_target = '#main_content_swap'
#     hx_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML',
#     modal_form_title = 'Fecha de las Normas Operativas'
#     max_width = '500px'
#
#     def get_context_data(self, **kwargs):
#         fecha = self.request.GET.get('fecha', None)
#         ctx = super().get_context_data(**kwargs)
#         fecha_max = ctx['form'].initial['fecha']
#         fecha_min = fecha_max.replace(day=1) if fecha_max else None
#
#         ctx['form'].fields['fecha'].widget.picker_options['minDate'] = fecha_min.strftime('%d/%m/%Y') if fecha_min else ''
#         ctx['form'].fields['fecha'].widget.picker_options['maxDate'] = fecha_max.strftime('%d/%m/%Y') if fecha_max else ''
#         return ctx
#     #
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         fecha = self.request.GET.get('fecha')
#         fecha_ini, fecha_fin = dame_fecha_cierre_mes(ueb=self.request.user.ueb)
#         kwargs['initial'].update({
#             "fecha": fecha_fin,
#             "fecha_ini": fecha_ini
#         })
#         return kwargs
