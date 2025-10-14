from apps.costo.models import FechaProcesamientoCosto
def dame_fecha_costo(ueb):
    fechas = FechaProcesamientoCosto.objects_cache.get_cached_data()
    mes = None
    anno = None
    if fechas and ueb in fechas.keys():
        mes = fechas[ueb]['mes']
        anno = fechas[ueb]['anno']
    return mes, anno