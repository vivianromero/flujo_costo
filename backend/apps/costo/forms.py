# from datetime import date
# from decimal import Decimal
#
# from crispy_forms.bootstrap import (
#     TabHolder,
#     Tab, FormActions, AppendedText, UneditableField, )
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, Field, HTML
# from django import forms
# from django.template.loader import get_template
# from django.urls import reverse_lazy
# from django.utils.safestring import mark_safe
# from django.utils.translation import gettext as _
#
# from apps.app_index.widgets import MyCustomDateRangeWidget
# from apps.codificadores import ChoiceTiposProd
# from apps.costo.models import *
# from apps.cruds_adminlte3.utils import (
#     common_filter_form_actions, )
# from apps.cruds_adminlte3.widgets import SelectWidget
# from . import CHOICES_MESES
# from django.db.models import Q
#
#
# # ------------ Fichas de Costo / Form ------------
# class FichaCostoProductoForm(forms.ModelForm):
#     medida = forms.ModelChoiceField(
#         queryset=Medida.objects.all(),
#         label=_("Medida"),
#         required=True,
#     )
#
#     query_prod = ProductoFlujo.objects.filter(tipoproducto__in=[ChoiceTiposProd.VITOLA, ChoiceTiposProd.LINEASALIDA])
#     producto = forms.ModelChoiceField(
#         queryset=query_prod,
#         label=_("Producto"),
#         required=True,
#     )
#
#     fecha = forms.DateField(
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
#     )
#     class Meta:
#         model = FichaCostoProducto
#         fields = [
#             'fecha',
#             'tipoficha',
#             'producto',
#             'medida',
#             'cantidad',
#         ]
#
#         widgets = {
#             'tipoficha': SelectWidget(
#                 attrs={'style': 'width: 100%',
#                        'hx-get': reverse_lazy('app_index:costo:productotipoficha'),
#                        'hx-target': '#div_id_producto',
#                        'hx-trigger': 'change',
#                        }
#             ),
#             'medida': SelectWidget(
#                 attrs={'style': 'width: 100%'}
#             ),
#         }
#
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         data = kwargs.get('data', None)
#         self.user = kwargs.pop('user', None)
#         self.producto = kwargs.pop('producto', None)
#         self.tipoficha = kwargs.pop('tipoficha', None)
#         self.post = kwargs.pop('post', None)
#         producto = ProductoFlujo.objects.select_related('tipoproducto').get(codigo=self.producto.split('|')[0].strip()) if self.producto else None
#         if producto:
#             tipofi = TipoFichaCosto.TORCIDO if producto.tipoproducto.id == ChoiceTiposProd.VITOLA else TipoFichaCosto.TERMINADO
#             kwargs['initial'] = {'producto': producto, 'medida': producto.medida, 'tipoficha': tipofi}
#
#         super().__init__(*args, **kwargs)
#
#         self.fields['producto'].widget.attrs = {'style': 'width: 100%',
#                                                 'hx-get': reverse_lazy('app_index:productmedida'),
#                                                 'hx-target': '#div_id_medida',
#                                                 'hx-trigger': 'change',
#                                                 'hx-include': '[name="tipoficha"]',}
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fichacosto_Form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         if instance:
#             self.fields["tipoficha"].disabled = True
#
#         self.helper.layout = Layout(
#             TabHolder(
#                 Tab(
#                     'Ficha de Costo',
#                     Row(
#                         Column(
#                             Field('fecha', id='id_fecha_fichacosto', ),
#                             css_class='form-group col-md-2 mb-0'
#                         ),
#                         Column('tipoficha', css_class='form-group col-md-2 mb-0'),
#                         Column('producto', css_class='form-group col-md-4 mb-0'),
#                         Column('medida', css_class='form-group col-md-2 mb-0'),
#                         Column('cantidad', css_class='form-group col-md-2 mb-0'),
#                         css_class='form-row'
#                     ),
#                 ),
#             ),
#         )
#         self.helper.layout.append(
#             FormActions(
#                 HTML(
#                     get_template('cruds/actions/hx_common_form_actions.html').template.source
#                 )
#             )
#         )
#
#     def clean_cantidad(self):
#         cantidad = self.cleaned_data.get('cantidad')
#         if float(cantidad) <= 0:
#             raise forms.ValidationError('Debe introducir un valor > 0')
#         return cantidad
#
#     @transaction.atomic
#     def save(self, commit=True):
#         instance = super().save(commit=True)
#         filas = FichaCostoFilas.objects.all()
#         if instance.tipoficha == TipoFichaCosto.TORCIDO:
#             filas = filas.exclude(fila='1.2')
#         datos = [FichaCostoProductoFilas(fichacostoproducto=instance, fila=f) for f in filas]
#         FichaCostoProductoFilas.objects.bulk_update_or_create(datos,['fichacostoproducto', 'fila'], match_field = ['fichacostoproducto', 'fila'])
#         return instance
#
#
# # ------------ NormaConsumo / Form Filter ------------
# class FichaCostoFormFilter(forms.Form):
#     class Meta:
#         model = FichaCostoProducto
#         fields = [
#             'cantidad',
#             'activa',
#             'fecha',
#             'medida',
#             'producto',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super().__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fichacosto_form_filter'
#         self.helper.form_method = 'GET'
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     'Normas de Consumo',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                     ),
#                     Row(
#                         Column('fecha', css_class='form-group col-md-3 mb-0'),
#                         Column('cantidad', css_class='form-group col-md-3 mb-0'),
#                         Column('activa', css_class='form-group col-md-3 mb-0'),
#                         css_class='form-row',
#                     ),
#                 ),
#                 style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
#             ),
#         )
#
#         self.helper.layout.append(
#             FormActions(
#                 HTML(
#                     get_template('cruds/actions/hx_common_filter_form_actions_normaconsumo.html').template.source
#                 )
#             )
#         )
#
#     def get_context(self):
#         context = super().get_context()
#         if 'tipo' in context['form'].data and int(context['form'].data['tipo']) != 0:
#             self.fields['tipo'].disabled = True
#         context['width_right_sidebar'] = '760px'
#         context['height_right_sidebar'] = '505px'
#         return context
#
#
# class FichaCostoProductoFilasForm(forms.ModelForm):
#     class Meta:
#         model = FichaCostoProductoFilas
#         fields = [
#             'costo',
#         ]
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.costo_editable = kwargs.pop('costo_editable', False)
#
#         super().__init__(*args, **kwargs)
#
#         # Configurar Crispy Forms
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fichacostoProductofilas_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         # Determinar el tipo de widget para 'costo'
#         if self.costo_editable:
#             costo_widget = forms.NumberInput(
#                 attrs={
#                     'class': 'form-control',
#                     'step': '0.01',
#                     'placeholder': 'Ingrese el costo'
#                 }
#             )
#             costo_css = 'form-group col-md-12 mb-0'
#         else:
#             costo_widget = forms.HiddenInput()
#             costo_css = 'form-group col-md-8 mb-0 d-none'  # Opcional: ocultar visualmente
#
#         # Aplicar el widget al campo
#         self.fields['costo'].widget = costo_widget
#
#         # Configurar el layout de Crispy
#         self.helper.layout = Layout(
#             Row(
#                 Field('costo', css_class=costo_css, css_id='productodetalle'),
#                 css_class='form-row'
#             ),
#         )
#
# class FichaCostoProductoFilaDesgloseSalarioAddForm(forms.ModelForm):
#     class Meta:
#         model = FichaCostoProductoFilaDesgloseSalario
#         fields = ['cargo', 'cantidad']
#         widgets = {
#             'cargo': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['cargo'].label_from_instance = lambda obj: "{} | {} | {} | {}".format(
#             getattr(obj, 'codigo', ''),
#             getattr(obj, 'descripcion', ''),
#             getattr(obj, 'grupo', None) and getattr(obj.grupo, 'grupo', '') or '',
#             getattr(obj, 'salario', '')
#         )
#
# class FichaCostoProductoFilasDetailForm(FichaCostoProductoFilasForm):
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fichacostoproductofilas_detail_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             Row(
#                 Column(UneditableField('costo'), css_class='form-group col-md-8 mb-0', css_id='productodetalle'),
#                 css_class='form-row'
#             ),
#         )
#
#
# class FichaCostoGroupedFormFilter(forms.Form):
#     class Meta:
#         model = FichaCostoGrouped
#         fields = [
#             'tipoficha',
#             'cantidad',
#             'activa',
#             'fecha',
#             'medida',
#             'producto',
#             'Producto',
#             'Cantidad_Fichas',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super().__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fichacostogrouped_form_filter'
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     'Fichas de Costo Agrupadas',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                     ),
#                     Row(
#                         Column('tipoficha', css_class='form-group col-md-4 mb-0'),
#                         Column('Cantidad_Fichas', css_class='form-group col-md-4 mb-0'),
#                         Column('Producto', css_class='form-group col-md-8 mb-0'),
#                         css_class='form-row',
#                     ),
#                 ),
#                 style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
#             ),
#         )
#
#         self.helper.layout.append(
#             common_filter_form_actions()
#         )
#
#     def get_context(self):
#         context = super().get_context()
#         context['width_right_sidebar'] = '760px'
#         context['height_right_sidebar'] = '505px'
#         return context
#
# class VarGlobalesCostoDatosForm(forms.ModelForm):
#     centrocosto = forms.CharField(label='', required=False)
#     mes = forms.CharField(label='', required=False)
#     anno = forms.CharField(label='', required=False)
#
#     class Meta:
#         model = VarGlobalesCostoDatos
#         fields = [
#             'variable_global',
#             'destino',
#             'valor',
#             'centrocosto',
#             'mes',
#             'anno',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         self.instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.centrocosto = kwargs.pop('centrocosto', None)
#         self.mes = 1
#         self.anno = 2024
#         self.ueb = self.user.ueb
#
#         self.editar = True if self.instance else False
#
#
#         super(VarGlobalesCostoDatosForm, self).__init__(*args, **kwargs)
#
#         self.fields['mes'].initial = self.mes
#         self.fields['anno'].initial = self.anno
#         self.fields['centrocosto'].initial = self.centrocosto
#
#         vg_queryset = self.fields['variable_global'].queryset
#         varg = None if not self.editar else VarGlobalesCostoDatos.objects.get(pk=self.instance.pk).variable_global
#         dicc_ = {}
#         dicc_vg = {'activa': True}
#         if varg and not varg.activa:
#             dicc_['pk'] = varg.id
#             vg_queryset = vg_queryset.filter(Q(**dicc_vg) | Q(**dicc_))
#         else:
#             vg_queryset = vg_queryset.filter(**dicc_vg)
#
#         self.fields['variable_global'].queryset = vg_queryset
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_varglobdatos_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('variable_global', css_class='form-group col-md-6 mb-0'),
#                 Column('destino', css_class='form-group col-md-2 mb-0'),
#                 Column('valor', css_class='form-group col-md-2 mb-0'),
#                 Field('centrocosto', type="hidden", css_class='form-group col-md-8 mb-0'),
#                 Field('mes', type="hidden", css_class='form-group col-md-8 mb-0'),
#                 Field('anno', type="hidden", css_class='form-group col-md-8 mb-0'),
#                 css_class='form-row'
#             ),
#         )
#         self.helper.layout.append(
#             FormActions(
#                 HTML(
#                     get_template('cruds/actions/hx_common_form_actions.html').template.source
#                 )
#             )
#         )
#
#     def clean_valor(self):
#         valor = self.cleaned_data.get('valor')
#         if valor <= Decimal('0.0000000'):
#             raise forms.ValidationError('El valor debe ser > 0')
#         return valor
#
#     @transaction.atomic
#     def save(self, commit=True):
#         if not self.instance or not self.instance.varglobalescosto_id:
#             cc = CentroCosto.objects.get(pk=self.centrocosto)
#             varglobalcosto, _ = VarGlobalesCosto.objects.update_or_create(
#                             ueb=self.ueb,
#                             centrocosto=cc,
#                             mes=self.mes,
#                             anno=self.anno,
#                             defaults={
#                                 'ueb': self.ueb,
#                                 'centrocosto': cc,
#                                 'mes': self.mes,
#                                 'anno': self.anno,
#                             }
#                         )
#             self.instance.varglobalescosto = varglobalcosto
#         return super().save(commit=True)
#
#
# # ------------ FechaProcesamientoCosto / Form ------------
# class FechaProcesamientoCostoForm(forms.ModelForm):
#     mes = forms.ChoiceField(
#         choices=CHOICES_MESES,
#         label=_('Mes'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     # Campo personalizado para el año
#     anno = forms.ChoiceField(
#         label=_('Año'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     class Meta:
#         model = FechaProcesamientoCosto
#         fields = [
#             'ueb',
#             'mes',
#             'anno',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         # instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(FechaProcesamientoCostoForm, self).__init__(*args, **kwargs)
#         # self.instance = instance
#         current_year = date.today().year
#         year_choices = [(current_year, current_year), (current_year - 1, current_year - 1)]
#
#         self.fields['mes'].initial = date.today().month
#         if self.instance and self.instance.ueb_id:
#             self.fields['mes'].initial = self.instance.mes
#             self.fields['anno'].initial = self.instance.anno
#             self.fields["ueb"].disabled = True
#
#         self.fields['anno'].choices = year_choices
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fechaprocesamiento_Form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             TabHolder(
#                 Tab(
#                     _('Fecha Inicial de Procesamiento del Costo'),
#                     Row(
#                         Column('ueb', css_class='form-group col-md-8 mb-0'),
#                         css_class='form-row'
#                     ),
#                     Row(
#                         Column('mes', css_class='form-group col-md-2 mb-0'),
#                         Column('anno', css_class='form-group col-md-2 mb-0'),
#                         css_class='form-row'
#                     ),
#                 ),
#             ),
#         )
#         self.helper.layout.append(
#             FormActions(
#                 HTML(
#                     get_template('cruds/actions/hx_common_form_actions.html').template.source
#                 )
#             )
#         )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         ueb = cleaned_data.get('ueb')
#         if self.instance and not self.instance.ueb_id:
#             if FechaProcesamientoCosto.objects.filter(ueb=ueb).exists():
#                 self.add_error('ueb',
#                                _('Esta UEB ya tiene fechas de procesamiento registradas. No se pueden agregar más.'))
#         return cleaned_data
#     @transaction.atomic
#     def save(self, commit=True):
#         instance = super().save(commit=True)
#         instance.inicial = True
#         instance.save()
#         return instance
#
#
# # ------------ FechaProcesamientoCosto / Form Filter ------------
# class FechaProcesamientoCostoFormFilter(forms.Form):
#     class Meta:
#         model = FechaProcesamientoCosto
#         fields = [
#             'ueb',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(FechaProcesamientoCostoFormFilter, self).__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_fechaprocesamiento_form_filter'
#         self.helper.form_method = 'GET'
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     _('Fecha Inicio de Procesamiento del Costo'),
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                         Column('ueb', css_class='form-group col-md-8 mb-0'),
#                         css_class='form-row',
#                     ),
#                 ),
#                 style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
#             ),
#         )
#
#         self.helper.layout.append(
#             common_filter_form_actions()
#         )
#
#     def get_context(self):
#         context = super().get_context()
#         context['width_right_sidebar'] = '760px'
#         context['height_right_sidebar'] = '505px'
#         return context

