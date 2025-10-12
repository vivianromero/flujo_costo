# import django_tables2 as tables
# from django.template.loader import render_to_string
# from django.utils.translation import gettext as _
# from django.utils.translation import gettext_lazy as _
#
# from apps.cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
# from apps.cruds_adminlte3.utils import attrs_center_center
# from apps.flujo.models import *
#
#
# # ------ Documento / Table ------
# class DocumentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = Documento
#
#         fields = (
#             'numeroconsecutivo',
#             'tipodocumento',
#             'numerocontrol',
#             'estado',
#             'fecha',
#             'tipodocumento__operacion',
#         )
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_documentos_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     @staticmethod
#     def render_estado(value):
#         if value == 'Edición':
#             return render_to_string('app_index/table_icons/edicion_icon.html')
#         elif value == 'Confirmado':
#             return render_to_string('app_index/table_icons/confirmado_icon.html')
#         elif value == 'Rechazado':
#             return render_to_string('app_index/table_icons/rechazado_icon.html')
#         elif value in ['Cancelado', 'Con Errores']:
#             return render_to_string('app_index/table_icons/cancelado_icon.html')
#
#     @staticmethod
#     def value_estado(value):
#         return value
#
#
# # ------ DocumentoDetalle / Table ------
# class DocumentoDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = DocumentoDetalle
#
#         fields = (
#             'producto',
#             'estado',
#             'cantidad',
#             'precio',
#             'importe',
#             'existencia',
#         )
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_documento_detalles_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
# class DocumentoDetalleReprocesoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     hx_target = "#id_documentodetallereproc_myList"
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = DocumentoDetalleReproceso
#
#         fields = (
#             'producto',
#             'estado',
#             'cantidad',
#             'precio',
#             'importe',
#             'existencia',
#         )
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_documento_detalles_inline_template.html',
#         verbose_name=_('Actions'),
#         orderable=False,
#         attrs={'td': {'class': 'text-center'}},
#     )
#
# # ------ DocumentoDetalleProductoNC / Table ------
# class DocumentoProduccionTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     hx_target = "#id_documentodetalleproductonc_myList"
#
#     # Columnas definidas explícitamente
#     codigo = tables.Column(
#         verbose_name=_("Código"),
#         accessor='normaconsumodetalles__producto__codigo',
#         order_by='normaconsumodetalles__producto__codigo'
#     )
#     producto = tables.Column(
#         verbose_name=_("Producto"),
#         accessor='normaconsumodetalles__producto__descripcion',
#         order_by='normaconsumodetalles__producto__descripcion'
#     )
#     medida = tables.Column(
#         verbose_name="UM",
#         accessor='normaconsumodetalles__medida__descripcion',
#         order_by='normaconsumodetalles__medida__descripcion'
#     )
#     norma = tables.Column(
#         verbose_name=_("Norma Ramal"),
#         accessor='normaconsumodetalles__norma_ramal',
#         order_by='normaconsumodetalles__norma_ramal'
#     )
#     cantidad = tables.Column(
#         verbose_name=_("Cantidad"),
#         accessor='cantidad',
#         order_by='cantidad'
#     )
#
#     # Se utiliza el alias "calc_existencia" para evitar conflictos con el campo del modelo.
#     existencia = tables.Column(
#         verbose_name=_("Existencia"),
#         accessor='existencia',
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = DocumentoDetalleProductoNC
#         fields = (
#             'codigo',
#             'medida'
#         )
#         sequence = (
#             'codigo',
#             'producto',
#             'medida',
#             'norma',
#             'cantidad',
#             'existencia',
#         )
#         exclude = ['actions',]
#         order_by = 'producto__descripcion'
#
#     # Columna de acciones
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_documento_detalles_inline_template.html',
#         verbose_name=_('Actions'),
#         orderable=False,
#         attrs={'td': {'class': 'text-center'}},
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#
#     def render_existencia(self, value, record):
#         return f"{value:.6f}" if value is not None else "0.00"
#
#
#     def render_normaconsumodetalles_producto_descripcion(self, value, record):
#         return f"{value.codigo} - {value.descripcion}" if value else _("Sin producto")
#
# # ------ DocumentoDetalleProductoNO / Table ------
# class DocumentoProduccionNOTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     hx_target = "#id_documentodetalleproductono_myList"
#     id = tables.Column(visible=False)
#     # producto = tables.Column(verbose_name=_("Producto"), accessor=('producto'))
#     medida = tables.Column(verbose_name=_("Medida"), accessor=('medida'))
#     norma = tables.Column(verbose_name=_("Norma"), accessor=('norma'))
#     cantidad = tables.Column(verbose_name=_("Cantidad"), accessor=('cantidad_usada'))
#     cantidad = tables.TemplateColumn(
#         template_code='''\
#         {% if 'detail' not in getparams %}
#         <input type="text"
#                name="cantidad_{{ record.id }}"
#                value="{{ record.cantidad|default_if_none:0.0|stringformat:"0.6f" }}"
#                class="textinput form-control text-end decimal-mask"
#                data-inputmask="'alias': 'decimal', 'digits': 6"
#                    onblur="updateCantidadUsada(this, '{{ record.id }}')"
#                inputmode="decimal"
#                style="min-width: 100px; max-width: 150px;">
#         {% else %}
#             {{ record.cantidad|default_if_none:0.0|stringformat:"0.6f" }}
#         {% endif %}
#         <script>
#         Inputmask().mask(document.querySelectorAll("input"));
#         function updateCantidadUsada(input, id) {
#             const mainCantidadInput = document.getElementById('id_cantidad');
#             const submitBtn = document.getElementById('id_inline_form_btn_acept');
#             const mainCantidad = parseFloat(mainCantidadInput.value.replace(',', '.')) || 0;
#
#             // Selecciona todos los campos `cantidad_<uuid>`
#             const cantidadInputs = document.querySelectorAll('input[name^="cantidad_"]');
#             let total = 0;
#             cantidadInputs.forEach(input => {
#                 const value = parseFloat(input.value.replace(',', '.')) || 0;
#                 total += value;
#             });
#
#             // Cálculo de cantidad_usada y saldo por fila
#             const row = input.closest('tr');
#             const normaCell = row.querySelector('td.norma');
#             const cantidadUsadaCell = row.querySelector('td.cantidad_usada');
#             const existenciaCell = row.querySelector('td.existencia');
#
#             if (!normaCell || !cantidadUsadaCell || !existenciaCell) return;
#
#             const cantidad = parseFloat(input.value.replace(',', '.')) || 0;
#             const norma = parseFloat(normaCell.textContent.replace(',', '.')) || 0;
#             const existencia = parseFloat(existenciaCell.textContent.replace(',', '.')) || 0;
#
#             // Actualiza cantidad_usada
#             const cantidadUsada = cantidad * norma;
#             cantidadUsadaCell.textContent = cantidadUsada.toFixed(6).replace('.', ',');
#
#             // Validación del botón de envío
#             if (total > mainCantidad) {
#                 submitBtn.classList.add('disabled');
#             } else {
#                 //guardar la cantidad
#                 guardarCantidadNorma(id, cantidad, norma, existencia);
#                 submitBtn.classList.remove('disabled');
#             }
#         }
#         // Función utilitaria para obtener el CSRF token desde las cookies
#         function getCookie(name) {
#             let cookieValue = null;
#             if (document.cookie && document.cookie !== '') {
#                 const cookies = document.cookie.split(';');
#                 for (let i = 0; i < cookies.length; i++) {
#                     const cookie = cookies[i].trim();
#                     if (cookie.substring(0, name.length + 1) === (name + '=')) {
#                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
#                         break;
#                     }
#                 }
#             }
#             return cookieValue;
#         }
#         function guardarCantidadNorma(id, cantidad, norma, existencia) {
#
#             fetch(`/es/guardar_cantidad_norma_operativa/${id}/`, {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                     'X-CSRFToken': getCookie('csrftoken')
#                 },
#                 body: JSON.stringify({ cantidad, norma, existencia })
#             })
#             .then(response => {
#                 if (!response.ok) throw new Error("Error HTTP");
#                 return response.json();
#             })
#             .then(data => {
#                 if (data.status === 'ok') {
#                     data.datos.forEach(dato => {
#
#                         htmx.ajax('GET', `/es/flujo/documentodetalleproductonc/${dato.detalle}/list`, {
#                             target: "#id_documentodetalleproductonc_myList",
#                             swap: "innerHTML"
#                         });
#                         const row = document.querySelector(`input[name="cantidad_${dato.id}"]`).closest('tr');
#                         if (row) {
#                             const existenciaCell = row.querySelector('td.existencia');
#                             if (existenciaCell) {
#                                 const existenciaNum = parseFloat(dato.existencia) || 0;
#                                 existenciaCell.textContent = existenciaNum.toFixed(6).replace('.', ',');
#                             }
#                         }
#
#                     });
#
#                     //Si se quiere mostrar alguna alerta cuando salga bien
#                 } else {
#                     //Si se quiere mostrar alguna alerta cuando salga mal
#                 }
#             })
#             .catch(err => {
#                 console.error("Error al guardar:", err);
#                 alert("Ocurrió un error al guardar la cantidad.");
#             });
#         }
#
#         </script>
#         ''',
#
#     verbose_name=_("Productos Producidos"),
#         attrs={
#             "th": {
#                 "class": "text-nowrap",
#                 "style": "width: 150px;"
#             },
#             "td": {
#                 "class": "text-end"
#             }
#         }
#     )
#
#     existencia = tables.Column(
#         verbose_name=_("Existencia"),
#         accessor='existencia',
#         orderable=True
#     )
#
#     class Meta:
#         model = DocumentoDetalleProductoNO
#         fields = ("id", "producto", "medida", "norma","cantidad", "existencia", "cantidad_usada")
#         sequence = (
#             'producto',
#             'medida',
#             'norma',
#             'cantidad',
#             'cantidad_usada',
#             'existencia'
#         )
#         exclude = ['actions']
#
#     def __init__(self, *args, **kwargs):
#         kwargs['data'] = self.get_queryset(*args, **kwargs)
#         super().__init__(*args, **kwargs)
#
#     def get_queryset(self, *args, **kwargs):
#
#         queryset = kwargs['data'].select_related(
#             'normaoperativadetalle',  # Relación directa
#             'normaoperativadetalle__producto',
#             'normaoperativadetalle__medida',
#             'documentodetalle__documento',
#             'documentodetalle__documento__departamento',
#             'documentodetalle__documento__ueb'
#         ).annotate(
#             # producto=F('normaoperativadetalle__producto__descripcion'),
#             medida=F('normaoperativadetalle__medida__descripcion'),
#             norma=F('normaoperativadetalle__norma')
#         ).order_by('normaoperativadetalle__producto__descripcion', 'normaoperativadetalle__norma')
#
#         return queryset
#
#     def render_existencia(self, value, record):
#         return f"{value:.6f}" if value is not None else "0.00"
#
#
# # ------ Documentos Versat / Table ------
# class DocumentosVersatTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     iddocumento = tables.Column(verbose_name='Id',
#                                 visible=False)
#     iddocumento_numero = tables.Column(verbose_name='Número')
#     iddocumento_numctrl = tables.Column(verbose_name='Número Ctrl')
#     iddocumento_fecha = tables.Column(verbose_name='Fecha')
#     iddocumento_concepto = tables.Column(verbose_name='Concepto')
#     iddocumento_almacen = tables.Column(verbose_name='Almacén')
#     iddocumento_sumaimporte = tables.Column(verbose_name='Importe')
#     iddocumento_detalle = tables.JSONColumn(verbose_name='Detalles', visible=False)
#     json_data = tables.JSONColumn(verbose_name='Json Data', visible=False)
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_documentosversat_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs={"th": {'style': 'text-align: center;'},
#                "td": {'style': 'text-align: center;'},
#                }
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         attrs = {
#             "class": 'table display table-sm table-bordered table-striped table-hover',
#             "style": 'line-height: 1;',
#             "td": {
#                 "class": "align-middle",
#                 "style": 'padding: 0px;',
#             },
#             'th': {
#                 "style": 'position: sticky; top: 0;'
#             }
#         }
#         sequence = (
#             'iddocumento',
#             'iddocumento_numero',
#             'iddocumento_numctrl',
#             'iddocumento_fecha',
#             'iddocumento_concepto',
#             'iddocumento_almacen',
#             'iddocumento_sumaimporte',
#             'iddocumento_detalle',
#             'actions',
#             'json_data',
#         )
#
#
# # ------ Documentos Versat / Table ------
# class DocumentosVersatDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     existe_sistema = tables.Column(verbose_name='', orderable=False)
#     idmovimiento = tables.Column(verbose_name='Id Movimiento', orderable=False, visible=False)
#     iddocumento = tables.Column(verbose_name='Id Documento', orderable=False, visible=False)
#     idproducto = tables.Column(verbose_name='Id Producto', orderable=False, visible=False)
#     producto_codigo = tables.Column(verbose_name='Código')
#     producto_descripcion = tables.Column(verbose_name='Descripción')
#     idmedida = tables.Column(verbose_name='Id Medida', orderable=False, visible=False)
#     medida_clave = tables.Column(verbose_name='Clave Medida', orderable=False, visible=False)
#     medida_descripcion = tables.Column(verbose_name='Medida')
#     cantidad = tables.Column(verbose_name='Cantidad')
#     precio = tables.Column(verbose_name='Precio')
#     importe = tables.Column(verbose_name='Importe')
#
#     actions = None
#
#     @staticmethod
#     def render_existe_sistema(value):
#         if value:
#             return render_to_string('app_index/table_icons/confirmado_icon.html')
#         else:
#             return render_to_string('app_index/table_icons/rechazado_icon.html')
#
#     @staticmethod
#     def value_existe_sistema(value):
#         return value
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         attrs = {
#             "class": 'table display table-sm table-bordered table-striped table-hover',
#             "style": 'line-height: 1;',
#             "td": {
#                 "class": "align-middle",
#                 "style": 'padding: 0px;',
#             },
#             'th': {
#                 "style": 'position: sticky; top: 0;'
#             }
#         }
#         sequence = (
#             'existe_sistema',
#             'idmovimiento',
#             'iddocumento',
#             'idproducto',
#             'producto_codigo',
#             'producto_descripcion',
#             'idmedida',
#             'medida_clave',
#             'medida_descripcion',
#             'cantidad',
#             'precio',
#             'importe',
#         )
#
# class NormaOperativaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_listarnormasoperativas_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=True,
#         attrs=attrs_center_center
#     )
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = NormaOperativa
#
#         fields = (
#             'fecha',
#         )
#
#
# class NormaOperativaProductoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_normasconsumo_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = NormaOperativaProducto
#
#         fields = (
#             'producto',
#             'medida',
#             'cantidad',
#         )
#
# class NormaOperativaDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = NormaOperativaDetalle
#
#         fields = (
#             'producto',
#             'medida',
#             'norma',
#         )
#         order_by = ('producto',)
#
#     hx_target = "#id_normaconsumodetalleno_myList"
#     hx_swap = "innerHTML"
