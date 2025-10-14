# import django_tables2 as tables
# from django.utils.translation import gettext as _
#
# from apps.cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
# from apps.cruds_adminlte3.utils import attrs_center_center
# from .models import *
#
#
# # ------ Ficha Costo / Table ------
# class FichaCostoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_normasconsumo_template.html',
#         # template_name='cruds/actions/hx_actions_fichacosto_filas_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoProducto
#
#         fields = (
#             'fecha',
#             'tipoficha',
#             'producto',
#             'cantidad',
#             'medida',
#             'confirmada',
#             'activa',
#         )
#
# class FichaCostoProductoFilasTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     descripcion = tables.TemplateColumn(template_name='cruds/tables/tree_node_fichaproductos_datos.html')
#     fila = tables.TemplateColumn(template_name='cruds/tables/tree_node_filafichaproducto_datos.html')
#     costo = tables.TemplateColumn(template_name='cruds/tables/tree_node_fichaproductoscosto_datos.html')
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_fichacosto_filas_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoProductoFilas
#
#         fields = (
#             'fila',
#             'descripcion',
#             'costo'
#         )
#
# class FichaCostoProductoFilaCapasTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     # Asumiendo que quieres mostrar los campos relevantes para las capas
#     nombre_capa = tables.Column(verbose_name=_('Capa'), empty_values=()) # Ajusta el accessor según tu modelo Vitola
#     um_capa = tables.Column(verbose_name=_('U.M'), empty_values=())
#     costo_propuesto_norma = tables.Column(verbose_name=_('Norma'))
#     costo_propuesto_precio = tables.Column(verbose_name=_('Precio'))
#     costo_propuesto_importe = tables.Column(verbose_name=_('Importe'))
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoProductoFilaCapas
#
#         fields = (
#             'nombre_capa',
#             'um_capa',
#             'costo_propuesto_norma',
#             'costo_propuesto_precio',
#             'costo_propuesto_importe',
#         )
#
#         exclude = ('actions',)
#
#     def render_nombre_capa(self, record, table):
#         return 'Capa' #getattr(table, 'row_counter', 0) + 1
#
#     def render_um_capa(self, record, table):
#         return 'MILLAR'
#
#
# # ------ FichaCostoProductoFilaDesgloseMPMatTable ------
# class FichaCostoProductoFilaDesgloseMPMatTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     # Mostrar información del producto y sus detalles de desglose
#     producto = tables.Column(accessor = 'producto.descripcion', verbose_name=_('Producto'))
#     um = tables.Column(accessor = 'producto.medida.descripcion', verbose_name=_('UM')) # Asumiendo relación con ProductoFlujo
#     costo_propuesto_norma = tables.Column(accessor='costo_propuesto_norma', verbose_name=_('Norma'))
#     costo_propuesto_precio = tables.Column(verbose_name=_('Precio')) # Será precio_lop de ProductoFlujo
#     costo_propuesto_importe = tables.Column( verbose_name=_('Importe'), empty_values=()) # Calculado: Norma * Precio
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_fichacosto_desglosempmat_template.html', # Debes crear este template
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoProductoFilaDesgloseMPMat
#
#         fields = (
#             'producto',
#             'um',
#             'costo_propuesto_norma',
#             'costo_propuesto_precio',
#             'costo_propuesto_importe',
#             'actions',
#         )
#
#         # Orden de aparición de las columnas
#         sequence = (
#             'producto',
#             'um',
#             'costo_propuesto_norma',
#             'costo_propuesto_precio',
#             'costo_propuesto_importe',
#             'actions'
#         )
#
#         exclude = ('actions',)
#
#
# # ------ FichaCostoProductoFilaDesgloseSalarioTable ------
# class FichaCostoProductoFilaDesgloseSalarioTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     # Mostrar información del desglose de salario
#     codigo = tables.Column(verbose_name=_('Código'), accessor= 'cargo__codigo' )
#     actividad = tables.Column(verbose_name=_('Actividad'), accessor= 'cargo__actividad' ) # Nombre de la actividad desde ClasificadorActividades
#     vinculo_produccion = tables.Column(verbose_name=_('Vínculo Producción'), accessor= 'cargo__vinculo_produccion' ) # Vínculo de producción desde ClasificadorCargos
#     grupo_escala = tables.Column(verbose_name=_('Grupo Escala'), accessor= 'cargo__grupo__grupo' ) # Grupo de escala desde ClasificadorCargos
#     cargo = tables.Column(verbose_name=_('Cargo'), accessor= 'cargo__descripcion' ) # Nombre del cargo desde ClasificadorCargos
#     cantidad = tables.Column(verbose_name=_('Cantidad Trabajadores')) # Cantidad de trabajadores
#     norma_tiempo = tables.Column(verbose_name=_('Norma de Tiempo (hrs)')) # Norma de tiempo
#     salario_hora = tables.Column(verbose_name=_('Salario/Hora'), accessor= 'salario_hora' ) # Norma de tiempo
#     gasto_salario = tables.Column(verbose_name=_('Gasto Salario'), accessor= 'gasto_salario' ) # Norma de tiempo
#
#     # Acciones para cada fila de desglose de salario (editar/eliminar)
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_fichacosto_desglosesalario_template.html', # Debes crear este template
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoProductoFilaDesgloseSalario
#
#         fields = ( #Codigo, Cargo, Actividad, Cantidad, Vinculo Produccion,  Grupo Escala, Salario, Norma de Tiempo
#             'codigo',
#             'cargo',
#             'actividad',
#             'cantidad',
#             'vinculo_produccion',
#             'grupo_escala',
#             'norma_tiempo',
#             'salario_hora',
#             'gasto_salario',
#             'actions'
#         )
# # ------ FichaCostoGrouped / Table ------
# class FichaCostoGroupedTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/hx_actions_productgrouped_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FichaCostoGrouped
#
#         fields = (
#             'Producto',
#             'Tipo_Ficha',
#             'Cantidad_Fichas',
#         )
#
# class VarGlobalesCostoDatosTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = VarGlobalesCostoDatos
#
#         fields = (
#             'variable_global',
#             'destino',
#             'valor',
#         )
#
# class FechaProcesamientoCostoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     mes = tables.Column(verbose_name='Mes', accessor='get_mes_display')
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = FechaProcesamientoCosto
#
#         fields = (
#             'ueb',
#             'mes',
#             'anno',
#         )



