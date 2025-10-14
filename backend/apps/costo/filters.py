# import django_filters
# from django.utils.translation import gettext_lazy as _
#
# from apps.app_index.filters import CustomDateFromToRangeFilter
# from apps.app_index.widgets import MyCustomRangeWidget
# from apps.cruds_adminlte3.filter import MyGenericFilter
# from apps.cruds_adminlte3.utils import crud_url_name
# from .forms import *
# from .filters import *
# from apps.utiles.utils import YES_NO, EMPTY_LABEL
#
# # ------ Ficha Costo / Filter ------
# class FichaCostoFilter(MyGenericFilter):
#     tipoficha = django_filters.ChoiceFilter(
#         field_name='tipoficha',
#         choices=TipoFichaCosto.choices,
#         empty_label=EMPTY_LABEL,
#         widget=forms.Select(
#             attrs={
#                 'style': 'width: 90%',
#                 'hx-get': reverse_lazy(crud_url_name(FichaCostoProducto, 'list', 'app_index:costo:')),
#                 'hx-target': '#main_content_swap',
#                 'hx-trigger': 'change',
#             }
#         ),
#     )
#
#     fecha = CustomDateFromToRangeFilter(
#         label='Fecha',
#         field_name='fecha',
#         widget=MyCustomDateRangeWidget(
#             format='%d/%m/%Y',
#             picker_options={
#                 'use_ranges': True,
#             }
#         ),
#     )
#
#     activa = django_filters.ChoiceFilter(
#         choices=YES_NO,
#         empty_label=EMPTY_LABEL,
#         widget=forms.Select(attrs={
#             'style': 'width: 100%',
#         }),
#     )
#
#     cantidad = django_filters.RangeFilter(
#         label='Cantidad',
#         method='my_range_queryset',
#         widget=MyCustomRangeWidget()
#     )
#
#     search_fields = [
#         'tipoficha',
#         'cantidad__contains',
#         'fecha',
#         'medida__descripcion__icontains',
#         'producto__descripcion__icontains',
#     ]
#     split_space_search = ' '
#
#     class Meta:
#         model = FichaCostoProducto
#         fields = [
#             'cantidad',
#             'activa',
#             'fecha',
#             'producto',
#         ]
#
#         form = FichaCostoFormFilter
#
#         filter_overrides = {
#             models.ForeignKey: {
#                 'filter_class': django_filters.ModelMultipleChoiceFilter,
#                 'extra': lambda f: {
#                     'queryset': django_filters.filterset.remote_queryset(f),
#                 }
#             },
#         }
#
#
# # ------ Ficha Costo / Filter ------
# class FichaCostoGroupedFilter(MyGenericFilter):
#     tipoficha = django_filters.ChoiceFilter(
#         field_name='tipoficha',
#         choices=TipoFichaCosto.choices,
#         empty_label=EMPTY_LABEL,
#         widget=forms.Select(
#             attrs={
#                 'style': 'width: 100%',
#                 'hx-get': reverse_lazy(crud_url_name(FichaCostoGrouped, 'list', 'app_index:costo:')),
#                 'hx-target': '#main_content_swap',
#                 'hx-trigger': 'change',
#             }
#         ),
#     )
#
#     Cantidad_Fichas = django_filters.RangeFilter(
#         label='Cantidad de Fichas',
#         method='my_range_queryset',
#         widget=MyCustomRangeWidget()
#     )
#
#     Producto = django_filters.ModelMultipleChoiceFilter(
#         label="Producto",
#         queryset=ProductoFlujo.objects.filter(tipoproducto__id__in=[ChoiceTiposProd.VITOLA,
#                                                                     ChoiceTiposProd.LINEASALIDA]),
#     )
#
#     search_fields = [
#         'tipoficha',
#         'cantidad__contains',
#         'fecha',
#         'medida__descripcion__icontains',
#         'producto__descripcion__icontains',
#         'producto__codigo__icontains',
#     ]
#     split_space_search = ' '
#
#     class Meta:
#         model = FichaCostoProducto
#         fields = [
#             'tipoficha',
#             'cantidad',
#             'activa',
#             'fecha',
#             'medida',
#             'producto',
#         ]
#
#         form = FichaCostoGroupedFormFilter
#
#         filter_overrides = {
#             models.ForeignKey: {
#                 'filter_class': django_filters.ModelMultipleChoiceFilter,
#                 'extra': lambda f: {
#                     'queryset': django_filters.filterset.remote_queryset(f),
#                 }
#             },
#         }
#
# class VarGlobalesCostoDatosFilter(django_filters.FilterSet):
#     """
#     Filtro para VarGlobalesCostoDatos.
#     Permite filtrar por centrocosto (a través de VarGlobalesCosto),
#     variable_global, destino y valor.
#     """
#
#     # === Filtro por Centro de Costo (relación FK a través de varglobalescosto) ===
#     centrocosto = django_filters.ModelChoiceFilter(
#         queryset=CentroCosto.objects.all(),
#         field_name='varglobalescosto__centrocosto',  # ¡Clave! Relación cruzada
#         label=_("Centro de Costo"),
#         widget=forms.RadioSelect(),
#     )
#
#     # === Filtros directos ===
#     variable_global = django_filters.ModelChoiceFilter(
#         queryset=CostoVarGlobales.objects.all(),
#         field_name='variable_global',
#         label=_("Variable Global"),
#         widget=forms.Select(attrs={'class': 'form-select'}),
#     )
#
#     destino = django_filters.ChoiceFilter(
#         choices=Destino.choices,
#         field_name='destino',
#         label=_("Destino"),
#         empty_label=_("Todos los destinos"),
#         widget=forms.Select(attrs={'class': 'form-select'}),
#     )
#
#     valor = django_filters.RangeFilter(
#         field_name='valor',
#         label=_("Valor (Rango)"),
#         widget=django_filters.widgets.RangeWidget(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': '0.00'
#             }
#         )
#     )
#
#     split_space_search = ' '
#
#     class Meta:
#         model = VarGlobalesCostoDatos
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Si quieres que el filtro de centrocosto dispare HTMX:
#         if 'centrocosto' in self.form.fields:
#             self.form.fields['centrocosto'].label = False
#             self.form.fields['centrocosto'].widget.attrs.update({
#                 'hx-get': reverse_lazy(crud_url_name(VarGlobalesCostoDatos, 'list', 'app_index:costo:')),
#                 'hx-target': "#table_content_varglobales_swap",
#                 'hx-include': '[name="centrocosto"],[name="variable_global"],[name="destino"]',
#                 'hx-swap': 'outerHTML',
#                 'hx-trigger': "change",
#                 'hx-push-url': 'true',
#                 'hx-replace-url': 'true',
#                 'class': 'form-select',
#             })
#
# # ------ FechaProcesamientoCosto / Filter ------
# class FechaProcesamientoCostoFilter(MyGenericFilter):
#     search_fields = [
#         'ueb__icontains',
#     ]
#     split_space_search = ' '
#
#     class Meta:
#         model = FechaProcesamientoCosto
#         fields = [
#             'ueb',
#             'anno',
#             'mes',
#         ]
#
#         form = FechaProcesamientoCostoFormFilter
#
#         filter_overrides = {
#             models.ForeignKey: {
#                 'filter_class': django_filters.ModelMultipleChoiceFilter,
#                 'extra': lambda f: {
#                     'queryset': django_filters.filterset.remote_queryset(f),
#                 }
#             },
#         }
