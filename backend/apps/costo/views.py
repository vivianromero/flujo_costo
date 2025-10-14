# from apps.codificadores import ChoiceClasesMatPrima
# from apps.codificadores.models import LineaSalida, Vitola
# from django.db import IntegrityError
# from django.db.models import Prefetch
# from django.db.models import ProtectedError
# from django.http import HttpResponseRedirect
# from django.shortcuts import redirect
# from django.shortcuts import render
# from django.views.generic.edit import FormView
# from django_htmx.http import HttpResponseLocation
#
# from apps.app_index.views import CommonCRUDView
# from apps.cruds_adminlte3.inline_htmx_crud import InlineHtmxCRUD
# from apps.cruds_adminlte3.templatetags.crud_tags import crud_inline_url
# from apps.exportar.views import crear_export_datos_table
# from apps.utiles.utils import message_error
# from .filters import *
# from .tables import *
# from .utils import dame_fecha_costo
# from .forms import *
# from apps.codificadores.models import NormaConsumo, NormaconsumoDetalle, VinculoCargoProduccion
#
#
# # ------ FichaCostoFilasDetalle / HtmxCRUD ------
# class FichaCostoProductoFilasHtmxCRUD(InlineHtmxCRUD):
#     model = FichaCostoProductoFilas
#     base_model = FichaCostoProducto
#     namespace = 'app_index:costo'
#     inline_field = 'fichacostoproducto'
#     add_form = FichaCostoProductoFilasForm
#     update_form = FichaCostoProductoFilasForm
#     detail_form = FichaCostoProductoFilasDetailForm
#     list_fields = [
#         'fila',
#         'costo'
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
#     inlines=[]
#
#     hx_retarget = '#edit_modal_inner'
#
#     title = "Filas Ficha de Costo"
#     no_add_prod = True  # variable para que no salva el botón Adicionar Productos
#     table_class = FichaCostoProductoFilasTable
#     url_father = None
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class UpdateView(view):
#             integrity_error = "El producto ya existe para la norma!"
#
#             def get_form_kwargs(self):
#                 kwargs = super().get_form_kwargs()
#                 fila_tipo = self.object.fila.fila
#                 costo_editable = fila_tipo not in ['1.1','1.2']
#                 kwargs['costo_editable'] = costo_editable
#                 return kwargs
#
#             def get_context_data(self, **kwargs):
#                 ctx = super(UpdateView, self).get_context_data(**kwargs)
#                 title = 'Formulario Ajax Modal'  # 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
#
#                 # 1. Obtener el tipo de fila
#                 fila_tipo = self.object.fila.fila
#                 fila_id = self.object.pk
#                 # 2. Determinar qué inline agregar basado en el tipo
#                 inlines_to_add = []
#                 norma_capas = Decimal("1")
#                 if '1.1' in fila_tipo:
#                     if self.model_id.tipoficha == TipoFichaCosto.TORCIDO:
#                         # Obtener la vitola asociada al producto
#                         vitola_qs = Vitola.objects.filter(
#                             producto=self.object.fichacostoproducto.producto.pk
#                         )
#                         vitola = vitola_qs.first()
#
#                         if vitola:
#                             capa = vitola
#                             pesada = vitola.pesada
#                             # ================================
#                             # PROCESO PARA CAPAS CLASIFICADAS
#                             # ================================
#                             if capa.capa and hasattr(capa.capa, 'get_clasemateriaprima') and capa.capa.get_clasemateriaprima \
#                             and capa.capa.get_clasemateriaprima.id == ChoiceClasesMatPrima.CAPACLASIFICADA:
#
#                                 # Paso 1: Obtener IDs de normas de consumo activas para capas clasificadas
#                                 normas_ids = NormaConsumo.objects.filter(
#                                     activa=True,
#                                     producto_id__in=Vitola.objects.filter(
#                                         categoriavitola_id=capa.categoriavitola.id
#                                     ).values_list('capa_id', flat=True)
#                                 ).values_list('id', flat=True)
#
#                                 if normas_ids:
#                                     # Paso 1: Calcular precios usando el método personalizado
#                                     datos = NormaConsumo.objects.calcular_precio_capasclasificadas(normas_ids=normas_ids)
#
#                                     if datos:
#                                         # Paso 2: Calcular precio promedio
#                                         precios = list(datos.values())
#                                         precio_promedio = sum(precios) / len(precios)
#
#                                         # Paso 3: Obtener norma_empresarial PROMEDIO desde NormaConsumoDetalle
#                                         detalles_norma_empresarial = NormaconsumoDetalle.objects.filter(
#                                             normaconsumo__in=normas_ids
#                                         ).values_list('norma_empresarial', flat=True)
#
#                                         if detalles_norma_empresarial:
#                                             norma_empresarial_promedio = sum(detalles_norma_empresarial) / len(detalles_norma_empresarial)
#                                         else:
#                                             norma_empresarial_promedio = Decimal("1.00")
#
#                                         # Paso 4: Crear o actualizar el registro en FichaCostoProductoFilaCapas
#                                         obj, created = FichaCostoProductoFilaCapas.objects.update_or_create(
#                                             fila=self.object,
#                                             defaults={
#                                                 "costo_base_norma": Decimal("0"),
#                                                 "costo_base_precio": Decimal("0"),
#                                                 "costo_base_importe": Decimal("0"),
#                                                 "costo_propuesto_norma": norma_capas,
#                                                 "costo_propuesto_precio": precio_promedio,
#                                                 "costo_propuesto_importe": precio_promedio * norma_capas,
#                                             }
#                                         )
#
#                             # ================================
#                             # PROCESO PARA MATERIA PRIMA (PESADA)
#                             # ================================
#                             if pesada:
#                                 try:
#                                     norma_consumo = NormaConsumo.objects.get(
#                                         producto_id=pesada.pk,
#                                         activa=True,
#                                     )
#                                     queryset = NormaconsumoDetalle.objects.filter(
#                                         normaconsumo=norma_consumo
#                                     ).select_related(
#                                         'producto',
#                                         'medida',
#                                         'normaconsumo__producto',
#                                     )
#
#                                     for det in queryset:
#                                         obj, created = FichaCostoProductoFilaDesgloseMPMat.objects.update_or_create(
#                                             fila=self.object,
#                                             producto=det.producto,
#                                             defaults={
#                                                 "costo_base_norma": Decimal("0"),
#                                                 "costo_base_precio": Decimal("0"),
#                                                 "costo_base_importe": Decimal("0"),
#                                                 "costo_propuesto_norma": Decimal(det.norma_empresarial),
#                                                 "costo_propuesto_precio": Decimal(det.producto.precio_lop),
#                                                 "costo_propuesto_importe": Decimal(det.norma_empresarial * det.producto.precio_lop),
#                                             }
#                                         )
#
#                                 except NormaConsumo.DoesNotExist:
#                                     print(f">>> Advertencia: No se encontró norma activa para pesada {pesada}")
#                     elif self.model_id.tipoficha == TipoFichaCosto.TERMINADO:
#                         salida = LineaSalida.objects.filter(
#                             producto=self.object.fichacostoproducto.producto.pk
#                         )
#                         vitola = salida.first().vitola
#
#                         vitola_qs = Vitola.objects.filter(
#                             producto=vitola
#                         )
#                         vitola = vitola_qs.first()
#
#                         if vitola:
#                             capa = vitola
#                             pesada = vitola.pesada
#
#                             # ================================
#                             # PROCESO PARA CAPAS CLASIFICADAS
#                             # ================================
#                             if capa.capa and hasattr(capa.capa, 'get_clasemateriaprima') and capa.capa.get_clasemateriaprima \
#                             and capa.capa.get_clasemateriaprima.id == ChoiceClasesMatPrima.CAPACLASIFICADA:
#
#                                 # Paso 1: Obtener IDs de normas de consumo activas para capas clasificadas
#                                 normas_ids = NormaConsumo.objects.filter(
#                                     activa=True,
#                                     producto_id__in=Vitola.objects.filter(
#                                         categoriavitola_id=capa.categoriavitola.id
#                                     ).values_list('capa_id', flat=True)
#                                 ).values_list('id', flat=True)
#                                 test = Vitola.objects.filter(
#                                         categoriavitola_id=capa.categoriavitola.id
#                                     ).values_list('capa_id', flat=True)
#
#                                 if normas_ids:
#                                     # Paso 1: Calcular precios usando el método personalizado
#                                     datos = NormaConsumo.objects.calcular_precio_capasclasificadas(normas_ids=normas_ids)
#
#                                     if datos:
#                                         # Paso 2: Calcular precio promedio
#                                         precios = list(datos.values())
#                                         precio_promedio = sum(precios) / len(precios)
#
#                                         # Paso 3: Obtener norma_empresarial PROMEDIO desde NormaConsumoDetalle
#                                         detalles_norma_empresarial = NormaconsumoDetalle.objects.filter(
#                                             normaconsumo__in=normas_ids
#                                         ).values_list('norma_empresarial', flat=True)
#
#                                         if detalles_norma_empresarial:
#                                             norma_empresarial_promedio = sum(detalles_norma_empresarial) / len(detalles_norma_empresarial)
#                                         else:
#                                             norma_empresarial_promedio = Decimal("1.00")
#
#                                         # Paso 4: Crear o actualizar el registro en FichaCostoProductoFilaCapas
#                                         obj, created = FichaCostoProductoFilaCapas.objects.update_or_create(
#                                             fila=self.object,
#                                             defaults={
#                                                 "costo_base_norma": Decimal("0"),
#                                                 "costo_base_precio": Decimal("0"),
#                                                 "costo_base_importe": Decimal("0"),
#                                                 "costo_propuesto_norma": norma_capas,
#                                                 "costo_propuesto_precio": precio_promedio,
#                                                 "costo_propuesto_importe": precio_promedio * norma_capas,
#                                             }
#                                         )
#
#                             # ================================
#                             # PROCESO PARA MATERIA PRIMA (PESADA)
#                             # ================================
#                             if pesada:
#                                 try:
#                                     norma_consumo = NormaConsumo.objects.get(
#                                         producto_id=pesada.pk,
#                                         activa=True,
#                                     )
#                                     queryset = NormaconsumoDetalle.objects.filter(
#                                         normaconsumo=norma_consumo
#                                     ).select_related(
#                                         'producto',
#                                         'medida',
#                                         'normaconsumo__producto',
#                                     )
#                                     for det in queryset:
#                                         obj, created = FichaCostoProductoFilaDesgloseMPMat.objects.update_or_create(
#                                             fila=self.object,
#                                             producto=det.producto,
#                                             defaults={
#                                                 "costo_base_norma": Decimal("0"),
#                                                 "costo_base_precio": Decimal("0"),
#                                                 "costo_base_importe": Decimal("0"),
#                                                 "costo_propuesto_norma": Decimal(det.norma_empresarial),
#                                                 "costo_propuesto_precio": Decimal(det.producto.precio_lop),
#                                                 "costo_propuesto_importe": Decimal(det.norma_empresarial * det.producto.precio_lop),
#                                             }
#                                         )
#
#                                 except NormaConsumo.DoesNotExist:
#                                     print(f">>> Advertencia: No se encontró norma activa para pesada {pesada}")
#                     inlines_to_add.append(FichaCostoProductoFilaCapasHtmxCRUD)
#                     inlines_to_add.append(FichaCostoProductoFilaDesgloseMPMatHtmxCRUD)
#                 if '1.2' in fila_tipo:
#                     try:
#                         norma_consumo = NormaConsumo.objects.get(
#                             producto_id=self.object.fichacostoproducto.producto.pk,
#                             activa=True,
#                         )
#                         queryset = NormaconsumoDetalle.objects.filter(
#                             normaconsumo=norma_consumo
#                         ).select_related(
#                             'producto',
#                             'medida',
#                             'normaconsumo__producto',
#                         )
#                         for det in queryset:
#                             obj, created = FichaCostoProductoFilaDesgloseMPMat.objects.update_or_create(
#                                 fila=self.object,
#                                 producto=det.producto,
#                                 defaults={
#                                     "costo_base_norma": Decimal("0"),
#                                     "costo_base_precio": Decimal("0"),
#                                     "costo_base_importe": Decimal("0"),
#                                     "costo_propuesto_norma": Decimal(det.norma_empresarial),
#                                     "costo_propuesto_precio": Decimal(det.producto.precio_lop),
#                                     "costo_propuesto_importe": Decimal(det.norma_empresarial * det.producto.precio_lop),
#                                 }
#                             )
#
#                     except NormaConsumo.DoesNotExist:
#                         print(f">>> Advertencia: No se encontró norma activa para pesada")
#                     inlines_to_add.append(FichaCostoProductoFilaDesgloseMPMatHtmxCRUD)
#
#                 elif self.object.fila.salario and self.object.fila.desglosado:
#                     inlines_to_add.append(FichaCostoProductoFilaDesgloseSalarioHtmxCRUD)
#
#                 # ✅✅✅ ACTUALIZAR EL COSTO DE LA FILA PRINCIPAL DIRECTAMENTE EN LA BASE DE DATOS ✅✅✅
#                 costo_total = Decimal("0.00")
#
#                 # Tipo 1.1 o 1.2: Capas + Materias primas
#                 if '1.1' in fila_tipo or '1.2' in fila_tipo:
#                     # Costo de capas
#                     capa_obj = FichaCostoProductoFilaCapas.objects.filter(fila=self.object).first()
#                     if capa_obj:
#                         costo_total += capa_obj.costo_propuesto_importe or Decimal("0.00")
#
#                     # Costo de materias primas
#                     total_mp = FichaCostoProductoFilaDesgloseMPMat.objects.filter(
#                         fila=self.object
#                     ).aggregate(
#                         total=models.Sum('costo_propuesto_importe')
#                     )['total'] or Decimal("0.00")
#                     costo_total += total_mp
#
#                 # Tipo 2.1: Salario
#                 elif self.object.fila.desglosado and self.object.fila.salario:
#                     desgloses_salario = self.object.desglosesalario_fila.all()
#                     total_salario = sum(
#                         Decimal(str(desg.gasto_salario)) for desg in desgloses_salario
#                     )
#                     costo_total = total_salario
#
#                 # Actualizar el costo de la fila principal
#                 try:
#                     fila_db = FichaCostoProductoFilas.objects.get(pk=self.object.pk)
#                     if fila_db.costo != costo_total:
#                         fila_db.costo = costo_total
#                         fila_db.save()  # Dispara actualizar_costos_dependientes()
#                         self.object.costo = costo_total  # Para que el template lo muestre
#                 except FichaCostoProductoFilas.DoesNotExist:
#                     pass
#
#                 # 3. Agregar el inline condicionalmente al contexto
#                 if inlines_to_add:
#                     # Obtener la lista actual de inlines del contexto
#                     current_inlines = ctx.get('inlines', []).copy()
#
#                     # Instanciar cada inline y agregarlo
#                     for inline_class in inlines_to_add:
#                         inline_instance = inline_class()
#                         current_inlines.append(inline_instance)
#
#                     ctx['inlines'] = current_inlines
#
#                 ctx.update({
#                     'modal_form_title': title,
#                     'max_width': '950px',
#                     'hx_target': '#id_' + self.name + '_myList',
#                     'confirm': True,
#                     'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
#                     'object_model': self.model,
#                 })
#                 return ctx
#
#             def get_success_url(self):
#                 return crud_inline_url(self.model_id, self.object, 'list', 'app_index:costo')
#
#             def calcular_costo_fila(self, fila, fila_tipo, costo_form):
#                 costo_total = Decimal("0.00")
#
#                 # Solo calcular si es tipo 1.1 o 1.2
#                 if fila_tipo and ('1.1' == fila_tipo or '1.2' == fila_tipo):
#                     # Tipo 1.1: Capas + Materias primas (TORCIDO o TERMINADO)
#                     capa_obj = FichaCostoProductoFilaCapas.objects.filter(fila=self.object).first()
#                     if capa_obj:
#                         costo_total += capa_obj.costo_propuesto_importe or Decimal("0.00")
#
#                     # Sumar todas las materias primas
#                     total_mp = fila.desglosempmat_fila.aggregate(
#                         total=models.Sum('costo_propuesto_importe')
#                     )['total'] or Decimal("0.00")
#                     costo_total += total_mp
#                 elif fila.fila.desglosado and  fila.fila.salario:
#                     desgloses_salario = self.object.desglosesalario_fila.all()
#                     total_salario = sum(
#                         Decimal(str(desg.gasto_salario)) for desg in desgloses_salario
#                     )
#                     costo_total = total_salario
#                 else:
#                     costo_total = costo_form
#
#
#                 return costo_total
#
#             def form_valid(self, form):
#                 response = super().form_valid(form)
#                 costo_form = form.cleaned_data.get('costo')
#
#                 fila_tipo = self.object.fila.fila
#                 nuevo_costo = self.calcular_costo_fila(self.object, fila_tipo, costo_form)
#                 if self.object.costo != nuevo_costo:
#                     self.object.costo = nuevo_costo
#                     self.object.save(update_fields=['costo'])
#
#                 return response
#
#         return UpdateView
#
#     def get_delete_view(self):
#         delete_view = super().get_delete_view()
#
#         class DeleteView(delete_view):
#
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return context
#
#             def get_success_url(self):
#                 return super().get_success_url()
#
#             def get(self, request, *args, **kwargs):
#                 return self.post(self, request, *args, **kwargs)
#
#             def post(self, request, *args, **kwargs):
#                 return super().post(request, *args, **kwargs)
#
#         return DeleteView
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
# # ------ FichaCostoProductoFilaCapas / HtmxCRUD ------
# class FichaCostoProductoFilaCapasHtmxCRUD(InlineHtmxCRUD):
#     model = FichaCostoProductoFilaCapas
#     base_model = FichaCostoProductoFilas
#     namespace = 'app_index:costo'
#     inline_field = 'fila'  # related_name='desglosecapas_fila'
#     # Puedes definir forms específicos si los necesitas
#     # add_form = FichaCostoProductoFilaCapasForm
#     # update_form = FichaCostoProductoFilaCapasForm
#     # detail_form = FichaCostoProductoFilaCapasDetailForm
#     list_fields = [
#         'costo_propuesto_norma',
#         'costo_propuesto_precio',
#         'costo_propuesto_importe'
#         # Añade otros campos que quieras mostrar
#     ]
#
#     table_class = FichaCostoProductoFilaCapasTable
#
#     title = "Capas"
#
#     views_available = [
#         'list',
#         'list_detail',
#         'update',
#         'delete',
#         'detail',
#     ]
#
#     hx_retarget = '#edit_modal_inner'
#
#
# # ------ FichaCostoProductoFilaDesgloseMPMat / HtmxCRUD ------
# class FichaCostoProductoFilaDesgloseMPMatHtmxCRUD(InlineHtmxCRUD):
#     model = FichaCostoProductoFilaDesgloseMPMat
#     base_model = FichaCostoProductoFilas
#     namespace = 'app_index:costo'
#     inline_field = 'fila'  # related_name='desglosempmat_fila'
#     # add_form = FichaCostoProductoFilaDesgloseMPMatForm
#     # update_form = FichaCostoProductoFilaDesgloseMPMatForm
#     # detail_form = FichaCostoProductoFilaDesgloseMPMatDetailForm
#     list_fields = [
#         'producto',
#         'costo_propuesto_norma',
#         'costo_propuesto_precio',
#         'costo_propuesto_importe'
#         # Añade otros campos relevantes
#     ]
#
#     table_class = FichaCostoProductoFilaDesgloseMPMatTable
#
#     title = "Materia Prima/Materiales"
#
#     views_available = [
#         'list',
#         'list_detail',
#         'update',
#         'delete',
#         'detail',
#     ]
#
#     hx_retarget = '#edit_modal_inner'
#
#
# # ------ FichaCostoProductoFilaDesgloseSalario / HtmxCRUD ------
# class FichaCostoProductoFilaDesgloseSalarioHtmxCRUD(InlineHtmxCRUD):
#     model = FichaCostoProductoFilaDesgloseSalario
#     base_model = FichaCostoProductoFilas
#     namespace = 'app_index:costo'
#     inline_field = 'fila'  # related_name='desglosesalario_fila'
#     list_fields = [
#         'cargo',
#         'cantidad',
#         'salario',
#         'norma_tiempo',
#         #'gasto_salario'  # Esta es una propiedad calculada
#         # Añade otros campos relevantes
#     ]
#
#     add_form = FichaCostoProductoFilaDesgloseSalarioAddForm
#     update_form = FichaCostoProductoFilaDesgloseSalarioAddForm
#     table_class = FichaCostoProductoFilaDesgloseSalarioTable
#
#     title = "Desglose de Salario"
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
#                 context['target'] = self.request.GET.get('target', None)
#                 return context
#             def form_valid(self, form):
#                 """
#                 Asigna los valores de salario y norma_tiempo desde el ClasificadorCargos
#                 seleccionado antes de guardar.
#                 """
#                 self.object = form.save(commit=False)
#
#                 # Obtener el cargo seleccionado del formulario
#                 cargo_seleccionado = form.cleaned_data.get('cargo')
#
#                 if cargo_seleccionado:
#                     directo = self.object.cargo.vinculo_produccion == VinculoCargoProduccion.DIRECTO
#                     self.object.fila = self.model_id  # Asignar la relación con la fila padre
#                     self.object.salario = getattr(cargo_seleccionado, 'salario', 0)
#                     self.object.nr_media = getattr(cargo_seleccionado, 'nr_media', 0)
#                     self.object.salario_calculado = getattr(cargo_seleccionado, 'salario_calculado', 0)
#                     self.object.norma_tiempo = getattr(cargo_seleccionado, 'norma_tiempo', 0) * (self.object.fila.fichacostoproducto.cantidad if directo else 1)
#                 try:
#                     with transaction.atomic():
#                         self.object.save()
#                 except Exception as e:
#                     form.add_error(None, f"Error al guardar: {e}")
#                     return self.form_invalid(form)
#
#                 return super().form_valid(form)
#         return CreateView
#
# # ------ Ficha Costo / CRUD ------
# class FichaCostoCRUD(CommonCRUDView):
#     model = FichaCostoProducto
#
#     namespace = 'app_index:costo'
#
#     fields = [
#         'fecha',
#         'tipoficha',
#         'producto',
#         'cantidad',
#         'medida',
#         'confirmada',
#         'activa',
#     ]
#
#     views_available = [
#         'list',
#         'create',
#         'update',
#         'delete',
#         'detail',
#     ]
#
#     # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
#     # y no distinga entre mayúsculas y minúsculas.
#     # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
#     search_fields = [
#         'tipoficha',
#         'cantidad__contains',
#         'fecha',
#         'medida__descripcion__icontains',
#         'producto__descripcion__icontains',
#         'producto__codigo__icontains',
#     ]
#
#     add_form = FichaCostoProductoForm
#     update_form = FichaCostoProductoForm
#     detail_form = FichaCostoProductoFilasForm
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     filterset_class = FichaCostoFilter
#
#     # Table settings
#     table_class = FichaCostoTable
#
#     inlines = [FichaCostoProductoFilasHtmxCRUD]
#
#     inline_actions = False
#
#     def get_create_view(self):
#         view = super().get_create_view()
#
#         class OCreateView(view):
#
#             def form_valid(self, form):
#                 return super().form_valid(form)
#
#             def get_form_kwargs(self):
#                 form_kwargs = super().get_form_kwargs()
#                 form_kwargs.update(
#                     {
#                         "user": self.request.user,
#                         "producto": self.request.GET['Producto'] if 'Producto' in self.request.GET else None,
#                     }
#                 )
#                 return form_kwargs
#
#         return OCreateView
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 return_url = reverse_lazy(crud_url_name(FichaCostoGrouped, 'list', 'app_index:costo:'))
#                 context.update({
#                     'url_list_fichacosto': False,
#                     'return_url': return_url,
#                     'confirm': True,
#                     'activar': True,
#                     'return_text': 'fichas de costo',
#                     'texto_confirm': "Al confirmar no podrá modificar la Ficha.!Esta acción no podrá revertirse!",
#                     'texto_activar': "Las demás fichas de este producto serán desactivadas",
#                 })
#
#                 pfilter = self.get_filter_dict()
#                 if 'producto__codigo' and 'producto__descripcion' in pfilter:
#                     producto = ProductoFlujo.objects.get(
#                         codigo=pfilter['producto__codigo'],
#                         descripcion=pfilter['producto__descripcion']
#                     )
#                 else:
#                     producto = None
#                 context.update(self.get_filter_dict())
#                 context.update({'Producto': producto})
#                 return context
#
#             def get_queryset(self):
#                 queryset = super(OFilterListView, self).get_queryset()
#                 qfilter = self.get_filter_dict()
#                 return queryset.filter(**qfilter)
#
#             def get_filter_dict(self):
#                 qfilter = {}
#                 active_filters = self.filterset_class(self.request.GET).form.changed_data != []
#                 tipoficha = None
#                 if active_filters and 'tipoficha' in self.filterset_class(self.request.GET).form.changed_data:
#                     tipoficha = self.request.GET.get('tipoficha', None)
#
#                 producto = self.request.GET.get('Producto', None)
#                 if producto is not None:
#                     if '?' in producto:
#                         producto = producto.split('?')[0]
#                     p = producto.split(' | ')
#                     qfilter.update({
#                         'producto__codigo': p[0],
#                         'producto__descripcion': p[1]
#                     })
#                 if tipoficha is not None:
#                     qfilter.update({
#                         'tipoficha': tipoficha
#                     })
#                 return qfilter
#
#         return OFilterListView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OEditView(view):
#
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data()
#                 if 'pk' in self.kwargs and self.inline_tables:
#                     filter_dict = {'fichacostoproducto__id': self.kwargs['pk']}
#                     data = FichaCostoProductoFilas.objects.filter(**filter_dict)
#                     self.inline_tables[0].update({
#                         "table": FichaCostoProductoFilasTable(data),
#                     })
#                 else:
#                     inline_object_list = None
#                     table = None
#                 ctx.update({
#                     'inline_url_edit': reverse_lazy(
#                         crud_url_name(FichaCostoProducto, 'update', 'app_index:costo:', ),
#                         kwargs={'pk': self.kwargs['pk']}
#                     ),
#                     "add_button_href": 'app_index:costo:obtener_fichacostoproductofilas_datos',
#                     "add_button_hx_get": reverse_lazy('app_index:costo:obtener_fichacostoproductofilas_datos'),
#                     "add_button_hx_target": '#dialog_form',
#                     "acept_btn_hx_get": self.get_success_url(),
#                     "acept_btn_hx_target": '#main_content_swap',
#                     "acept_btn_hx_swap": 'outerHTML',
#                     "inline_tables": self.inline_tables,
#                 })
#                 return ctx
#
#         return OEditView
#
#
# class FichaCostoGroupedCRUD(CommonCRUDView):
#     env = {
#         'fichacosto': FichaCostoProducto
#     }
#     model = FichaCostoGrouped
#
#     namespace = 'app_index:costo'
#
#     fields = [
#         'Tipo_Ficha',
#         'cantidad',
#         'activa',
#         'fecha',
#         'medida',
#         'producto',
#         'Producto',
#         'Cantidad_Fichas',
#     ]
#
#     views_available = [
#         'list',
#         'create',
#     ]
#
#     # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
#     # y no distinga entre mayúsculas y minúsculas.
#     # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
#     search_fields = [
#         'Tipo_Ficha',
#         'cantidad__contains',
#         'fecha',
#         'medida__descripcion__icontains',
#         'producto__descripcion__icontains',
#     ]
#
#     add_form = FichaCostoProductoForm
#     update_form = FichaCostoProductoForm
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     filterset_class = FichaCostoGroupedFilter
#
#     # Table settings
#     table_class = FichaCostoGroupedTable
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 tipoficha = None
#                 active_filters = self.filterset_class(self.request.GET).form.changed_data != []
#                 if active_filters and 'tipoficha' in self.filterset_class(self.request.GET).form.changed_data:
#                     tipoficha = self.filterset_class(self.request.GET).form.data.get('tipoficha', None)
#                 context.update({
#                     'filtrar': True,
#                     'url_exportar': True,
#                     'url_importar': 'app_index:importar:fichacosto_importar',
#                     'url_list_fichacosto': True,
#                     'object2': self.env['fichacosto'],
#                     'titlegroup': 'Mostrar fichas de costo asociadas al producto',
#                     'return_url': None,
#                     'tipoficha': tipoficha,
#
#                 })
#                 return context
#
#             def get_queryset(self):
#                 queryset = super().get_queryset()
#                 return queryset
#
#             def get(self, request, *args, **kwargs):
#                 myexport = request.GET.get("_export", None)
#                 if myexport and myexport == 'sisgest':
#                     table = self.get_table(**self.get_table_kwargs())
#                     datostable = table.data.data
#                     idprods = [p['idprod'] for p in datostable]
#
#                     prefetch_desgloses = Prefetch(
#                         'desglosempmat_fila',
#                         queryset=FichaCostoProductoFilaDesgloseMPMat.objects.all()
#                     )
#
#                     prefetch_filas = Prefetch(
#                         'fichacostoproducto_ficha',
#                         queryset=FichaCostoProductoFilas.objects.all().prefetch_related(prefetch_desgloses)
#                     )
#
#                     datos = FichaCostoProducto.objects.filter(
#                         producto__id__in=idprods,
#                         confirmada=True
#                     ).prefetch_related(prefetch_filas)
#
#                     datos3 = []
#                     datos2 = []
#                     for ficha in datos:
#                         datos2.extend(ficha.fichacostoproducto_ficha.all())
#                         for fila in ficha.fichacostoproducto_ficha.all():
#                             datos3.extend(fila.desglosempmat_fila.all())
#
#                     return crear_export_datos_table(request, "FICHA_COSTO", FichaCostoGrouped, datos, datos2, datos3)
#                 else:
#                     return super().get(request=request)
#
#         return OFilterListView
#
# class VarGlobalesCostoDatosCRUD(CommonCRUDView):
#     model = VarGlobalesCostoDatos
#
#     template_name_base = 'app_index/costo'
#     partial_template_name_base = 'app_index/costo/partials'
#     namespace = 'app_index:costo'
#
#     fields = [
#         'variable_global',
#         'destino',
#         'valor',
#     ]
#
#     add_form = VarGlobalesCostoDatosForm
#     update_form = VarGlobalesCostoDatosForm
#
#     search_fields = [
#         'variable_global__descripcion',
#         'destino',
#     ]
#
#     views_available = ['list', 'create', 'update', 'delete']
#     view_type = ['list', 'create', 'update', 'delete']
#
#     list_fields = fields
#     filter_fields = ['variable_global', 'destino']
#     filterset_class = VarGlobalesCostoDatosFilter
#
#     table_class = VarGlobalesCostoDatosTable
#
#     # HTMX Settings
#     hx_target = '#table_content_varglobales_swap'
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
#             integrity_error = "Ya existe la variable para ese destino"
#             def get_form_kwargs(self):
#                 kwargs = super().get_form_kwargs()
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 if varglobalescosto_id:
#                     kwargs['initial'] = kwargs.get('initial', {})
#                     kwargs['initial']['varglobalescosto'] = varglobalescosto_id
#
#                 centrocosto = self.request.GET.get('centrocosto', None)
#                 if not centrocosto and 'centrocosto' in self.request.POST.keys():
#                     centrocosto = self.request.POST.get('centrocosto')
#
#                 ccosto = CentroCosto.objects.get(pk=centrocosto)
#                 mes, anno = dame_fecha_costo(ueb=self.request.user.ueb) if ccosto else ''
#                 if not mes:
#                     mes = date.today().month
#                     anno = date.today().year
#
#                 kwargs.update(
#                     {
#                         "user": self.request.user,
#                         "centrocosto": centrocosto,
#                     }
#                 )
#                 return kwargs
#
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data(**kwargs)
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 varglobalescosto = None
#                 if varglobalescosto_id:
#                     try:
#                         varglobalescosto = VarGlobalesCosto.objects.get(pk=varglobalescosto_id)
#                     except VarGlobalesCosto.DoesNotExist:
#                         pass
#
#                 title = ('Agregar Valor a Variable Global')
#                 if varglobalescosto:
#                     title += f" - {varglobalescosto.centrocosto.descripcion} ({varglobalescosto.mes}/{varglobalescosto.anno})"
#
#                 params_hx = ''
#                 if self.request.htmx and self.request.htmx.current_url_abs_path:
#                     parts = self.request.htmx.current_url_abs_path.split('?', 1)
#                     if len(parts) > 1:
#                         params_hx = '?' + parts[1]
#
#                 ctx.update({
#                     'modal_form_title': title,
#                     'hx_target': '#table_content_varglobales_swap',
#                     'max_width': '800px',
#                     'getparams_hx': params_hx,
#                 })
#                 return ctx
#
#             def form_valid(self, form):
#                 try:
#                     return super().form_valid(form)
#                 except IntegrityError as e:
#                     form.add_error(None, self.integrity_error)
#                     return self.form_invalid(form)
#                 except Exception as e:
#                     form.add_error(None, 'Existe un error al salvar los datos')
#                     return self.form_invalid(form)
#
#             def form_invalid(self, form, **kwargs):
#                 return super().form_invalid(form, **kwargs)
#
#         return OCreateView
#
#     def get_update_view(self):
#         view = super().get_update_view()
#
#         class OUpdateView(view):
#             integrity_error = "Ya existe la variable para ese destino"
#             def get_context_data(self, **kwargs):
#                 ctx = super().get_context_data(**kwargs)
#                 obj = self.get_object()
#                 title = ('Editar Valor: ') + obj.variable_global.descripcion
#
#                 params_hx = ''
#                 if self.request.htmx and self.request.htmx.current_url_abs_path:
#                     parts = self.request.htmx.current_url_abs_path.split('?', 1)
#                     if len(parts) > 1:
#                         params_hx = '?' + parts[1]
#
#                 ctx.update({
#                     'modal_form_title': title,
#                     'hx_target': '#table_content_varglobales_swap',
#                     'max_width': '800px',
#                     'getparams_hx': params_hx,
#                 })
#                 return ctx
#
#             def get_success_url(self):
#                 # Mantener los parámetros de filtro (varglobalescosto)
#                 url = super().get_success_url()
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 if varglobalescosto_id:
#                     from django.http import QueryDict
#                     q = QueryDict(mutable=True)
#                     q['varglobalescosto'] = varglobalescosto_id
#                     url += '?' + q.urlencode()
#                 return url
#
#             def form_valid(self, form):
#                 try:
#                     return super().form_valid(form)
#                 except IntegrityError as e:
#                     form.add_error(None, self.integrity_error)
#                     return self.form_invalid(form)
#                 except Exception as e:
#                     form.add_error(None, 'Existe un error al salvar los datos')
#                     return self.form_invalid(form)
#
#             def form_invalid(self, form, **kwargs):
#                 return super().form_invalid(form, **kwargs)
#
#         return OUpdateView
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 varglobalescosto = None
#                 self.centrocosto = self.request.GET.get('centrocosto')
#                 ueb = self.request.user.ueb
#                 if self.centrocosto:
#                     try:
#                         varglobalescosto = VarGlobalesCostoDatos.objects.\
#                             filter(varglobalescosto__centrocosto=self.centrocosto, varglobalescosto__ueb=ueb)
#                     except VarGlobalesCostoDatos.DoesNotExist:
#                         pass
#
#                 cc_queryset = context['form'].fields['centrocosto'].queryset
#
#                 cc_queryset = cc_queryset.filter(departamento_centrocosto__isnull=False,
#                                                  departamento_centrocosto__unidadcontable=ueb).distinct(). \
#                     order_by('departamento_centrocosto__centrocosto__clave')
#                 context['form'].fields['centrocosto'].queryset = cc_queryset
#
#                 # Pasar info del padre al template
#                 context.update({
#                     'varglobalescosto': varglobalescosto,
#                     'hx_get': reverse_lazy(crud_url_name(VarGlobalesCostoDatos, 'list', 'app_index:costo:')),
#                     'hx_target': '#table_content_varglobales_swap',
#                     'hay_centrocosto': not self.centrocosto is None,
#                     'select_period': False,
#                     'create_link_menu': True,
#                     'confirm': True,
#                     'show_filters': False,
#                     'filter': False,
#                 })
#
#                 # Si no hay padre, mostrar mensaje
#                 # if not varglobalescosto:
#                 #     context['no_data_msg'] = ("Seleccione un registro de Costo Global para ver sus valores.")
#
#                 return context
#
#             def get_queryset(self):
#                 qs = super().get_queryset()
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 cc = self.request.GET.get('centrocosto', None)
#                 if cc:
#                     return qs
#                 return self.model.objects.none()
#
#         return OFilterListView
#
#     def get_delete_view(self):
#         view = super().get_delete_view()
#
#         class ODeleteView(view):
#             def get_success_url(self):
#                 url = super().get_success_url()
#                 varglobalescosto_id = self.request.GET.get('varglobalescosto')
#                 if varglobalescosto_id:
#                     from django.http import QueryDict
#                     q = QueryDict(mutable=True)
#                     q['varglobalescosto'] = varglobalescosto_id
#                     url += '?' + q.urlencode()
#                 return url
#
#         return ODeleteView
#
# # ------ FechaProcesamientoCosto / CRUD ------
# class FechaProcesamientoCostoCRUD(CommonCRUDView):
#     model = FechaProcesamientoCosto
#
#     namespace = 'app_index:costo'
#
#     fields = [
#         'mes',
#         'anno',
#     ]
#
#     # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
#     # y no distinga entre mayúsculas y minúsculas.
#     # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
#     search_fields = [
#         'ueb__icontains',
#     ]
#
#     add_form = FechaProcesamientoCostoForm
#     update_form = FechaProcesamientoCostoForm
#
#     list_fields = fields
#
#     filter_fields = fields
#
#     views_available = ['list', 'update', 'create', 'delete']
#     view_type = ['list', 'update', 'create', 'delete']
#
#     filterset_class = FechaProcesamientoCostoFilter
#
#     # Table settings
#     table_class = FechaProcesamientoCostoTable
#
#     def get_filter_list_view(self):
#         view = super().get_filter_list_view()
#
#         class OFilterListView(view):
#             def get_context_data(self, *, object_list=None, **kwargs):
#                 context = super().get_context_data(**kwargs)
#                 context.update({
#                     'url_importar': 'app_index:importar:fpc_importar',
#                     'filtrar': True,
#                     'url_exportar': True,
#                 })
#                 return context
#
#             def get_queryset(self):
#                 queryset = super().get_queryset()
#                 queryset = queryset.filter(inicial=True)
#                 return queryset
#
#             def get(self, request, *args, **kwargs):
#                 myexport = request.GET.get("_export", None)
#                 if myexport and myexport == 'sisgest':
#                     table = self.get_table(**self.get_table_kwargs())
#                     datos = table.data.data
#                     return crear_export_datos_table(request, "FechaIniCosto", FechaProcesamientoCosto, datos, None)
#                 else:
#                     return super().get(request=request)
#
#         return OFilterListView
# class FichaCostoProductoFilasModalFormView(FormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = FichaCostoProductoFilasForm
#
#     def form_valid(self, form):
#         if form.is_valid():
#             costo = form.cleaned_data['costo']
#             self.success_url = reverse_lazy(
#                 'app_index:appexternas:prod_appversat',
#                 kwargs={
#                     'costo': costo,
#                 }
#             )
#
#             return HttpResponseLocation(
#                 self.get_success_url(),
#                 target='#main_content_swap',
#
#             )
#         else:
#             return render(self.request, 'app_index/modals/modal_form.html', {
#                 'form': form,
#             })
#
#
# def confirm_fc(request, pk):
#     with transaction.atomic():
#         obj = FichaCostoProducto.objects.get(pk=pk)
#         if obj.fichacostoproducto_ficha.count() > 0:
#             obj.confirmada = True
#             obj.save()
#         else:
#             title = 'No puede ser confrimada la Ficha de Costo '
#             text = 'No tiene productos asociados'
#             message_error(request,
#                           title + obj.__str__() + '!',
#                           text=text)
#     return redirect(
#         reverse_lazy(
#             crud_url_name(FichaCostoProducto, 'list', 'app_index:costo:')) + "?Producto=" + obj.producto.__str__())
#
#
# def activar_fc(request, pk):
#     with transaction.atomic():
#         obj = FichaCostoProducto.objects.get(pk=pk)
#         product = obj.producto
#         objs = FichaCostoProducto.objects.filter(producto=product).update(activa=False)
#         obj.activa = True
#         obj.save()
#     return redirect((
#             reverse_lazy(
#                 crud_url_name(FichaCostoProducto, 'list', 'app_index:costo:')) + "?Producto=" + obj.producto.__str__()))
#
# def productotipoficha(request):
#     tipoficha = request.GET.get('tipoficha', 0)
#     tipoficha = 0 if not tipoficha else int(tipoficha)
#     tipoprod = ChoiceTiposProd.VITOLA if tipoficha == TipoFichaCosto.TORCIDO else ChoiceTiposProd.LINEASALIDA
#     productos = ProductoFlujo.objects.filter(tipoproducto=tipoprod) if tipoficha != 0 else ProductoFlujo.objects.filter(
#         tipoproducto__in=[ChoiceTiposProd.VITOLA, ChoiceTiposProd.LINEASALIDA])
#     context = {
#         'productos': productos,
#         'nottipoficha': tipoficha == 0,
#     }
#     return render(request, 'app_index/partials/producttipoficha.html', context)
