# import json
#
# from apps.app_index.views import BaseModalFormView
# from apps.reports.reports import ReportGenerator
# from . import ChoiceReports
# from .reportsforms import *
# from apps.flujo.models import EstadosDocumentos, EstadoProducto, DocumentoDetalle, Documento, DocumentoDetalleProducto, \
#     DocumentoDetalleEstado, DocumentoDetalleReproceso, DocumentoDetalleProductoNC, DocumentoDetalleProductoNO
#
#
# def genera_report(kwargs):
#     centrocosto = kwargs['centrocosto']
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
#         'param_centrocosto_id': str(centrocosto.pk),
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
#         if self.report_name in [ChoiceReports.EXISTENCIAS]:
#             existe = valida_existencia(filtros)
#
#         if not existe:
#             form.add_error(None, 'No existen datos para mostrar')
#             return self.form_invalid(form)
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         # fecha = self.request.GET.get('fecha', None)
#         context = super().get_context_data(**kwargs)
#         cc_queryset = context['form'].fields['centrocosto'].queryset
#         ueb = self.request.user.ueb
#         cc_queryset = cc_queryset.filter(departamento_centrocosto__unidadcontable=ueb).distinct()
#         context['form'].fields['centrocosto'].queryset = cc_queryset
#         return context
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['report_type'] = self.report_name
#         return kwargs
#
#     def get_fields_kwargs(self, form):
#         kw = {}
#         centrocosto = form.cleaned_data['centrocosto']
#
#         kw.update({
#             'request': self.request,
#             'centrocosto': centrocosto,
#             'estados': form.cleaned_data['estados'],
#             'producto': form.cleaned_data['producto'],
#             'fechai': form.cleaned_data['fechai'],
#             'fechaf': form.cleaned_data['fechaf'],
#             'report_name': self.report_name,
#             'ueb': self.request.user.ueb,
#         })
#         return kw
#
#
# class ReportExistenciaModalFormView(ReportModalFormView):
#     modal_form_title = ChoiceReports.EXISTENCIAS
#     report_name = ChoiceReports.EXISTENCIAS
#
#
# def get_filter_report(request, form, report_type=ChoiceReports.EXISTENCIAS):
#     centrocosto = form.cleaned_data['centrocosto']
#     estados = form.cleaned_data['estados']
#
#     if '0' in estados:
#         estados.remove('0')
#     ueb = request.user.ueb
#     fechai = form.cleaned_data['fechai'].strftime('%Y-%m-%d')
#     fechaf = form.cleaned_data['fechaf'].strftime('%Y-%m-%d')
#     producto = form.cleaned_data.get('producto', None)
#
#     dicc_filter = {'centrocosto': centrocosto, 'ueb': ueb,
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
#             'documento__centrocosto': filtros['centrocosto'],
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
#             'documentodetalle__documento__centrocosto': filtros['centrocosto'],
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
#     filtros.update({
#         'departamento__centrocosto': filtros['centrocosto']
#     })
#     filtros.pop('centrocosto')
#
#     return Documento.objects.filter(**filtros).exists()

