from django.urls import path

from . import views

app_name = 'exportar'
urlpatterns = [
    path('uc_exportar/', views.uc_exportar, name='uc_exportar'),
    path('um_exportar/', views.um_exportar, name='um_exportar'),
    path('umc_exportar/', views.umc_exportar, name='umc_exportar'),
    path('ms_exportar/', views.ms_exportar, name='ms_exportar'),
    path('ma_exportar/', views.ma_exportar, name='ma_exportar'),
    path('th_exportar/', views.th_exportar, name='th_exportar'),
    path('vc_exportar/', views.vc_exportar, name='vc_exportar'),
    path('cc_exportar/', views.cc_exportar, name='cc_exportar'),
    path('ccta_exportar/', views.ccta_exportar, name='ccta_exportar'),
    path('dpto_exportar/', views.dpto_exportar, name='dpto_exportar'),
    path('cprod_exportar/', views.cprod_exportar, name='cprod_exportar'),
    path('numdoc_exportar/', views.numdoc_exportar, name='numdoc_exportar'),
    path('tipodoc_exportar/', views.tipodoc_exportar, name='tipodoc_exportar'),
    path('tipoprod_exportar/', views.tipoprod_exportar, name='tipoprod_exportar'),
    path('clacargos_exportar/', views.clacargos_exportar, name='clacargos_exportar'),
    path('all_conf_exportar/', views.all_conf_exportar, name='all_conf_exportar'),
    path('filafichacosto_exportar/', views.filafichacosto_exportar, name='filafichacosto_exportar'),
    path('configuracionesgen_exportar/', views.configuracionesgen_exportar, name='configuracionesgen_exportar'),
]

