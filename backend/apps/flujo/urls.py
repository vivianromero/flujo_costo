from django.urls import path, include

from . import views, reportsview

documento_crud = views.DocumentoCRUD()
documento_detalle_producto_nc = views.DocumentoDetalleProductoNCHtmxCRUD()
documento_detalle_producto_no = views.DocumentoDetalleProductoNOHtmxCRUD()
documento_detalle_reproceso = views.DocumentoDetalleReprocesoHtmxCRUD()
no_crud = views.NormaOperativaCRUD()
noproducto_crud = views.NormaOperativaProductoCRUD()
nodetalle_crud = views.NormaOperativaDetalleHtmxCRUD()
app_name = 'flujo'

urlpatterns = [
    path('', include(documento_crud.get_urls())),
    path('', include(documento_detalle_producto_nc.get_urls())),
    path('', include(documento_detalle_producto_no.get_urls())),
    path('', include(documento_detalle_reproceso.get_urls())),
    path('', include(no_crud.get_urls())),
    path("", include(noproducto_crud.get_urls())),
    path("", include(nodetalle_crud.get_urls())),

    path('<uuid:pk>/confirm_doc/', views.confirmar_documento, name='flujo_documento_confirm'),
    path("creartransfprod_doc/", views.ObtenerDepartamentoDestinoModalFormView.as_view(), name='creartransfprod_doc'),
    path('<uuid:pk>/refused_doc/', views.rechazar_documento, name='flujo_documento_refused'),
    path("<uuid:pk>/inicializar_dep/", views.inicializar_departamento, name='codificadores_departamento_inicializar'),
    path("obtener_documento_versat/", views.ObtenerDocumentoVersatModalFormView.as_view(), name='obtener_documento_versat'),
    path('precioproducto/', views.precioproducto, name='precioproducto'),
    path('departamentosueb/', views.departamentosueb, name='departamentosueb'),
    path('productosdestino/', views.productosdestino, name='productosdestino'),
    path('estadodestino/', views.estadodestino, name='estadodestino'),
    path('obtener_fecha/', views.DameFechaModalFormView.as_view(), name='obtener_fecha'),
    path('obtener_fecha_procesamiento/', views.obtener_fecha_procesamiento, name='obtener_fecha_procesamiento'),
    path('obtener_fechacambioperiodo/', views.DameFechaCambioPeriodoModalFormView.as_view(), name='obtener_fechacambioperiodo'),
    path('report_flujo_existencia/', reportsview.ReportExistenciaModalFormView.as_view(), name='report_flujo_existencia'),
    path('report_flujo_movimiento/', reportsview.ReportMovimientoModalFormView.as_view(), name='report_flujo_movimiento'),
    path('report_flujo_ctrol_mov_mp/', reportsview.ReportMovimientoMPModalFormView.as_view(), name='report_flujo_ctrol_mov_mp'),
    path('report_flujo_ctrol_pesadas/', reportsview.ReportControlPesadasModalFormView.as_view(), name='report_flujo_ctrol_pesadas'),
    path('guardar_cantidad_norma_operativa/<uuid:pk>/', views.guardar_cantidad_norma_operativa, name='guardar_cantidad_norma_operativa'),
    path("obtener_no", views.DameFechaNOModalFormView.as_view(), name='obtener_no'),
]
