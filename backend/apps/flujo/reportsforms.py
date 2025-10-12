# from datetime import date
#
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column
# from django import forms
# from django_select2.forms import Select2MultipleWidget
#
# from apps.app_index.widgets import MyCustomDateRangeWidget
# from apps.codificadores import ChoiceTiposProd, ChoiceClasesMatPrima
# from apps.codificadores.models import TipoActividadDepartamento
# from apps.cruds_adminlte3.widgets import SelectWidget
# from apps.flujo import ChoiceReports
# from apps.flujo.models import *
#
#
# # ------------ Report Existencia / Form ------------
# class ReportForm(forms.Form):
#     ESTADO_CHOICES = [(0, '--Todos--')] + list(EstadoProducto.choices)
#
#     element_checkbox = forms.BooleanField(
#         required=False,
#         label=''
#     )
#
#     departamento = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento",
#         required=True,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%;',
#         }
#         )
#     )
#
#     fechai = forms.DateField(
#         widget=MyCustomDateRangeWidget(
#             format='%d/%m/%Y',
#             picker_options={
#                 'showDropdowns': True,
#                 'format': 'DD/MM/YYYY',
#                 'singleDatePicker': True,
#                 'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
#             },
#         ),
#         input_formats=['%d/%m/%Y'],
#         label = 'Desde',
#     )
#
#     fechaf = forms.DateField(
#         widget=MyCustomDateRangeWidget(
#             format='%d/%m/%Y',
#             picker_options={
#                 'showDropdowns': True,
#                 'format': 'DD/MM/YYYY',
#                 'singleDatePicker': True,
#                 'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
#             },
#         ),
#         input_formats=['%d/%m/%Y'],
#         label='Hasta',
#     )
#
#     producto = forms.ModelChoiceField(
#         queryset=ProductoFlujo.objects.all(),
#         label="Producto",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%;',
#         }),
#         empty_label="---Todos---"
#     )
#
#     estados = forms.MultipleChoiceField(
#         choices=ESTADO_CHOICES,
#         required=False,
#         widget=Select2MultipleWidget,
#         label="Selecciona los estados",
#         initial=[0]
#     )
#
#     class Meta:
#         fields = [
#             'departamento',
#             'fechai',
#             'fechaf',
#             'estados',
#             'producto',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.report_type = kwargs.pop('report_type', None)
#         super(ReportForm, self).__init__(*args, **kwargs)
#
#         self.fields['fechai'].initial = date.today().replace(day=1)
#         self.fields['fechai'].widget.attrs['readonly'] = True
#
#         self.fields['fechaf'].initial = date.today()
#         self.fields['fechaf'].widget.attrs['readonly'] = True
#
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#
#         fields_row1 = [
#             Column('fechai', css_class='form-group col-md-2 mb-0'),
#             Column('fechaf', css_class='form-group col-md-2 mb-0'),
#             Column('departamento', css_class='form-group col-md-8 mb-0')
#         ]
#
#         fields_row2 = [
#             Column('producto', css_class='form-group col-md-8 mb-0'),
#             Column('estados', css_class='form-group col-md-4 mb-0'),
#         ]
#
#         fields_row3 = []
#         if self.report_type in [ChoiceReports.EXISTENCIAS]:
#             self.fields['element_checkbox'].label = 'Mostrar existencias en 0'
#             fields_row3 = [
#                 Column('element_checkbox', css_class='form-group col-md-4 mb-0'),
#             ]
#         elif self.report_type in [ChoiceReports.MOVIMIENTOSMP, ChoiceReports.CONTROLPESADAS, ChoiceReports.CONTROLPESADASRESUMEN]:
#             self.fields["estados"].required = False
#             self.fields["departamento"].required = False
#             self.fields['producto'].label = 'Vitola'
#             filtro_producto = {
#                 'tipoproducto': ChoiceTiposProd.VITOLA
#             }
#             filtro_departamento = {
#                 'departamentoactividad': TipoActividadDepartamento.DESPACHO
#             }
#             if self.report_type == ChoiceReports.CONTROLPESADAS or self.report_type == ChoiceReports.CONTROLPESADASRESUMEN:
#                 self.fields['element_checkbox'].label = 'Resumen del Período'
#                 filtro_producto={
#                     'productoflujoclase_producto__clasemateriaprima_id__in':[ChoiceClasesMatPrima.CAPOTE,
#                                                                              ChoiceClasesMatPrima.F1, ChoiceClasesMatPrima.F2,
#                                                                              ChoiceClasesMatPrima.F3, ChoiceClasesMatPrima.F4,
#                                                                              ChoiceClasesMatPrima.PICADURA
#                                                                              ]
#                 }
#                 filtro_departamento = {
#                     'departamentoactividad': TipoActividadDepartamento.PREPMATERIAPRIMA
#                 }
#                 self.fields['producto'].label = 'Producto'
#                 fields_row3 = [
#                     Column('element_checkbox', css_class='form-group col-md-4 mb-0'),
#                 ]
#
#             self.fields['producto'].queryset = self.fields['producto'].queryset.filter(**filtro_producto)
#
#             self.fields["departamento"].queryset = self.fields["departamento"].queryset.filter(**filtro_departamento)
#             fields_row1 = fields_row1[:-1]
#             fields_row1[0]=Column('fechai', css_class='form-group col-md-4 mb-0')
#             fields_row1[1]=Column('fechaf', css_class='form-group col-md-4 mb-0')
#
#             fields_row2 = fields_row2[:-1]
#             fields_row2[0] = Column('producto', css_class='form-group col-md-12 mb-0')
#
#         self.helper.layout = Layout(
#             Row(*fields_row1, css_class='form-row'),
#             Row(*fields_row2, css_class='form-row'),
#             Row(*fields_row3, css_class='form-row'),
#         )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         fechai = cleaned_data.get("fechai")
#         fechaf = cleaned_data.get("fechaf")
#
#         if fechai and fechaf and fechai > fechaf:
#             msg = 'La fecha Hasta debe ser mayor que la fecha Desde'
#             self.add_error('fechaf', msg)
#         return cleaned_data

