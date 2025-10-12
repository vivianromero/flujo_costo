# import json
#
# from django.db.models import CharField
# from django.db.models.functions import Concat, Cast
#
# from apps.app_index.views import BaseModalFormView
# from apps.codificadores import ChoiceTiposDoc
# from apps.reports.reports import ReportGenerator
# from .reportsforms import *
#
#
# def genera_report(kwargs):
#     departamento = kwargs['departamento']
#     producto = kwargs['producto']
#     estados = kwargs['estados']
#     ueb = kwargs['request'].user.ueb
#     fechai = kwargs['fechai']
#     fechaf = kwargs['fechaf']
#     param_periodo = f"Del {fechai.strftime('%d/%m/%Y')} al {fechaf.strftime('%d/%m/%Y')}"
#     filtro_estado = [EstadoProducto(int(e)).label for e in estados]
#     if not filtro_estado or len(filtro_estado) == len(EstadoProducto.choices):
#         filtro_estado = ['Todos']
#
#     param_filtro_estado = ','.join(filtro_estado)
#     for e in estados:
#         param_filtro_estado.join(EstadoProducto(int(e)).label)
#
#     param_estado = ','.join(estados)
#
#     param_filtro_producto = 'Todos' if not producto else producto.codigo + '-' + producto.descripcion
#
#     parameters = {
#         'param_ueb_id': str(ueb.pk),
#         'param_ueb': str(ueb),
#         'param_departamento_id': str(departamento.pk),
#         'param_producto_id': str(producto.pk) if producto else producto,
#         'param_estado': param_estado if param_estado else None,
#         'param_periodo': param_periodo,
#         'param_fechai': fechai.strftime('%Y-%m-%d'),
#         'param_fechaf': fechaf.strftime('%Y-%m-%d'),
#         'param_filtro_producto': param_filtro_producto,
#         'param_filtro_estado': param_filtro_estado,
#     }
#
#     report_name = kwargs.get('report_name', '')
#     if report_name == ChoiceReports.MOVIMIENTOSMP:
#         parameters.update({
#             'param_tiposdocumentos': ",".join(
#                 [str(ChoiceTiposDoc.TRANSF_HACIA_DPTO), str(ChoiceTiposDoc.TRANSF_DESDE_DPTO),
#                  str(ChoiceTiposDoc.DEVOLUCION)])
#         })
#     elif report_name == ChoiceReports.CONTROLPESADAS or report_name == ChoiceReports.CONTROLPESADASRESUMEN:
#         parameters.update({
#             'param_tiposdocumentos': ",".join(
#                 [str(ChoiceTiposDoc.RECEPCION_PRODUCCION)])
#         })
#     elif report_name == ChoiceReports.EXISTENCIAS:
#         parameters.update({
#             'param_existencia_cero': str(int(kwargs['existencia_cero']))
#         })
#     report_generator = ReportGenerator(report_name, output_formats=['pdf'], ueb=ueb, user=kwargs['request'].user)
#     generado = report_generator.generate_report(parameters)
#     return json.loads(generado.content)
#
#
# def loadreport(kwargs):
#     func_ret = {
#         'success': True,
#         'errors': {},
#         'success_title': 'Report Generado con Éxito',
#         'error_title': '',
#     }
#
#     generado = genera_report(kwargs)
#     if generado.get('error', False):
#         func_ret.update({
#             'success': False,
#             'error_title': "Se ha producido un error al generar el reporte"
#         })
#     return func_ret
#
#
# class ReportModalFormView(BaseModalFormView):
#     template_name = 'app_index/modals/modal_form.html'
#     form_class = ReportForm
#     father_view = 'app_index:index'
#     hx_target = '#body'
#     hx_swap = 'outerHTML'
#     hx_retarget = '#dialog'
#     hx_reswap = 'outerHTML'
#     modal_form_title = ''
#     max_width = '850px'
#
#     funcname = {
#         'submitted': loadreport,
#     }
#
#     close_on_error = True
#     isreport = True
#
#     def form_valid(self, form):
#         filtros = get_filter_report(self.request, form, self.report_name)
#         existe = True
#         if self.report_name in [ChoiceReports.MOVIMIENTOS, ChoiceReports.EXISTENCIAS]:
#             existe = valida_existencia(filtros)
#         elif self.report_name == ChoiceReports.MOVIMIENTOSMP:
#             existe = valida_existencia_mov_mp(filtros)
#         elif self.report_name == ChoiceReports.CONTROLPESADAS or self.report_name == ChoiceReports.CONTROLPESADASRESUMEN:
#             existe = valida_existencia_control_pesadas(filtros)
#             if form.cleaned_data['element_checkbox']:
#                 self.report_name = ChoiceReports.CONTROLPESADASRESUMEN
#             else:
#                 self.report_name = ChoiceReports.CONTROLPESADAS
#         if not existe:
#             form.add_error(None, 'No existen datos para mostrar')
#             return self.form_invalid(form)
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         # fecha = self.request.GET.get('fecha', None)
#         context = super().get_context_data(**kwargs)
#         dep_queryset = context['form'].fields['departamento'].queryset
#         ueb = self.request.user.ueb
#         dep_queryset = dep_queryset.filter(unidadcontable=ueb)
#         context['form'].fields['departamento'].queryset = dep_queryset
#         return context
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['report_type'] = self.report_name
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         departamento = form.cleaned_data['departamento']
#         if self.report_name in [ChoiceReports.MOVIMIENTOSMP, ChoiceReports.CONTROLPESADAS, ChoiceReports.CONTROLPESADASRESUMEN]:
#             departamento = form.fields['departamento'].queryset.first()
#         kw.update({
#             'request': self.request,
#             'departamento': departamento,
#             'estados': form.cleaned_data['estados'],
#             'producto': form.cleaned_data['producto'],
#             'fechai': form.cleaned_data['fechai'],
#             'fechaf': form.cleaned_data['fechaf'],
#             'report_name': self.report_name,
#             'ueb': self.request.user.ueb,
#         })
#         if self.report_name in [ChoiceReports.EXISTENCIAS]:
#             existencia_cero = form.cleaned_data['element_checkbox']
#             kw.update({
#                 'existencia_cero': existencia_cero,
#             })
#         return kw
#
#
# class ReportExistenciaModalFormView(ReportModalFormView):
#     modal_form_title = ChoiceReports.EXISTENCIAS
#     report_name = ChoiceReports.EXISTENCIAS
#
#
# class ReportMovimientoModalFormView(ReportModalFormView):
#     modal_form_title = ChoiceReports.MOVIMIENTOS
#     report_name = ChoiceReports.MOVIMIENTOS
#
#
# class ReportMovimientoMPModalFormView(ReportModalFormView):
#     modal_form_title = ChoiceReports.MOVIMIENTOSMP
#     report_name = ChoiceReports.MOVIMIENTOSMP
#     max_width = '500px'
#
# class ReportControlPesadasModalFormView(ReportModalFormView):
#     modal_form_title = ChoiceReports.CONTROLPESADAS
#     report_name = ChoiceReports.CONTROLPESADAS
#     max_width = '500px'
#
#
# def get_filter_report(request, form, report_type=ChoiceReports.EXISTENCIAS):
#     departamento = form.cleaned_data['departamento']
#     if report_type == ChoiceReports.MOVIMIENTOSMP or report_type == ChoiceReports.CONTROLPESADAS or report_type == ChoiceReports.CONTROLPESADASRESUMEN:
#         departamento = form.fields["departamento"].queryset.first()
#     estados = form.cleaned_data['estados']
#
#     if '0' in estados:
#         estados.remove('0')
#     ueb = request.user.ueb
#     fechai = form.cleaned_data['fechai'].strftime('%Y-%m-%d')
#     fechaf = form.cleaned_data['fechaf'].strftime('%Y-%m-%d')
#     producto = form.cleaned_data.get('producto', None)
#
#     dicc_filter = {'departamento': departamento, 'ueb': ueb,
#                    'estado__in': estados,  # estado de los productos
#                    'fecha__range': [fechai, fechaf],
#                    'estado': EstadosDocumentos.CONFIRMADO,
#                    'producto': producto
#                    }
#
#     return dicc_filter
#
#
# def valida_existencia(filtros):
#     if filtros['estado__in'] or filtros.get('producto', None):
#         filtrodetalle = {
#             'documento__fecha__range': filtros['fecha__range'],
#             'documento__departamento': filtros['departamento'],
#             'documento__ueb': filtros['ueb'],
#             'documento__estado': filtros['estado']
#         }
#
#         if filtros['estado__in']:
#             filtrodetalle['estado__in'] = filtros['estado__in']
#
#         if filtros.get('producto', None):
#             filtrodetalle['producto'] = filtros['producto']
#
#         detall = DocumentoDetalle.objects.filter(**filtrodetalle)
#         if detall.exists():
#             return True
#
#         filtrodetalleprodest = {
#             'documentodetalle__documento__fecha__range': filtros['fecha__range'],
#             'documentodetalle__documento__departamento': filtros['departamento'],
#             'documentodetalle__documento__ueb': filtros['ueb'],
#             'documentodetalle__documento__estado': filtros['estado']
#         }
#         if filtros['estado__in']:
#             filtrodetalleprodest['estado__in'] = filtros['estado__in']
#
#         if filtros.get('producto', None):
#             filtrodetalleprodest['producto'] = filtros['producto']
#
#         detall = DocumentoDetalleProducto.objects.filter(**filtrodetalleprodest)
#         if detall.exists():
#             return True
#
#         detallestado = DocumentoDetalleEstado.objects.filter(**filtrodetalleprodest)
#         if detallestado.exists():
#             return True
#
#         detallestadoreproc = DocumentoDetalleReproceso.objects.filter(**filtrodetalleprodest)
#         if detallestadoreproc.exists():
#             return True
#
#         if filtros.get('producto', None):
#             filtrodetalleprodest['normaconsumodetalles__producto'] = filtros['producto']
#             filtrodetalleprodest['cantidad__gt'] = 0
#             filtrodetalleprodest.pop('producto')
#
#         detallesnc = DocumentoDetalleProductoNC.objects.filter(**filtrodetalleprodest)
#         if detallesnc.exists():
#             return True
#
#         if filtros.get('producto', None):
#             filtrodetalleprodest['normaoperativadetalle__producto'] = filtros['producto']
#             filtrodetalleprodest['cantidad__gt'] = 0
#             filtrodetalleprodest.pop('normaconsumodetalles__producto')
#
#         detallesno = DocumentoDetalleProductoNO.objects.filter(**filtrodetalleprodest)
#         return detallesno.exists()
#
#     filtros.pop('estado__in')
#     filtros.pop('producto')
#
#     return Documento.objects.filter(**filtros).exists()
#
#
# def valida_existencia_mov_mp(filtros):
#     filtros.update({
#         'tipodocumento': [ChoiceTiposDoc.TRANSF_HACIA_DPTO, ChoiceTiposDoc.TRANSF_DESDE_DPTO,
#                           ChoiceTiposDoc.DEVOLUCION
#                           ]
#     })
#     # Paso 1: filtrar movimientos válidos en el período
#     movimientos_filtrados = DocumentoDetalle.objects.filter(Q(
#         documento__fecha__range=filtros['fecha__range'],
#         documento__ueb_id=filtros['ueb'].id,
#         documento__departamento_id=filtros['departamento'].id,
#         documento__estado=EstadosDocumentos.CONFIRMADO,
#         documento__tipodocumento__id__in=filtros['tipodocumento'],
#         producto__tipoproducto_id=ChoiceTiposProd.PESADA) | Q(producto__tipoproducto_id=ChoiceTiposProd.MATERIAPRIMA,
#         producto__productoflujoclase_producto__clasemateriaprima_id=ChoiceClasesMatPrima.CAPACLASIFICADA)
#     ).values_list('producto_id', flat=True).distinct()
#
#     #si se filtra por producto
#     if filtros['producto']:
#         ids_productos = [x for x in movimientos_filtrados]
#         productos_validos = ProductoFlujo.objects.filter(
#             id__in=ids_productos  # lista de IDs de productos con movimiento
#         ).annotate(
#             vitola_id=Concat(
#                 Coalesce(Cast(F('vitola_productocapa__producto__id'), output_field=CharField()), Value('')),
#                 Coalesce(Cast(F('vitola_productopesada__producto__id'), output_field=CharField()), Value('')),
#                 output_field=CharField()
#             )
#         ).filter(
#             vitola_id=filtros['producto'].id  # el string concatenado que viene como parámetro
#         ).values(
#             'id', 'vitola_id'
#         ).distinct()
#
#         return productos_validos.exists()
#     return movimientos_filtrados.exists()
#
# def valida_existencia_control_pesadas(filtros):
#     filtros.update({
#         'tipodocumento': [ChoiceTiposDoc.RECEPCION_PRODUCCION]
#     })
#     # Condiciones comunes
#     condiciones_comunes = Q(
#         documentodetalle__documento__fecha__range=filtros['fecha__range'],
#         documentodetalle__documento__departamento_id=filtros['departamento'].id,
#         documentodetalle__documento__ueb_id=filtros['ueb'].id,
#         documentodetalle__documento__tipodocumento_id__in=filtros['tipodocumento'],
#         documentodetalle__documento__estado=EstadosDocumentos.CONFIRMADO,
#         documentodetalle__producto__tipoproducto_id=ChoiceTiposProd.PESADA
#     )
#
#     producto_id = filtros['producto']
#     # Producto utilizado opcional (NC)
#     if producto_id:
#         condiciones_nc = condiciones_comunes & Q(normaconsumodetalles__producto_id=producto_id.id)
#     else:
#         condiciones_nc = condiciones_comunes
#
#     existe_nc = DocumentoDetalleProductoNC.objects.filter(condiciones_nc).exists()
#
#     # Producto utilizado opcional (NO)
#     if producto_id:
#         condiciones_no = condiciones_comunes & Q(normaoperativadetalle__producto_id=producto_id.id)
#     else:
#         condiciones_no = condiciones_comunes
#
#     existe_no = DocumentoDetalleProductoNO.objects.filter(condiciones_no).exists()
#
#     return existe_nc or existe_no
