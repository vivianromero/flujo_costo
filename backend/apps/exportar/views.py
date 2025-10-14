# views.py
import json
from io import StringIO


from django.core import serializers
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect

from apps.codificadores.models import UnidadContable, Medida, MedidaConversion, MarcaSalida, CentroCosto, Cuenta, \
    Departamento, CambioProducto, NumeracionDocumentos, MotivoAjuste, NormaConsumo, ClasificadorCargos, FichaCostoFilas, \
    ConfiguracionesGen, TipoDocumento, TipoProducto, CostoVarGlobales, TipoHabilitacion

from apps.utiles.decorators import adminempresa_required

from .utils import crear_export_datos, crear_export_file


@adminempresa_required
def uc_exportar(request):
    return crear_export_datos(request, 'UC', UnidadContable)


@adminempresa_required
def um_exportar(request):
    return crear_export_datos(request, 'UM', Medida)


@adminempresa_required
def umc_exportar(request):
    return crear_export_datos(request, 'UMC', MedidaConversion)


@adminempresa_required
def ms_exportar(request):
    return crear_export_datos(request, 'MS', MarcaSalida)

@adminempresa_required
def ma_exportar(request):
    return crear_export_datos(request, 'MotAjus', MotivoAjuste)

@adminempresa_required
def vc_exportar(request):
    return crear_export_datos(request, 'VarGlobCosto', CostoVarGlobales)

@adminempresa_required
def cc_exportar(request):
    return crear_export_datos(request, 'CC', CentroCosto)


@adminempresa_required
def ccta_exportar(request):
    return crear_export_datos(request, 'CCTA', Cuenta)


@adminempresa_required
def dpto_exportar(request):
    return crear_export_datos(request, 'DPTO', Departamento)


@adminempresa_required
def cprod_exportar(request):
    return crear_export_datos(request, 'CambioPROD', CambioProducto)


@adminempresa_required
def numdoc_exportar(request):
    return crear_export_datos(request, 'NumDoc', NumeracionDocumentos)

@adminempresa_required
def tipodoc_exportar(request):
    return crear_export_datos(request, 'TipoDoc', TipoDocumento)

@adminempresa_required
def tipoprod_exportar(request):
    return crear_export_datos(request, 'TipoProd', TipoProducto)

@adminempresa_required
def clacargos_exportar(request):
    return crear_export_datos(request, 'CLA_CARG', ClasificadorCargos)

@adminempresa_required
def th_exportar(request):
    return crear_export_datos(request, 'TipoHab', TipoHabilitacion)

@adminempresa_required
def all_conf_exportar(request):
    if not valida_datos_exportar(request):
        return redirect('app_index:index')

    try:
        output_codificadores = StringIO()

        call_command(
            'dumpdata',
            'codificadores',
            exclude=['codificadores.FechaInicio'],
            indent=2,
            stdout=output_codificadores
        )

        datos = json.loads(output_codificadores.getvalue())

        objetos_costo = FechaProcesamientoCosto.objects.filter(inicial=True)
        datos_costo = json.loads(serializers.serialize('json', objetos_costo, indent=2))

        datos_completos = datos + datos_costo

        datos_json = json.dumps(datos_completos, ensure_ascii=False)
        return crear_export_file(request, datos_json, 'ALL_CONF', None)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@adminempresa_required
def filafichacosto_exportar(request):
    return crear_export_datos(request, 'FILAS_FICHA', FichaCostoFilas)

@adminempresa_required
def configuracionesgen_exportar(request):
    return crear_export_datos(request, 'CONFIG_GEN', ConfiguracionesGen)





