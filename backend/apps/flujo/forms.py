# import re
# from datetime import date
#
# from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText, UneditableField
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, HTML, Field, Div
# from django import forms
# from django.core.exceptions import ValidationError
# from django.template.loader import get_template
# from django.urls import reverse_lazy
# from django.utils.safestring import mark_safe
# from django.utils.translation import gettext as _
#
# from apps.app_index.widgets import MyCustomDateRangeWidget
# from apps.codificadores import ChoiceTiposDoc, ChoiceTiposProd
# from apps.codificadores.models import CambioProducto, NumeracionDocumentos, ConfiguracionesGen
# from apps.cruds_adminlte3.utils import (
#     common_filter_form_actions, )
# from apps.cruds_adminlte3.utils import crud_url_name
# from apps.cruds_adminlte3.widgets import SelectWidget
# from apps.flujo.models import *
# from .models import EstadoProducto
# from .utils import genera_numero_doc, actualiza_numeros, dame_productos, dame_precio_salida, \
#     existencia_producto, actualiza_existencias_documentos, dame_productos_departamento
# from django.db.models import Sum
#
# # ------------ Documento / Form ------------
# class DocumentoForm(forms.ModelForm):
#     departamento = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     ueb = forms.ModelChoiceField(
#         queryset=UnidadContable.objects.all(),
#         label="UEB",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     tipodocumento = forms.ModelChoiceField(
#         queryset=TipoDocumento.objects.all(),
#         label="Tipo Documento",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     motivoajuste = forms.ModelChoiceField(
#         queryset=MotivoAjuste.objects.all(),
#         label="Motivo Ajuste",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     estado = forms.CharField(label='', required=False)
#     mes = forms.CharField(label='', required=False)
#     anno = forms.CharField(label='', required=False)
#
#     departamento_destino = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento Destino",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     departamento_origen = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento Origen",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     ueb_destino = forms.ModelChoiceField(
#         queryset=UnidadContable.objects.filter(activo=True),
#         label="U.E.B Destino",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     ueb_origen = forms.ModelChoiceField(
#         queryset=UnidadContable.objects.filter(activo=True),
#         label="U.E.B Origen",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     class Meta:
#         model = Documento
#         fields = [
#             'fecha',
#             'numerocontrol',
#             'numeroconsecutivo',
#             'suma_importe',
#             'observaciones',
#             'estado',
#             'reproceso',
#             'editar_nc',
#             'comprob',
#             'departamento',
#             'tipodocumento',
#             'ueb',
#             'motivoajuste',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         data = kwargs.get('data', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.departamento = kwargs.pop('departamento', None)
#         self.tipo_doc = kwargs.pop('tipo_doc', 0)
#         self.fecha_procesamiento = kwargs.pop('fecha_procesamiento', None)
#
#         super(DocumentoForm, self).__init__(*args, **kwargs)
#         self.fields['departamento_destino'].label = False
#         self.fields['departamento_origen'].label = False
#         self.fields['departamento'].label = False
#         self.fields['ueb_origen'].label = False
#         self.fields['ueb_destino'].label = False
#         self.origen_dpto = False
#         self.destino_dpto = False
#         self.motivo = False
#         self.destino_ueb = False
#         self.origen_ueb = False
#         self.edicion = False if not instance else True
#         self.numeroconcecutivo_anterior = None if not instance else Documento.objects.get(
#             pk=instance.pk).numeroconsecutivo
#
#         otras_conf = ConfiguracionesGen.objects.get_cached_data()
#
#         self.es_centralizado = False if not otras_conf or not 'Sistema Centralizado' in otras_conf.keys() or \
#                                         otras_conf[
#                                             'Sistema Centralizado']['activo'] == False else True
#         dicc = {}
#         self.fields['estado'].initial = EstadosDocumentos.EDICION
#         if self.user:
#             self.fields['ueb'].initial = self.user.ueb
#             dicc['unidadcontable'] = self.user.ueb
#
#         if self.tipo_doc:
#             self.fields['tipodocumento'].initial = self.tipo_doc
#
#         if self.departamento:
#             self.fields['departamento'].initial = self.departamento
#
#         conf_numeracion = NumeracionDocumentos.objects_cache.get_cached_data()
#         self.numeracion_doc_conf_consecutivo = conf_numeracion[TipoNumeroDoc.NUMERO_CONSECUTIVO]
#         self.numeracion_doc_conf_control = conf_numeracion[TipoNumeroDoc.NUMERO_CONTROL]
#         if self.numeracion_doc_conf_consecutivo and 'numeroconsecutivo' in self.fields.keys():
#             self.fields["numeroconsecutivo"].widget.attrs['readonly'] = \
#                 self.numeracion_doc_conf_consecutivo['sistema']
#
#             self.fields["numerocontrol"].widget.attrs['readonly'] = \
#                 self.numeracion_doc_conf_control['sistema']
#
#         if instance:
#             self.tipo_doc = instance.tipodocumento.pk
#             self.fields['tipodocumento'].initial = instance.tipodocumento
#             self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
#             self.fields['departamento'].widget.enabled_choices = [instance.departamento]
#             self.fields['departamento'].initial = instance.departamento
#             self.fields['estado'].initial = instance.estado
#             self.fields['numeroconsecutivo'].initial = instance.numeroconsecutivo
#             self.fields['numerocontrol'].initial = instance.numerocontrol
#
#         if self.fecha_procesamiento or self.edicion:
#             self.fields['fecha'].initial = self.fecha_procesamiento
#             self.fields['fecha'].widget.attrs['readonly'] = True
#
#             self.fields['fecha'].initial = self.fecha_procesamiento
#             self.fields['fecha'].widget.attrs['readonly'] = True
#
#             numeros = genera_numero_doc(self.departamento, self.user.ueb, self.tipo_doc, self.numeracion_doc_conf_consecutivo, self.numeracion_doc_conf_control)
#
#             numero_consec = str(numeros[0][0])
#             self.fields['numeroconsecutivo'].initial = numero_consec
#
#             numero_ctrl = str(numeros[1][0]) if not numeros[1][2] else numeros[1][2] + '/' + str(numeros[1][0])
#             self.fields['numerocontrol'].initial = numero_ctrl
#
#             match int(self.tipo_doc):
#                 case ChoiceTiposDoc.AJUSTE_AUMENTO | ChoiceTiposDoc.AJUSTE_DISMINUCION:
#                     self.motivo = True
#                     dicc_ma = {}
#                     dicc_ma['aumento'] = int(self.tipo_doc) == ChoiceTiposDoc.AJUSTE_AUMENTO
#                     motivo_queryset = self.fields['motivoajuste'].queryset
#                     motivo = None if not instance else DocumentoAjuste.objects.get(documento=instance).motivoajuste
#                     dicc_ = {}
#                     if motivo and not motivo.activo:
#                         dicc_['pk'] = motivo.id
#                         motivo_queryset = motivo_queryset.filter(Q(**dicc_ma) | Q(**dicc_))
#                     else:
#                         dicc_ma.update({'activo': True})
#                         motivo_queryset = motivo_queryset.filter(**dicc_ma)
#
#                     self.fields['motivoajuste'].queryset = motivo_queryset
#                     self.fields['motivoajuste'].initial = motivo
#                     self.fields['motivoajuste'].widget.attrs = {'style': 'width: 100%;', }
#                     self.fields['motivoajuste'].label = "Motivo de Ajuste"
#                     self.fields['motivoajuste'].disabled = False
#                     self.fields['motivoajuste'].required = True
#                 case ChoiceTiposDoc.TRANSF_HACIA_DPTO:
#                     self.destino_dpto = True
#                     destino_queryset = self.fields['departamento_destino'].queryset
#                     dicc['relaciondepartamento'] = instance.departamento if instance else self.departamento
#                     destino = None if not instance else DocumentoTransfDepartamento.objects.get(documento=instance).departamento
#
#                     destino_queryset = destino_queryset.filter(**dicc)
#                     dptos_no_inicializados = [
#                         x.pk for x in destino_queryset if
#                         not x.fechainicio_departamento.filter(ueb=dicc['unidadcontable']).all().exists()
#                     ]
#                     self.fields['departamento_destino'].queryset = destino_queryset.exclude(pk__in=dptos_no_inicializados)
#                     self.fields['departamento_destino'].initial = destino
#                     self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%;', }
#                     self.fields['departamento_destino'].label = "Departamento Destino"
#                     self.fields['departamento_destino'].disabled = False
#                     self.fields['departamento_destino'].required = True
#                 case ChoiceTiposDoc.TRANSF_DESDE_DPTO | ChoiceTiposDoc.DEVOLUCION_RECIBIDA:
#                     self.origen_dpto = True
#                     origen_queryset = self.fields['departamento_origen'].queryset
#                     if self.tipo_doc == ChoiceTiposDoc.DEVOLUCION_RECIBIDA:
#                         doc_origen = DocumentoDevolucionRecibida.objects.get(documento=instance)
#                         origen = doc_origen.documentoorigen
#                         origen_queryset = origen_queryset.filter(pk=origen.departamento.pk)
#                         if origen.ueb != dicc['unidadcontable']:
#                             self.origen_ueb = True
#                             origen_ueb_queryset = self.fields['ueb_origen'].queryset.exclude(pk=dicc['unidadcontable'].pk)
#                             self.fields['ueb_origen'].queryset = origen_ueb_queryset
#                             self.fields['ueb_origen'].initial = origen.ueb
#                             self.fields['ueb_origen'].widget.enabled_choices = [origen.ueb]
#                             self.fields['ueb_origen'].widget.attrs = {'style': 'width: 100%;', }
#                             self.fields['ueb_origen'].label = "U.E.B Origen"
#                             self.fields['ueb_origen'].disabled = False
#                             self.fields['ueb_origen'].required = True
#                     else:
#                         origen_queryset = origen_queryset.filter(relaciondepartamento=instance.departamento)
#                         origen = DocumentoTransfDepartamentoRecibida.objects.get(documento=instance).documentoorigen
#
#                     self.fields['departamento_origen'].queryset = origen_queryset
#                     self.fields['departamento_origen'].initial = origen.departamento
#                     self.fields['departamento_origen'].widget.enabled_choices = [origen.departamento]
#                     self.fields['departamento_origen'].widget.attrs = {'style': 'width: 100%;', }
#                     self.fields['departamento_origen'].label = "Departamento Origen"
#                     self.fields['departamento_origen'].disabled = False
#                     self.fields['departamento_origen'].required = True
#                 case ChoiceTiposDoc.TRANSFERENCIA_EXTERNA:
#                     self.destino_ueb = True
#                     destino_queryset = self.fields['ueb_destino'].queryset.exclude(pk=dicc['unidadcontable'].pk)
#                     self.fields['ueb_destino'].queryset = destino_queryset
#                     destino = DocumentoTransfExterna.objects.get(documento=instance).unidadcontable if instance else None
#                     if data:
#                         destino = data.get('ueb_destino')
#
#                     self.fields['ueb_destino'].initial = destino
#                     self.fields['ueb_destino'].widget.attrs = {'style': 'width: 100%;', }
#                     self.fields['ueb_destino'].label = "U.E.B Destino"
#                     self.fields['ueb_destino'].disabled = False
#                     self.fields['ueb_destino'].required = True
#
#                 case ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA:
#                     self.origen_ueb = True
#                     origen_queryset = self.fields['ueb_origen'].queryset
#                     origen_queryset = origen_queryset.exclude(pk=self.user.ueb.pk)
#                     self.fields['ueb_origen'].queryset = origen_queryset
#
#                     if self.edicion:
#                         origen = DocumentoTransfExternaRecibida.objects.get(documento=instance).unidadcontable
#
#                         self.fields['ueb_origen'].initial = origen
#
#                     self.fields['ueb_origen'].widget.attrs = {'style': 'width: 100%;', }
#                     self.fields['ueb_origen'].label = "U.E.B Origen"
#                     self.fields['ueb_origen'].disabled = False
#                     self.fields['ueb_origen'].required = True
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_documento_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column(
#                     Field('fecha', id='id_fecha_documento_form', ),
#                     css_class='form-group col-md-3 mb-0'
#                 ),
#                 Column('numeroconsecutivo', css_class='form-group col-md-3 mb-0'),
#                 Column('numerocontrol', css_class='form-group col-md-3 mb-0'),
#                 Field('motivoajuste', type="hidden") if not self.motivo else Column('motivoajuste', css_class='form-group col-md-3 mb-0'),
#                 Field('ueb_destino', type="hidden") if not self.destino_ueb else Column('ueb_destino', css_class='form-group col-md-3 mb-0'),
#                 Field('ueb_origen', type="hidden") if not self.origen_ueb else Column('ueb_origen', css_class='form-group col-md-3 mb-0'),
#                 Field('departamento_destino', type="hidden") if not self.destino_dpto else Column('departamento_destino', css_class='form-group col-md-3 mb-0'),
#                 Field('departamento_origen', type="hidden") if not self.origen_dpto else Column('departamento_origen', css_class='form-group col-md-3 mb-0'),
#                 Field('departamento', type="hidden"),
#                 Field('tipodocumento', type="hidden"),
#                 Field('suma_importe', type="hidden"),
#                 Field('estado', type="hidden"),
#                 Field('ueb', type="hidden"),
#                 Field('mes', type="hidden"),
#                 Field('anno', type="hidden"),
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
#     def clean(self):
#         if not self.numeracion_doc_conf_control['sistema']:
#             cleaned_data = super().clean()
#             numerocontrol = cleaned_data.get('numerocontrol')
#             if self.numeracion_doc_conf_control['prefijo']:
#                 pattern = r'^\d+$|^[a-zA-Z]+/\d+$'
#                 mess_err = 'El campo debe ser un número o una cadena seguida de "/" y un número (ej. "ABC/123").'
#                 validado = re.match(pattern, numerocontrol) if numerocontrol else False
#             else:
#                 validado = numerocontrol.isdigit() if numerocontrol else False
#                 mess_err = 'El campo debe contener solo números.'
#
#             if not validado:
#                 self.add_error('numerocontrol', mess_err)
#             return cleaned_data
#
#
#     @transaction.atomic
#     def save(self, commit=True):
#         # si los numeros son controlados por el sistema
#         control_sistema = self.numeracion_doc_conf_control['sistema']
#         control_departamento = self.numeracion_doc_conf_control['departamento']
#         consec_sistema = self.numeracion_doc_conf_consecutivo['sistema']
#         consec_departamento = self.numeracion_doc_conf_consecutivo['departamento']
#
#         # actualiza el campo donde se guarda el tipo de configuracion de los documentos para aplicar las constraints
#         self.instance.confconsec = ConfigNumero.DEPARTAMENTO if self.numeracion_doc_conf_consecutivo[
#             'departamento'] else ConfigNumero.UNICO
#         self.instance.confcontrol = ConfigNumero.DEPARTAMENTO if self.numeracion_doc_conf_control[
#             'departamento'] else ConfigNumero.UNICO
#
#         # se bloquea el documento
#         doc = Documento.objects.select_for_update().filter(pk=self.instance.pk)
#         numeroconsec_antes = self.instance.numeroconsecutivo if not doc.exists() else doc[0].numeroconsecutivo
#         NumeroDocumentos.objects.select_for_update().filter(ueb=self.user.ueb)
#         numeros_consec = genera_numero_doc(self.instance.departamento, self.instance.ueb,
#                                            self.instance.tipodocumento.pk, self.numeracion_doc_conf_consecutivo, self.numeracion_doc_conf_control)
#
#         partes_control = self.instance.numerocontrol.split('/')
#         numero_control = partes_control[len(partes_control) - 1]
#
#         numeroconsecutivo = self.instance.numeroconsecutivo
#
#         tipo_doc = TipoDocumento.objects.get_cached_data()
#         if prefijo := tipo_doc[self.instance.tipodocumento.pk].get('prefijo'):
#             numero_control = prefijo + '/' + numero_control
#
#         if not self.edicion:
#             # numero consecutivo y de control se actualizan si los controla el sistema, porque puede que se halla salvado un documento
#             # después de haber asignado el numero al documento actual
#             numeroconsecutivo = numeros_consec[0][
#                 0] if consec_sistema else self.instance.numeroconsecutivo
#
#             numero_control = numero_control if not control_sistema else str(
#                 numeros_consec[1][0]) if not numeros_consec[1][2] else numeros_consec[1][2] + '/' + str(
#                 numeros_consec[1][0])
#
#         # se va a actualizar la tabla que lleva el control de los numeros
#
#         # numeros de la instancia
#         partes_control = numero_control.split('/')
#         control = int(partes_control[len(partes_control) - 1])
#
#         actualiza_numeros(ueb=self.instance.ueb,
#                           departamento=None if not consec_departamento else self.instance.departamento,
#                           consecutivo=numeroconsecutivo, control=control, pk=self.instance.pk
#                           )
#
#         self.instance.mes = self.instance.fecha.month
#         self.instance.anno = self.instance.fecha.year
#         self.instance.numeroconsecutivo = numeroconsecutivo
#         self.instance.numerocontrol = numero_control
#
#         doc_error = False
#         estado = EstadosDocumentos.EDICION
#         detall = self.instance.documentodetalle_documento.filter(existencia__lt=0)
#
#         if detall.exists():
#             doc_error = True
#             estado = EstadosDocumentos.ERRORES
#
#         self.instance.error = doc_error
#         self.instance.estado = estado
#
#         instance = super().save(commit=True)
#
#         match self.cleaned_data['tipodocumento'].pk:
#             case ChoiceTiposDoc.AJUSTE_AUMENTO | ChoiceTiposDoc.AJUSTE_DISMINUCION:
#                 motivoajuste = self.cleaned_data.get('motivoajuste')
#                 DocumentoAjuste.objects.update_or_create(
#                     documento=instance,
#                     defaults={
#                         'motivoajuste': motivoajuste,
#                     }
#                 )
#             case ChoiceTiposDoc.TRANSF_HACIA_DPTO:
#                 departamento_destino = self.cleaned_data.get('departamento_destino')
#                 if departamento_destino:
#                     documento_transf_departamento = DocumentoTransfDepartamento.objects.update_or_create(
#                         documento=instance,
#                         defaults={
#                             'departamento': departamento_destino,
#                         }
#                     )
#             case ChoiceTiposDoc.TRANSFERENCIA_EXTERNA:
#                 ueb_destino = self.cleaned_data.get('ueb_destino')
#
#                 if ueb_destino:
#                     documento_transf_ext = DocumentoTransfExterna.objects.update_or_create(
#                         documento=instance,
#                         defaults={
#                             'unidadcontable': ueb_destino,
#                         }
#                     )
#                     otras_conf = ConfiguracionesGen.objects.get_cached_data()
#                     es_centralizado = True if otras_conf and 'Sistema Centralizado' in otras_conf.keys() and \
#                                               otras_conf[
#                                                   'Sistema Centralizado']['activo'] == True else False
#             case ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA:
#                 ueb_origen = self.cleaned_data.get('ueb_origen')
#                 documento_recibir_transf_ext = DocumentoTransfExternaRecibida.objects.update_or_create(
#                     documento=instance,
#                     defaults={
#                         'unidadcontable': ueb_origen,
#                     }
#                 )
#         return instance
#
#
# class DocumentoDetailForm(forms.ModelForm):
#     departamento_destino = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento Destino",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     motivoajuste = forms.ModelChoiceField(
#         queryset=MotivoAjuste.objects.all(),
#         label="Motivo de Ajuste",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     departamento_origen = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento Origen",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%;',
#         }
#         )
#     )
#
#     class Meta:
#         model = Documento
#         fields = [
#             'fecha',
#             'numerocontrol',
#             'numeroconsecutivo',
#             'suma_importe',
#             'observaciones',
#             'estado',
#             'reproceso',
#             'editar_nc',
#             'comprob',
#             'departamento',
#             'tipodocumento',
#             'ueb',
#             'departamento_destino',
#             'motivoajuste',
#             'mes',
#             'anno'
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         data = kwargs.get('data', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.departamento = kwargs.pop('departamento', None)
#         self.tipo_doc = kwargs.pop('tipo_doc', None)
#         self.destino_tipo_documento = [ChoiceTiposDoc.TRANSF_HACIA_DPTO, ]
#         super(DocumentoDetailForm, self).__init__(*args, **kwargs)
#         self.origen_tipo_documento = [ChoiceTiposDoc.TRANSF_DESDE_DPTO, ]
#         super(DocumentoDetailForm, self).__init__(*args, **kwargs)
#         self.fields['departamento_destino'].label = ""
#         self.fields['departamento_origen'].label = ""
#         self.fields['motivoajuste'].label = ""
#         self.origen = False
#         self.motivo = False
#         self.edicion = False if not instance else True  # Documento.objects.filter(pk=instance.pk).exists()
#         self.numeroconcecutivo_anterior = None if not instance else Documento.objects.get(
#             pk=instance.pk).numeroconsecutivo  # Documento.objects.filter(pk=instance.pk).exists()
#
#         numconf = NumeracionDocumentos.objects_cache.get_cached_data()
#
#         numeracion_doc_conf_consecutivo = numconf[TipoNumeroDoc.NUMERO_CONSECUTIVO]
#         numeracion_doc_conf_control = numconf[TipoNumeroDoc.NUMERO_CONTROL]
#         if instance:
#             self.fields['departamento'].widget.enabled_choices = [instance.departamento]
#             self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
#             if numeracion_doc_conf_consecutivo:
#                 self.fields["numeroconsecutivo"].widget.attrs['readonly'] = \
#                     numeracion_doc_conf_consecutivo['sistema']
#
#                 self.fields["numerocontrol"].widget.attrs['readonly'] = \
#                     numeracion_doc_conf_control['sistema']
#
#             if instance.tipodocumento.pk in self.destino_tipo_documento:
#                 destino_queryset = self.fields['departamento_destino'].queryset.filter(
#                     relaciondepartamento=instance.departamento)
#                 self.fields['departamento_destino'].queryset = destino_queryset
#                 destino = DocumentoTransfDepartamento.objects.get(documento=instance)
#                 self.fields['departamento_destino'].initial = destino.departamento
#                 self.fields['departamento_destino'].widget.enabled_choices = [destino.departamento]
#                 self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%; display: block;', }
#                 self.fields['departamento_destino'].label = "Departamento Destino"
#                 self.fields['departamento_destino'].disabled = False
#                 self.fields['departamento_destino'].required = True
#             elif instance.tipodocumento.pk in [ChoiceTiposDoc.AJUSTE_AUMENTO, ChoiceTiposDoc.AJUSTE_DISMINUCION] \
#                     and instance.documentoajuste_documento.exists():
#                 self.motivo = True
#                 motivoajuste_query = self.fields['motivoajuste'].queryset.filter(
#                     pk=instance.documentoajuste_documento.get().motivoajuste.pk)
#                 self.fields['motivoajuste'].queryset = motivoajuste_query
#                 motivo = DocumentoAjuste.objects.get(documento=instance).motivoajuste
#                 self.fields['motivoajuste'].initial = motivo
#                 self.fields['motivoajuste'].widget.enabled_choices = [motivo]
#                 self.fields['motivoajuste'].widget.attrs = {'style': 'width: 100%; display: block;', }
#                 self.fields['motivoajuste'].label = "Motivo de Ajuste"
#                 self.fields['motivoajuste'].disabled = False
#                 self.fields['motivoajuste'].required = True
#         elif data:
#             self.fields['departamento'].widget.enabled_choices = [data.get('departamento', None)]
#             self.fields['tipodocumento'].widget.enabled_choices = [data.get('tipodocumento', None)]
#             estado = data.get('estado')
#             self.fields['estado'].initial = estado if estado != '' else EstadosDocumentos.EDICION
#             if int(data.get('tipodocumento')) in self.destino_tipo_documento:
#                 destino = data.get('departamento_destino')
#                 self.fields['departamento_destino'].initial = destino
#                 self.fields['departamento_destino'].disabled = False
#                 self.fields['departamento_destino'].required = True
#         else:
#             if self.departamento:
#                 self.fields['departamento'].initial = self.departamento
#                 self.fields['departamento'].widget.enabled_choices = [self.departamento]
#                 self.fields['estado'].initial = EstadosDocumentos.EDICION
#             if self.tipo_doc:
#                 self.fields['tipodocumento'].initial = self.tipo_doc
#                 self.fields['tipodocumento'].widget.enabled_choices = [self.tipo_doc]
#
#                 if int(self.tipo_doc) in self.destino_tipo_documento:
#                     destino_queryset = self.fields['departamento_destino'].queryset.filter(
#                         relaciondepartamento=self.departamento)
#                     self.fields['departamento_destino'].queryset = destino_queryset
#                     self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%; display: block;', }
#                     self.fields['departamento_destino'].label = "Departamento Destino"
#                     self.fields['departamento_destino'].disabled = False
#                     self.fields['departamento_destino'].required = True
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_documento_detalle__form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column(
#                     UneditableField('fecha', id='id_fecha_documentodetail_form', ),
#                     css_class='form-group col-md-3 mb-0'
#                 ),
#                 Column(UneditableField('numeroconsecutivo'), css_class='form-group col-md-3 mb-0'),
#                 Column(UneditableField('numerocontrol'), css_class='form-group col-md-3 mb-0'),
#                 Field('motivoajuste', type="hidden") if not self.motivo else Column(UneditableField('motivoajuste'), css_class='form-group col-md-3 mb-0'),
#                 Column(UneditableField('departamento_destino'), css_class='form-group col-md-3 mb-0'),
#                 Field('departamento', type="hidden"),
#                 Field('tipodocumento', type="hidden"),
#                 Field('suma_importe', type="hidden"),
#                 Field('estado', type="hidden"),
#                 Field('ueb', type="hidden"),
#                 Field('mes', type="hidden"),
#                 Field('anno', type="hidden"),
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
#
# # ------------ DepartamentosDocumento / Form ------------
# class DepartamentoDocumentosForm(DocumentoForm):
#     class Meta(DocumentoForm.Meta):
#         fields = [
#             'departamento',
#         ]
#         widgets = {
#             'departamento': forms.RadioSelect(),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(DepartamentoDocumentosForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_departamentos_documento_form'
#         self.helper.form_method = 'post'
#         self.helper.form_show_labels = False
#
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('departamento', css_class='form-group col-md-12 mb-0'),
#                 css_class='form-row'
#             ),
#         )
#
#
# # ------------ Documento / Form Filter------------
# class DocumentoFormFilter(forms.Form):
#     departamento = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#     )
#     rango_fecha = forms.DateField()
#
#     class Meta:
#         model = Documento
#         fields = [
#             'rango_fecha',
#             'numerocontrol',
#             'numeroconsecutivo',
#             'suma_importe',
#             'observaciones',
#             'estado',
#             'reproceso',
#             'editar_nc',
#             'comprob',
#             'departamento',
#             'tipodocumento',
#             'ueb',
#         ]
#         widgets = {
#             'departamento': forms.RadioSelect(),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(DocumentoFormFilter, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.fields['departamento'].label = False
#         self.fields['departamento'].widget.attrs.update({
#             'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
#             'hx-target': '#table_content_documento_swap',
#             'hx-trigger': "change",
#             'hx-push-url': 'true',
#             'hx-replace-url': 'true',
#         })
#         self.fields['rango_fecha'].label = False
#         self.fields['rango_fecha'].widget.attrs.update({
#             'class': 'class="form-control',
#             'style': 'height: auto; padding: 0;',
#             'hx-ext': 'event-header',
#             'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
#             'hx-target': '#table_content_documento_swap',
#             'hx-trigger': 'change, process_date',
#             'hx-replace-url': 'true',
#             'hx-preserve': 'true',
#             'hx-indicator': '.loading-bar',
#         })
#         self.helper.form_id = 'id_documento_form_filter'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             TabHolder(
#                 Tab(
#                     'Documento',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                     ),
#                     Row(
#                         Column(
#                             Field('fecha', id='id_fecha_documento_formfilter', ),
#                             css_class='col-md-3 mb-0'
#                         ),
#                         Column('numerocontrol', css_class='form-group col-md-3 mb-0'),
#                         Column('numeroconsecutivo', css_class='form-group col-md-3 mb-0'),
#                         Column('suma_importe', css_class='form-group col-md-3 mb-0'),
#                         Column('observaciones', css_class='form-group col-md-3 mb-0'),
#                         Column('estado', css_class='form-group col-md-3 mb-0'),
#                         Column('reproceso', css_class='form-group col-md-3 mb-0'),
#                         Column('editar_nc', css_class='form-group col-md-3 mb-0'),
#                         Column('comprob', css_class='form-group col-md-5 mb-0'),
#                         Column(
#                             Field('departamento', id='id_departamento_documento_formfilter', ),
#                             css_class='form-group col-md-12 mb-0',
#                         ),
#                         Column('tipodocumento', css_class='form-group col-md-5 mb-0'),
#                         Column('ueb', css_class='form-group col-md-5 mb-0'),
#                     ),
#                 ),
#
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
#
# # ------------ DocumentoDetalle / Form ------------
# class DocumentoDetalleForm(forms.ModelForm):
#     documento_hidden = forms.CharField(label='', required=False)
#     operacion_hidden = forms.CharField(label='', required=False)
#
#     producto_destino = forms.ModelChoiceField(
#         queryset=ProductoFlujo.objects.all(),
#         label="Producto Destino",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#
#     estado_destino = forms.ChoiceField(
#         label="Estado Destino",
#         choices=EstadoProducto.choices,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         })
#     )
#
#     class Meta:
#         model = DocumentoDetalle
#         fields = [
#             'cantidad',
#             'precio',
#             'estado',
#             'producto',
#             'producto_destino',
#             'estado_destino',
#         ]
#
#         widgets = {
#             'producto': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%',
#                     'id': 'id_producto_documento_detalle',
#                 }
#             ),
#             'estado': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%; dislay: block',
#                     'id': 'id_estado_documento_detalle',
#                 },
#             ),
#             'cantidad': forms.TextInput(),
#             'precio': forms.TextInput(),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         self.skip_price_validation = kwargs.pop('skip_price_validation', False)
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.cantidad_anterior = Decimal('0.0')
#         self.existencia_product_deficiente = Decimal('0.0')
#         self.documentopadre = kwargs.pop('doc', None)
#         if self.documentopadre and self.documentopadre.tipodocumento.id in [ChoiceTiposDoc.RECEPCION_PRODUCCION,
#                                                                          ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO]:
#             kwargs['initial'] = {'estado': EstadoProducto.BUENO}
#             self.skip_price_validation = True
#
#         if args:
#             self.documentopadre = args[0]['doc']
#
#         self.prod_destino = False
#         if instance:
#             self.cantidad_anterior = instance.cantidad
#
#         super(DocumentoDetalleForm, self).__init__(*args, **kwargs)
#         self.fields['producto'].queryset = dame_productos(self.documentopadre, self.fields['producto'].queryset)
#
#         self.fields['producto_destino'].label = False
#         self.fields['estado_destino'].label = False
#
#         precio_hidden = ''
#
#         match self.documentopadre.tipodocumento.pk:
#             case ChoiceTiposDoc.CAMBIO_PRODUCTO:
#                 self.prod_destino = True
#                 query_origen_producto = self.fields['producto'].queryset
#                 ids_origen = [x.productoo.pk for x in CambioProducto.objects.all()]
#                 query_origen_producto = query_origen_producto.filter(pk__in=ids_origen)
#                 self.fields['producto'].queryset = query_origen_producto
#
#                 self.fields['producto_destino'].label = "Producto destino"
#                 self.fields['producto_destino'].disabled = False
#                 self.fields['producto_destino'].required = True
#
#                 self.fields['estado_destino'].label = "Estado"
#                 self.fields['estado_destino'].disabled = False
#                 self.fields['estado_destino'].required = True
#
#                 if instance:
#                     detalleproducto = instance.documentodetalleproducto_detalle.get()
#                     self.fields['estado_destino'].initial = detalleproducto.estado
#                     self.fields['producto_destino'].initial = detalleproducto.producto
#
#                 self.fields["producto_destino"].widget.attrs = {'hx-get': reverse_lazy('app_index:flujo:productosdestino'),
#                                                                 'hx-target': '#div_id_producto_destino',
#                                                                 'hx-trigger': 'change from:#div_id_producto, change from:#div_id_estado',
#                                                                 'hx-include': '[name="producto"], [name="estado"], [name="documento_hidden"]',
#                                                                 'readonly': True}
#
#                 self.fields["estado_destino"].widget.attrs = {
#                     'hx-get': reverse_lazy('app_index:flujo:estadodestino'),
#                     'hx-target': '#div_id_estado_destino',
#                     'hx-trigger': 'change from:#div_id_estado',
#                     'hx-include': '[name="estado"], [name="documento_hidden"]',
#                     'readonly': True}
#             case ChoiceTiposDoc.CAMBIO_ESTADO:
#
#                 self.fields['estado_destino'].label = "Estado Destino"
#                 self.fields['estado_destino'].disabled = False
#                 self.fields['estado_destino'].required = True
#
#                 if instance:
#                     detalleproducto = instance.documentodetalleestado_detalle.get()
#                     self.fields['estado_destino'].initial = detalleproducto.estado
#
#                 self.fields["estado_destino"].widget.attrs = {'readonly': True}
#             case ChoiceTiposDoc.REPORTE_SUBPRODUCTOS:
#                 self.fields['producto'].queryset = ProductoFlujo.objects.filter(tipoproducto=ChoiceTiposProd.SUBPRODUCTO)
#             case ChoiceTiposDoc.RECEPCION_PRODUCCION | ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO:
#                 self.fields["precio"].required = False
#                 self.fields["precio"].disabled = True
#                 self.fields["estado"].required = False
#                 self.fields["estado"].disabled = True
#                 if instance:
#                     self.fields["producto"].required = False
#                     self.fields["producto"].disabled = True
#             case ChoiceTiposDoc.TRANSF_HACIA_DPTO:
#                 departamento_destino = self.documentopadre.documentotransfdepartamento_documento.get().departamento
#                 claseproducto, tipoproducto = dame_productos_departamento(departamento_destino, OperacionDocumento.ENTRADA)
#                 self.fields['producto'].queryset = ProductoFlujo.objects.filter(Q(tipoproducto__in=tipoproducto) |
#                               Q(productoflujoclase_producto__clasemateriaprima__in=claseproducto))
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_documento_detalle_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#         self.fields['documento_hidden'].initial = '' if not self.documentopadre else self.documentopadre.pk
#         self.fields[
#             'operacion_hidden'].initial = '' if not self.documentopadre else self.documentopadre.tipodocumento.operacion
#
#         if self.fields['operacion_hidden'].initial == OperacionDocumento.SALIDA:
#             self.fields["precio"].widget.attrs = {'hx-get': reverse_lazy('app_index:flujo:precioproducto'),
#                                                   'hx-target': '#div_id_precio',
#                                                   'hx-trigger': 'change from:#div_id_producto, change from:#div_id_estado',
#                                                   'hx-include': '[name="producto"], [name="documento_hidden"], [name="estado"]',
#                                                   'readonly': True}
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('producto', css_class='form-group col-md-6 mb-0',
#                        css_id='id_producto_documento_detalle'),
#                 Column('estado', css_class='form-group col-md-2 mb-0'),
#                 Column(Field('cantidad', data_inputmask="'alias': 'decimal', 'digits': 4"),
#                        css_class='form-group col-md-2 mb-0',
#                        css_id='id_cantidad_documento_detalle'),
#                 Column(Field('precio', data_inputmask="'alias': 'decimal', 'digits': 7", type=precio_hidden),
#                        css_class='form-group col-md-2 mb-0',
#                        css_id='id_precio_documento_detalle'),
#                 Column('producto_destino', css_class='form-group col-md-6 mb-0') if self.prod_destino else Field('producto_destino', type="hidden"),
#                 Column('estado_destino', css_class='form-group col-md-2 mb-0',
#                        css_id='id_estado_destino_documento_detalle'),
#                 Field('documento_hidden', type="hidden"),
#                 Field('operacion_hidden', type="hidden"),
#                 css_class='form-row'
#             ),
#         )
#
#     def clean_cantidad(self):
#         cantidad = self.cleaned_data.get('cantidad')
#         if 'cantidad' in self.changed_data and self.documentopadre.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION and self.instance.documentodetalleproductono_detalle:
#                 cantidad_no = self.instance.documentodetalleproductono_detalle.aggregate(total=Sum('cantidad'))['total'] or Decimal('0.0')
#                 if cantidad_no > cantidad:
#                     raise forms.ValidationError('La cantidad no puede ser modifica, no se corresponde con los Porductos Producidos según Norma Operativa')
#         return cantidad
#     def clean_precio(self):
#         precio = self.cleaned_data.get('precio')
#         if not self.skip_price_validation and precio <= Decimal('0.0000000'):
#             raise forms.ValidationError('El valor debe ser > 0')
#         return precio
#
#     def clean_producto(self):
#         producto = self.cleaned_data.get('producto')
#         if self.documentopadre.tipodocumento.id == ChoiceTiposDoc.TRANSF_HACIA_DPTO:
#             claseproducto, tipoproducto = dame_productos_departamento(self.documentopadre.documentotransfdepartamento_documento.get().departamento, OperacionDocumento.ENTRADA)
#             if (not producto.tipoproducto.id in tipoproducto) and (producto.get_clasemateriaprima and not producto.get_clasemateriaprima.id in claseproducto):
#                 raise forms.ValidationError('El departamento destino no adminte este producto')
#         elif self.documentopadre.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO:
#             self.existencia_product_deficiente, hay_error = existencia_producto(self.documentopadre, producto, EstadoProducto.DEFICIENTE, 0,
#                                                                 1)
#             if self.existencia_product_deficiente < self.cleaned_data.get('cantidad') or hay_error:
#                 raise forms.ValidationError('No existen productos en estado deficiente para ser procesados')
#         return producto
#
#     def clean(self):
#         cleaned_data = super().clean()
#         if self.documentopadre.tipodocumento.pk == ChoiceTiposDoc.CAMBIO_ESTADO:
#             estado_destino = cleaned_data.get('estado_destino')
#             estado = cleaned_data.get('estado')
#             if estado_destino and estado and int(estado_destino) == estado.value:
#                 self.add_error('estado', "Los estados o pueden ser iguales")
#                 self.add_error('estado_destino', "Los estados o pueden ser iguales")
#         return cleaned_data
#
#     @transaction.atomic
#     def save(self, commit=True, doc=None, existencia=None):
#         if not doc:
#             return self.instance
#
#         ueb = doc.ueb
#         producto = self.instance.producto
#         estado = self.instance.estado
#         departamento = doc.departamento
#         operacion = doc.operacion
#         self.instance.documento = doc
#         self.instance.operacion = operacion
#
#         existencia_actual = Decimal(self.instance.existencia) - (Decimal(self.cantidad_anterior) * operacion) + (Decimal(self.instance.cantidad) * operacion) if not existencia else existencia
#         self.instance.existencia = existencia_actual + self.instance.cantidad
#
#         # actualizar las existencias de los demás documentos
#         # tomo la existencia del producto
#         dicc = {'documento__estado__in': [EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES],
#                 'documento__departamento': departamento, 'producto': producto, 'estado': estado,
#                 'documento__ueb': ueb}
#
#         existencia_product, hay_error = existencia_producto(doc, producto, estado, self.instance.cantidad, operacion)
#
#         self.instance.existencia = existencia_product
#         self.instance.error = hay_error
#         precio_producto_reproceso = Decimal('0.00')
#
#         if doc.tipodocumento.pk == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO:
#             precio_producto_reproceso = dame_precio_salida(producto,EstadoProducto.DEFICIENTE,
#                                                  self.instance.documento)
#             self.instance.precio = precio_producto_reproceso
#
#         # se van a actualizar las existencias de los doc posteriores que contienen el producto
#         # y se dejan los documentos con error para actualizar su existencia
#         actualiza_existencias_documentos(doc, producto, estado, existencia_product)
#
#         self.instance.importe = self.instance.precio * self.instance.cantidad
#
#         instance = super().save(commit=True)
#
#         doc_error = False
#         estado = EstadosDocumentos.EDICION
#         detall = doc.documentodetalle_documento.filter(existencia__lt=0).exclude(pk=self.instance.pk)
#
#         if detall.exists() or hay_error:
#             doc_error = True
#             estado = EstadosDocumentos.ERRORES
#
#         doc.error = doc_error
#         doc.estado = estado
#         doc.save(update_fields=['estado', 'error'])
#         if doc.tipodocumento.pk == ChoiceTiposDoc.CAMBIO_PRODUCTO:
#             product_destino = self.cleaned_data.get('producto_destino')
#             est_destino = self.cleaned_data.get('estado_destino')
#             existencia, hay_error = existencia_producto(doc, product_destino, est_destino, instance.cantidad, OperacionDocumento.ENTRADA)
#             if product_destino and est_destino:
#                 detalles_producto_destino_update, detalles_producto_destino_create = DocumentoDetalleProducto.objects.update_or_create(
#                     documentodetalle=instance,
#                     defaults={
#                         'producto': product_destino,
#                         'estado': est_destino,
#                         'existencia': existencia,
#                         'cantidad': self.instance.cantidad,
#                         'precio': self.instance.precio,
#                         'importe': self.instance.precio * self.instance.cantidad
#                     }
#                 )
#                 actualiza_existencias_documentos(doc, product_destino, est_destino, existencia)
#         elif doc.tipodocumento.pk == ChoiceTiposDoc.CAMBIO_ESTADO:
#             est_destino = self.cleaned_data.get('estado_destino')
#             existencia, hay_error = existencia_producto(doc, producto, est_destino,
#                                                         instance.cantidad, 1)
#             if producto and est_destino:
#                 detalles_producto_destino_update, detalles_producto_destino_create = DocumentoDetalleEstado.objects.update_or_create(
#                     documentodetalle=instance,
#                     defaults={
#                         'producto': producto,
#                         'estado': est_destino,
#                         'existencia': existencia,
#                         'cantidad': self.instance.cantidad,
#                         'precio': self.instance.precio,
#                         'importe': self.instance.precio * self.instance.cantidad
#                     }
#                 )
#                 actualiza_existencias_documentos(doc, producto, est_destino, existencia)
#         elif doc.tipodocumento.pk == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO:
#             estado = EstadoProducto.DEFICIENTE
#             existencia, hay_error = existencia_producto(doc, producto, estado,
#                                                         instance.cantidad, -1)
#             detalles_producto_reprocdeficientes_update, detalles_producto_reprocdeficientes_create = DocumentoDetalleReprocesoDeficiente.objects.update_or_create(
#                 documentodetalle=instance,
#                 defaults={
#                     'producto': producto,
#                     'estado': estado,
#                     'existencia': existencia,
#                     'cantidad': self.instance.cantidad,
#                     'precio': precio_producto_reproceso,
#                     'importe': precio_producto_reproceso * self.instance.cantidad,
#                     'error': hay_error
#                 }
#             )
#             actualiza_existencias_documentos(doc, producto, estado, existencia)
#         return self.instance
#
# # ----------- DocumentoDetalleReprocesoForm / Form -------------
# class DocumentoDetalleReprocesoForm(forms.ModelForm):
#     producto = forms.ModelChoiceField(
#         queryset=ProductoFlujo.objects.all(),
#         label="Producto",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: block;',
#         }
#         )
#     )
#     class Meta:
#         model = DocumentoDetalleReproceso
#         fields = [
#             'producto',
#             'estado',
#             'cantidad',
#             'precio',
#         ]
#         widgets = {
#             'estado': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%; dislay: block',
#                     'id': 'id_documentodetallereproceso_estado',
#                 },
#             ),
#             'cantidad': forms.TextInput(),
#             'precio': forms.TextInput(),
#         }
#         labels = {
#             'estado': 'Estado',
#             'precio': 'Precio',
#             'cantidad': 'Cantidad',
#             'producto': 'Producto',
#         }
#
#     def __init__(self, *args, **kwargs):
#         self.documento_detalle = kwargs.pop('doc', None)
#         self.doc = self.documento_detalle.documento if self.documento_detalle else None
#
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         if args and 'doc' in args[0] and not self.doc:
#             self.doc = args[0]['doc']
#         kwargs['initial'] = {'estado': EstadoProducto.BUENO}
#
#         self.skip_price_validation = True
#         super().__init__(*args, **kwargs)
#
#         self.fields["precio"].required = False
#         self.fields["precio"].disabled = True
#         self.fields["estado"].required = False
#         self.fields["estado"].disabled = True
#
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_documentodetallereproceso_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('producto', css_class='form-group col-md-6 mb-0',
#                        css_id='id_documentodetallereproceso_producto'),
#                 Column('estado', css_class='form-group col-md-2 mb-0'),
#                 Column(Field('cantidad', data_inputmask="'alias': 'decimal', 'digits': 4"),
#                        css_class='form-group col-md-2 mb-0',
#                        css_id='id_documentodetallereproceso_cantidad'),
#                 Column(Field('precio', data_inputmask="'alias': 'decimal', 'digits': 7", type=''),
#                        css_class='form-group col-md-2 mb-0', css_id='id_documentodetallereproceso_precio'),
#                 css_class='form-row'
#             ),
#         )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         producto = cleaned_data.get('producto')
#         cantidad = cleaned_data.get('cantidad', Decimal('0.00'))
#
#         existencia_product, hay_error = existencia_producto(self.doc, producto, EstadoProducto.BUENO, cantidad, -1)
#         if existencia_product < cantidad or hay_error:
#             raise forms.ValidationError('No hay existencia de este producto')
#
#         return cleaned_data
#
#     @transaction.atomic
#     def save(self, commit=True, doc=None, existencia=None):
#         if not doc:
#             return self.instance
#
#         documento = doc.documento
#         ueb = documento.ueb
#         departamento = documento.departamento
#         producto = self.instance.producto
#         estado = self.instance.estado
#
#         operacion = -1
#         self.instance.documentodetalle = doc
#         self.instance.operacion = operacion
#
#         existencia_product, hay_error = existencia_producto(documento, producto, estado, self.instance.cantidad, operacion)
#
#         self.instance.existencia = existencia_product
#         self.instance.error = hay_error
#         precio_producto_reproceso = dame_precio_salida(producto, EstadoProducto.BUENO,
#                                                            documento)
#         self.instance.precio = precio_producto_reproceso
#
#         # se van a actualizar las existencias de los doc posteriores que contienen el producto
#         # y se dejan los documentos con error para actualizar su existencia
#         actualiza_existencias_documentos(documento, producto, estado, existencia_product)
#
#         self.instance.importe = self.instance.precio * self.instance.cantidad
#
#         self.instance = super().save(commit=True)
#         return self.instance
#
#
# # ----------- DocumentoDetalleProductoNCForm / Form ------------
# class DocumentoDetalleProductoNCForm(forms.ModelForm):
#     """
#     Formulario para el modelo DocumentoDetalleProductoNC.
#     - Excluye el UUID y gestiona relaciones anidadas.
#     - Valida la coherencia entre normas y productos.
#     """
#     class Meta:
#         model = DocumentoDetalleProductoNC
#         exclude = ['id']  # El UUID se genera automáticamente
#
#         widgets = {
#             # Widget para búsqueda mejorada en ForeignKeys
#             'documentodetalle': forms.HiddenInput(),  # Se setea por el contexto padre
#             'normaconsumodetalles': forms.Select(
#                 attrs={'data-placeholder': 'Seleccione una norma de consumo'}
#             ),
#             'estado': forms.RadioSelect(  # Mejora UX para choices
#                 choices=EstadoProducto.choices
#             )
#         }
#
#     def __init__(self, *args, **kwargs):
#         """
#         Personalización inicial:
#         - Filtra normas activas
#         - Establece valores iniciales basados en el contexto
#         """
#         self.documento_detalle = kwargs.pop('documento_detalle', None)
#         super().__init__(*args, **kwargs)
#
#         if self.documento_detalle:
#             # Filtrar normas por producto del documento
#             self.fields['normaconsumodetalles'].queryset = NormaconsumoDetalle.objects.filter(
#                 normaconsumo__producto=self.documento_detalle.producto,
#                 normaconsumo__activa=True
#             ).select_related('medida')
#
#     def clean(self):
#         """
#         Validaciones adicionales:
#         - Cantidad no puede exceder existencias
#         - Norma debe corresponder al producto
#         """
#         cleaned_data = super().clean()
#         norma = cleaned_data.get('normaconsumodetalles')
#         cantidad = cleaned_data.get('cantidad')
#         existencia = cleaned_data.get('existencia')
#
#         # Validar relación con el producto
#         if norma and self.documento_detalle:
#             if norma.normaconsumo.producto != self.documento_detalle.producto:
#                 raise ValidationError("La norma seleccionada no corresponde al producto del documento")
#
#         # Validar saldo no negativo
#         if cantidad and existencia is not None:
#             if existencia - cantidad < 0:
#                 self.add_error('cantidad', "La cantidad no puede superar la existencia disponible")
#
#         return cleaned_data
#
# class DocumentoDetalleProductoNOForm(forms.Form):
#     fecha_documento = forms.DateField(
#         widget=forms.DateInput(
#             attrs={'type': 'date'},
#             format='%Y-%m-%d'
#         ),
#         input_formats=['%Y-%m-%d'],
#         label="Fecha de la Norma Operativa"
#     )
#
#     def __init__(self, *args, **kwargs):
#         self.documento_detalle = kwargs.pop('documento_detalle', None)
#         kwargs.pop('instance', None)
#         super().__init__(*args, **kwargs)
#
#         # Verificamos que documento_detalle y documento existan antes de usarlos.
#         if self.documento_detalle and hasattr(self.documento_detalle, 'documento'):
#             fecha_documento_padre = self.documento_detalle.documento.fecha
#             if fecha_documento_padre:
#                 max_date = fecha_documento_padre
#                 self.fields['fecha_documento'].widget.attrs.update({
#                     'max': max_date.strftime('%Y-%m-%d')
#                 })
#                 # Definimos la fecha inicial del campo
#                 self.fields['fecha_documento'].initial = max_date
#
#     def clean_fecha_documento(self):
#         fecha_documento_valor = self.cleaned_data.get('fecha_documento')
#         if self.documento_detalle and hasattr(self.documento_detalle, 'documento'):
#             fecha_documento_padre = self.documento_detalle.documento.fecha
#             if fecha_documento_valor and fecha_documento_padre:
#                 if fecha_documento_valor > fecha_documento_padre:
#                     raise forms.ValidationError(
#                         "La fecha no puede ser mayor que la fecha del documento."
#                     )
#         return fecha_documento_valor
#
# # ------------ DocumentoDetalle / Form ------------
# class DocumentoDetalleDetailForm(forms.ModelForm):
#     class Meta:
#         model = DocumentoDetalle
#         fields = [
#             'cantidad',
#             'precio',
#             'estado',
#             'producto',
#             'importe',
#             'existencia',
#         ]
#         widgets = {
#             'producto': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%',
#                     'id': 'id_producto_documento_detalle',
#                 }
#             ),
#             'estado': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%; dislay: block',
#                     'id': 'id_estado_documento_detalle',
#                 },
#             ),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.cantidad_anterior = 0
#         self.documentopadre = kwargs.pop('doc', None)
#         if instance:
#             self.cantidad_anterior = instance.cantidad
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_documento_detalle_detail_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column(UneditableField('producto'), css_class='form-group col-md-4 mb-0',
#                        css_id='id_producto_documento_detail_detalle'),
#                 Column(UneditableField('estado'), css_class='form-group col-md-2 mb-0'),
#                 Column(UneditableField('cantidad'), css_class='form-group col-md-2 mb-0',
#                        css_id='id_cantidad_documento_detail_detalle'),
#                 Column(UneditableField('precio'), css_class='form-group col-md-2 mb-0',
#                        css_id='id_precio_documento_detail_detalle'),
#                 Column(UneditableField('importe'), css_class='form-group col-md-2 mb-0',
#                        css_id='id_precio_documento_detail_detalle'),
#                 Column(UneditableField('existencia'), css_class='form-group col-md-2 mb-0',
#                        css_id='id_precio_documento_detail_detalle'),
#                 css_class='form-row'
#             ),
#         )
#
#
# # ------------ ObtenerDocumentoVersat / Form ------------
# class ObtenerDocumentoVersatForm(forms.Form):
#     iddocumento = forms.CharField(label='No Doc', required=False, widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_numero = forms.CharField(label='No Doc', required=False,
#                                          widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_numctrl = forms.CharField(label='Nro Control', required=False,
#                                           widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_fecha = forms.DateField(label='Fecha', required=False, widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_fecha_hidden = forms.CharField(label='Fecha x', required=False)
#     iddocumento_concepto = forms.CharField(label='Concepto', required=False,
#                                            widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_almacen = forms.CharField(label='Almacén', required=False,
#                                           widget=forms.TextInput(attrs={'readonly': True}))
#     iddocumento_sumaimporte = forms.CharField(label='Importe', required=False,
#                                               widget=forms.TextInput(attrs={'readonly': True}))
#     json_data = forms.JSONField(label='json', required=False, widget=forms.TextInput(attrs={'readonly': True}))
#
#     class Meta:
#         fields = [
#             'iddocumento_numero',
#             'iddocumento_numctrl',
#             'iddocumento_fecha',
#             'iddocumento_concepto',
#             'iddocumento_almacen',
#             'iddocumento_sumaimporte',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(ObtenerDocumentoVersatForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#
#         widget = forms.TextInput(attrs={'readonly': True})
#         self.helper.layout = Layout(
#             Row(
#                 Field('iddocumento', type="hidden"),
#                 Field('json_data', type="hidden"),
#                 Field('iddocumento_fecha_hidden', type="hidden"),
#                 Column(UneditableField('iddocumento_numero'), css_class='form-group col-md-1 mb-0'),
#                 Column(UneditableField('iddocumento_numctrl'), css_class='form-group col-md-2 mb-0'),
#                 Column(UneditableField('iddocumento_fecha'), css_class='form-group col-md-2 mb-0'),
#                 Column(UneditableField('iddocumento_concepto'), css_class='form-group col-md-3 mb-0'),
#                 Column(UneditableField('iddocumento_almacen'), css_class='form-group col-md-3 mb-0'),
#                 Column(UneditableField('iddocumento_sumaimporte'), css_class='form-group col-md-1 mb-0'),
#                 css_class='form-row'
#             ),
#         )
#
#
# # ------------ ObtenerFecha / Form ------------
# class ObtenerFechaForm(forms.Form):
#     departamento = forms.ModelChoiceField(
#         queryset=Departamento.objects.all(),
#         label="Departamento",
#         required=False,
#         widget=SelectWidget(attrs={
#             'style': 'width: 100%; display: none;',
#         }
#         )
#     )
#     fecha = forms.DateField(
#         widget=MyCustomDateRangeWidget(
#             format='%d/%m/%Y',
#             picker_options={
#                 'showDropdowns': True,
#                 'format': 'DD/MM/YYYY',
#                 'singleDatePicker': True,
#                 'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
#                 'minDate': date.today().replace(day=1).strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
#             },
#         ),
#         input_formats=['%d/%m/%Y'],
#     )
#
#     class Meta:
#         fields = [
#             'fecha',
#             'departamento',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.departamento = kwargs['initial']['departamento'] if 'departamento' in kwargs['initial'] else None
#         self.fecha_fin = kwargs['initial']['fecha']
#         super(ObtenerFechaForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#
#         if self.departamento:
#             self.fields['departamento'].initial = self.departamento
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('fecha', css_class='form-group col-md-4 mb-0'),
#                 Field('departamento', type="hidden"),
#                 css_class='form-row'
#             ),
#         )
#
# # ------------ NormaOperativa / Form Filter ------------
# class NormaOperativaFormFilter(forms.Form):
#     class Meta:
#         model = NormaOperativa
#         fields = [
#             'fecha',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(NormaOperativaFormFilter, self).__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_no_form_filter'
#         self.helper.form_method = 'GET'
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     'Normas Operativas',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                     ),
#                     Row(
#                         Column('fecha', css_class='form-group col-md-4 mb-0'),
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
# class NormaOperativaProductoFormFilter(forms.Form):
#     class Meta:
#         model = NormaOperativaProducto
#         fields = [
#             'producto',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(NormaOperativaProductoFormFilter, self).__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_nop_form_filter'
#         self.helper.form_method = 'GET'
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     'Normas Operativas',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                     ),
#                     Row(
#                         Column('producto', css_class='form-group col-md-4 mb-0'),
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
# class NormaOperativaDetalleForm(forms.ModelForm):
#     class Meta:
#         model = NormaOperativaDetalle
#         fields = [
#             'producto',
#             'medida',
#             'norma',
#         ]
#         widgets = {
#             'producto': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%',
#                     'id': 'id_productodetalleno',
#                 }
#             ),
#             'medida': SelectWidget(
#                 attrs={
#                     'style': 'width: 100%; dislay: block',
#                     'id': 'id_medidadetalleno',
#                 },
#             ),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_normaoperativadetalle_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('producto', css_class='form-group col-md-8 mb-0', css_id='productodetalleno'),
#                 Column('medida', css_class='form-group col-md-4 mb-0', css_id='medidadetalleno'),
#                 css_class='form-row'
#             ),
#             Row(Column('norma', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'),
#         )
#
# class NormaOperativaDetalleDetailForm(NormaOperativaDetalleForm):
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_normaoperativadetall_detail_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#         self.helper.layout = Layout(
#             Row(
#                 Column(UneditableField('producto'), css_class='form-group col-md-8 mb-0', css_id='productodetalleno'),
#                 Column(UneditableField('medida'), css_class='form-group col-md-4 mb-0', css_id='medidadetalleno'),
#                 css_class='form-row'
#             ),
#             Row(Column(UneditableField('norma'), css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'),
#         )
#
# class DameFechaNOModalForm(forms.Form):
#     fecha = forms.DateField(
#         widget=MyCustomDateRangeWidget(
#             format='%d/%m/%Y',
#             picker_options={
#                 'showDropdowns': True,
#                 'format': 'DD/MM/YYYY',
#                 'singleDatePicker': True,
#                 'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
#                 'minDate': date.today().replace(day=1).strftime('%d/%m/%Y'),
#                 # TODO Fecha no puede ser mayor que la fecha actual
#             },
#         ),
#         input_formats=['%d/%m/%Y'],
#     )
#
#     class Meta:
#         fields = [
#             'fecha',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.fecha_fin = kwargs['initial']['fecha']
#         super(DameFechaNOModalForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('fecha', css_class='form-group col-md-4 mb-0'),
#                 css_class='form-row'
#             ),
#         )
#
# class DameDptoATransfForm(forms.Form):
#     iddocumento = forms.CharField(label='iddocumento', required=False, widget=forms.TextInput(attrs={'readonly': True}))
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
#     class Meta:
#         fields = [
#             'departamento',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         self.iddocumento = kwargs['initial']['iddocumento'] if kwargs.get('initial', None) and kwargs.get('initial').get('iddocumento') else None
#         super(DameDptoATransfForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'GET'
#         self.helper.form_tag = False
#         if self.iddocumento:
#             doc = Documento.objects.get(pk=self.iddocumento)
#             self.fields['departamento'].queryset = doc.departamento.relaciondepartamento.all()
#
#         self.helper.layout = Layout(
#             Row(
#                 Column('departamento', css_class='form-group col-md-8 mb-0'),
#                 Field('iddocumento', type="hidden"),
#                 css_class='form-row'
#             ),
#         )