from django.urls import path, include

from . import views, reportsview

fichacostoproducto_crud = views.FichaCostoCRUD()
fichacostogrouped_crud = views.FichaCostoGroupedCRUD()
varglobalescostodatos_crud = views.VarGlobalesCostoDatosCRUD()
fechainiciocosto_crud = views.FechaProcesamientoCostoCRUD()
fichacostoproductofilacapas_crud = views.FichaCostoProductoFilaCapasHtmxCRUD()
fichacostoproductofiladesglosempmat = views.FichaCostoProductoFilaDesgloseMPMatHtmxCRUD()
fichacostoproductodiladesglosesalario = views.FichaCostoProductoFilaDesgloseSalarioHtmxCRUD()
app_name = 'costo'

urlpatterns = [
    path("", include(fichacostoproducto_crud.get_urls())),
    path("", include(fichacostogrouped_crud.get_urls())),
    path("", include(varglobalescostodatos_crud.get_urls())),
    path("", include(fechainiciocosto_crud.get_urls())),
    path("", include(fichacostoproductofiladesglosempmat.get_urls())),
    path("", include(fichacostoproductofilacapas_crud.get_urls())),
    path("", include(fichacostoproductodiladesglosesalario.get_urls())),
    path("<uuid:pk>/confirm_fc/", views.confirm_fc, name='costo_fichacostoproducto_confirm'),
    path("<uuid:pk>/activar_fc/", views.activar_fc, name='costo_fichacostoproducto_activar'),
    path('productotipoficha/', views.productotipoficha, name='productotipoficha'),
    path(
        "obtener_fichacostoproductofilas_datos",
        views.FichaCostoProductoFilasModalFormView.as_view(),
        name='obtener_fichacostoproductofilas_datos'
    ),
    path('report_costo_existencia/', reportsview.ReportExistenciaModalFormView.as_view(), name='report_costo_existencia'),
]
