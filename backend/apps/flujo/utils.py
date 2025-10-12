from django.db.models import Case, When, Sum, Max, \
    Func, CharField, ExpressionWrapper
from django.db.models.functions import Concat, Cast

from apps.codificadores import ChoiceClasesMatPrima, ChoiceTiposProd, ChoiceTiposDoc
from apps.codificadores.models import TipoProductoDepartamento, ClaseMateriaPrima, NumeracionDocumentos
from .models import *


def ids_documentos_versat_procesados(fecha_inicio, fecha_fin, departamento, ueb):
    # id de los documentos que se han introducido al sistema durante el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    dicc = {'fecha_documentoversat__gte': fecha_inicio,
            'fecha_documentoversat__lte': fecha_fin,
            'documento__ueb': ueb}
    if departamento:
        dicc.update({'documento__departamento': departamento})

    query_doc_acept = DocumentoOrigenVersat.objects.filter(**dicc).values(iddocversat=F('documentoversat')).all()

    # id de los documentos que se han rechazado en el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    query_doc_rechaz = DocumentoVersatRechazado.objects.filter(
        fecha_documentoversat__gte=fecha_inicio,
        fecha_documentoversat__lte=fecha_fin,
        ueb=ueb).values(iddocversat=F('documentoversat')).all()

    docs = query_doc_acept.union(query_doc_rechaz)
    ids = [i['iddocversat'] for i in docs]
    return ids

#actualiza la existencia de los productos en los documentos en edición
@transaction.atomic
def actualiza_existencias_documentos(doc, producto, estado, existencia_anterior):
    numeroconsecutivo = doc.numeroconsecutivo if doc else 1
    existencia_actual = Decimal(existencia_anterior)
    hay_error = False

    # Definición de modelos y campos
    modelos = [
        {
            'model': DocumentoDetalle,
            'cantidad_field': 'cantidad',
            'producto_field': 'producto',
            'documento_field': 'documento'
        },
        {
            'model': DocumentoDetalleEstado,
            'cantidad_field': 'cantidad',
            'producto_field': 'producto',
            'documento_field': 'documentodetalle__documento'
        },
        {
            'model': DocumentoDetalleProducto,
            'cantidad_field': 'cantidad',
            'producto_field': 'producto',
            'documento_field': 'documentodetalle__documento'
        },
        {
            'model': DocumentoDetalleProductoNC,
            'cantidad_field': 'cantidad',
            'producto_field': 'normaconsumodetalles__producto',
            'documento_field': 'documentodetalle__documento'
        },
        {
            'model': DocumentoDetalleProductoNO,
            'cantidad_field': 'cantidad_usada',
            'producto_field': 'normaoperativadetalle__producto',
            'documento_field': 'documentodetalle__documento'
        },
        {
            'model': DocumentoDetalleReproceso,
            'cantidad_field': 'cantidad',
            'producto_field': 'producto',
            'documento_field': 'documentodetalle__documento'
        },
        {
            'model': DocumentoDetalleReprocesoDeficiente,
            'cantidad_field': 'cantidad',
            'producto_field': 'producto',
            'documento_field': 'documentodetalle__documento'
        },
    ]

    # Primero recolectamos todos los objetos a procesar
    objetos_a_procesar = []

    for config in modelos:
        # Filtros comunes
        filtro = Q(**{
            f"{config['documento_field']}__numeroconsecutivo__gt": numeroconsecutivo,
            config['producto_field']: producto,
            'estado': estado
        })

        # Obtenemos los objetos con select_for_update
        queryset = config['model'].objects.filter(filtro).select_for_update()

        # Anotamos con el numeroconsecutivo para ordenar después
        if 'documentodetalle__documento' in config['documento_field']:
            queryset = queryset.annotate(
                consecutivo=F('documentodetalle__documento__numeroconsecutivo')
            )
        else:
            queryset = queryset.annotate(
                consecutivo=F('documento__numeroconsecutivo')
            )

        # Agregamos a la lista con toda la información necesaria
        for obj in queryset:
            objetos_a_procesar.append({
                'obj': obj,
                'consecutivo': obj.consecutivo,
                'cantidad_field': config['cantidad_field'],
                'documento_field': config['documento_field']
            })

    # Ordenamos todos los objetos por consecutivo
    objetos_a_procesar.sort(key=lambda x: x['consecutivo'])

    # Procesamos en orden
    for item in objetos_a_procesar:
        obj = item['obj']
        cantidad = getattr(obj, item['cantidad_field']) or Decimal('0.0')
        operacion = getattr(obj, 'operacion', 1)
        existencia_actual += cantidad * operacion
        obj.existencia = existencia_actual

        # Verificación de existencia negativa
        error = existencia_actual < 0
        hay_error = hay_error or error
        obj.error = error

        # Guardamos el objeto
        obj.save(update_fields=['existencia', 'error'])

        # Obtenemos el documento relacionado
        if 'documentodetalle__documento' in item['documento_field']:
            documento = obj.documentodetalle.documento
        else:
            documento = obj.documento

        # Actualizamos el documento
        documento.estado = EstadosDocumentos.ERRORES if hay_error else EstadosDocumentos.EDICION
        documento.error = hay_error
        documento.save(update_fields=['estado', 'error'])

@transaction.atomic
def genera_numero_doc(departamento, ueb, tipodoc, consecutivo_conf, control_conf, rep_prod=None):

    tipo_doc = TipoDocumento.objects.get_cached_data()
    tipodoc = tipo_doc[int(tipodoc)]
    prefijo = tipodoc.get('prefijo')

    numeros_consec_control = [(), ()]

    numeros_consec_control[0] = (1, consecutivo_conf['sistema'], '', consecutivo_conf)
    numeros_consec_control[1] = (1, control_conf['sistema'], prefijo, control_conf)

    numeros = NumeroDocumentos.objects.select_for_update().filter(ueb=ueb)

    if numeros:
        numeros_consec_control[0] = dame_numero(numeros, consecutivo_conf, departamento,
                                                TipoNumeroDoc.NUMERO_CONSECUTIVO, '')
        numeros_consec_control[1] = dame_numero(numeros, control_conf, departamento, TipoNumeroDoc.NUMERO_CONTROL,
                                                prefijo)

    if tipodoc.get('generado') or rep_prod:  # si el doc es generado se actualiza los numeros para evitar sea tomado por otro proceso
        actualiza_nros = [
            NumeroDocumentos(ueb=ueb, numero=numeros_consec_control[0][0], tiponumero=TipoNumeroDoc.NUMERO_CONSECUTIVO,
                             departamento=departamento),
            NumeroDocumentos(ueb=ueb, numero=numeros_consec_control[1][0], tiponumero=TipoNumeroDoc.NUMERO_CONTROL,
                             departamento=departamento)
        ]
        NumeroDocumentos.objects.bulk_update_or_create(actualiza_nros,
                                                       ['ueb', 'numero', 'tiponumero',
                                                        'departamento'],
                                                       match_field=['ueb', 'departamento', 'tiponumero'])

    return numeros_consec_control


def dame_numero(numeros, conf, departamento, tiponumero, prefijo):
    dicc_filter = {'tiponumero': tiponumero}
    if conf['departamento']:
        dicc_filter['departamento'] = departamento
    numeros_ = numeros.filter(**dicc_filter)
    if numeros_.exists():
        return (numeros_[0].numero + 1, conf['sistema'], '' if not prefijo else prefijo, conf)
    return (1, conf['sistema'], prefijo, conf)


@transaction.atomic
def actualiza_numeros(ueb, departamento, consecutivo, control, pk):
    dicc_filter_consec = {'tiponumero': TipoNumeroDoc.NUMERO_CONSECUTIVO}
    dicc_filter_control = {'tiponumero': TipoNumeroDoc.NUMERO_CONTROL}

    confnumero = NumeracionDocumentos.objects_cache.get_cached_data()
    consecutivo_conf = confnumero[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    control_conf = confnumero[TipoNumeroDoc.NUMERO_CONTROL]

    departamento_consec = None
    departamento_control = None

    docs_consec = None
    docs_control = None

    dicc_filter = {'ueb': ueb}

    fecha_procesamiento = dame_fecha(ueb, departamento)
    if fecha_procesamiento:
        dicc_filter.update({'fecha': fecha_procesamiento})

    if consecutivo_conf['departamento']:
        dicc_filter.update({'departamento': departamento})
        dicc_filter_consec.update({'departamento': departamento})

    docs_consec = Documento.objects.select_for_update().filter(**dicc_filter).exclude(pk=pk)

    if not docs_consec and pk == None:  # cuando es eliminar
        NumeroDocumentos.objects.select_for_update().filter(**dicc_filter_consec).delete()
        NumeroDocumentos.objects.select_for_update().filter(**dicc_filter_control).delete()
        return

    if control_conf['departamento']:
        dicc_filter.update({'departamento': departamento})
        dicc_filter_control.update({'departamento': departamento})

    docs_control = Documento.objects.select_for_update().filter(**dicc_filter).exclude(pk=pk)

    max_consec = docs_consec.aggregate(numeromax=Max('numeroconsecutivo', default=0))['numeromax']

    if consecutivo and consecutivo > max_consec:
        max_consec = consecutivo

    max_control = 0 if not pk else control

    for p in docs_control:
        ncontrol = p.get_numerocontrol()
        max_control = ncontrol if ncontrol > max_control else max_control

    actualiza_nros = [NumeroDocumentos(ueb=ueb, numero=max_consec, tiponumero=TipoNumeroDoc.NUMERO_CONSECUTIVO,
                                       departamento=departamento),
                      NumeroDocumentos(ueb=ueb, numero=max_control, tiponumero=TipoNumeroDoc.NUMERO_CONTROL,
                                       departamento=departamento)
                      ]
    NumeroDocumentos.objects.bulk_update_or_create(actualiza_nros,
                                                   ['ueb', 'numero', 'tiponumero',
                                                    'departamento'],
                                                   match_field=['ueb', 'departamento', 'tiponumero'])

    return


@transaction.atomic
def renumerar_documentos(ueb, departamento, consecutivo, control):
    dicc_filter = {'estado__in': [EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES], 'ueb': ueb}
    confnumero = NumeracionDocumentos.objects_cache.get_cached_data()
    consecutivo_conf = confnumero[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    control_conf = confnumero[TipoNumeroDoc.NUMERO_CONTROL]
    doc_cont = None
    doc_consec = None
    valor_act_cons = 1
    if consecutivo_conf['sistema']:
        valor_act_cons = 1000000
        dicc_filter.update({'numeroconsecutivo__gt': consecutivo})
        if consecutivo_conf['departamento']:
            dicc_filter.update({'departamento': departamento})

        Documento.objects.filter(**dicc_filter) \
            .update(numeroconsecutivo=F('numeroconsecutivo') * valor_act_cons)

        doc_consec = Documento.objects.annotate(old_numeroconsecutivo=F('numeroconsecutivo')/1000000).\
            filter(**dicc_filter).order_by('numeroconsecutivo')

    if control_conf['sistema']:
        dicc_filter = {}
        dicc_filter.update({'numeroconsecutivo__gt': consecutivo})
        if control_conf['departamento']:
            dicc_filter.update({'departamento': departamento})
        doc_cont = Documento.objects.annotate(
                    prefijo=Coalesce(Case(
                        When(numerocontrol__contains='/', then=Concat(
                            Func(
                                F('numerocontrol'),
                                function='split_part',
                                template="split_part(%(expressions)s, '/', 1)",
                                output_field=CharField()
                            ),
                            Value('/')
                        )),
                        default=Value(''),
                        output_field=CharField()
                    ), Value(''))
                ).filter(**dicc_filter)\

    if doc_cont:

        doc_cont.order_by('numeroconsecutivo').update(
                numerocontrol=Concat(
                    Coalesce(F('prefijo'), Value('')),
                    Cast((F('numeroconsecutivo')/valor_act_cons) - 1, output_field=CharField())
                )
            )

    if doc_consec:

        doc_consec.order_by('numeroconsecutivo').update(numeroconsecutivo=F('old_numeroconsecutivo') - 1)

    return


def dame_productos(documentopadre, queryproductos):
    departamento = documentopadre.departamento
    tipoproducto = []
    claseproducto = []
    productos = departamento.departamentoproductoentrada.all()
    if (documentopadre.tipodocumento.id in [ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO,
                                                ChoiceTiposDoc.RECEPCION_PRODUCCION,
                                                ChoiceTiposDoc.RECEPCION_RECHAZO]):
        productos = departamento.departamentoproductosalida.all()
    claseproducto, tipoproducto = productos_clase_tipo(productos)

    query = queryproductos.filter(Q(tipoproducto__in=tipoproducto) |
                          Q(productoflujoclase_producto__clasemateriaprima__in=claseproducto))

    #TODO esto va para validar en el reproceso que existan con estado deficiente
    # if documentopadre.tipodocumento.id == ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO:
    #     productos_defic = ExistenciaDpto.objects.filter(departamento=departamento, estado=EstadoProducto.DEFICIENTE,
    #                                   cantidad_final__gt=0, ueb=documentopadre.ueb,
    #                                   producto__tipoproducto__in=tipoproducto)
    #     ids = [p.id for p in productos_defic]
    #     query = query.filter(pk__in=ids)
    return query

def dame_productos_departamento(departamento, operacion):
    tipoproducto = []
    claseproducto = []
    if operacion == OperacionDocumento.ENTRADA:
        productos = departamento.departamentoproductoentrada.all()
    else:
        productos = departamento.departamentoproductosalida.all()

    claseproducto, tipoproducto = productos_clase_tipo(productos)

    return claseproducto, tipoproducto

def productos_clase_tipo(productos):
    claseproducto = []
    tipoproducto = []
    for p in productos:
        match p.pk:
            case TipoProductoDepartamento.MATERIAPRIMA:
                claseproducto = [x.pk for x in ClaseMateriaPrima.objects.filter(capote_fortaleza__in=['C', 'F', 'P'])]
            case TipoProductoDepartamento.CAPASINCLASIFICAR:
                claseproducto.append(ChoiceClasesMatPrima.CAPASINCLASIFICAR)
            case TipoProductoDepartamento.CAPACLASIFICADA:
                claseproducto.append(ChoiceClasesMatPrima.CAPACLASIFICADA)
            case TipoProductoDepartamento.PESADA:
                tipoproducto.append(ChoiceTiposProd.PESADA)
            case TipoProductoDepartamento.LINEASINTERMINAR:
                tipoproducto.append(ChoiceTiposProd.LINEASINTERMINAR)
            case TipoProductoDepartamento.LINEASALIDA:
                tipoproducto.append(ChoiceTiposProd.LINEASALIDA)
            case TipoProductoDepartamento.VITOLA:
                tipoproducto.append(ChoiceTiposProd.VITOLA)
    return claseproducto, tipoproducto

#Existencia de un producto, incluyendo los documentos en edicion
@transaction.atomic
def existencia_producto(doc, producto, estado, cantidad, operacion):

    departamento = doc.departamento
    ueb = doc.ueb
    consecutivo = doc.numeroconsecutivo
    cantidad = Decimal('0.00') if not cantidad else cantidad

    documentos_anteriores_edicion = Documento.objects.filter(
        departamento=departamento,
        ueb=ueb,
        estado=EstadosDocumentos.EDICION,
        numeroconsecutivo__lt=consecutivo
    ).only('id')

    documentos_anteriores_error = documentos_anteriores_edicion.filter(estado=EstadosDocumentos.ERRORES)

    hay_error = documentos_anteriores_error.exists()

    total_anterior = Decimal('0.0')

    modelos = [
        (DocumentoDetalle, 'cantidad', 'producto'),
        (DocumentoDetalleEstado, 'cantidad', 'producto'),
        (DocumentoDetalleProducto, 'cantidad', 'producto'),
        (DocumentoDetalleReproceso, 'cantidad', 'producto'),
        (DocumentoDetalleReprocesoDeficiente, 'cantidad', 'producto'),
        (DocumentoDetalleProductoNC, 'cantidad', 'normaconsumodetalles__producto'),
        (DocumentoDetalleProductoNO, 'cantidad_usada', 'normaoperativadetalle__producto'),
    ]

    for modelo, campo_cantidad, campo_producto in modelos:
        # Filtro por documento y producto (según ruta específica)
        if modelo == DocumentoDetalle:
            filtro = Q(documento__in=documentos_anteriores_edicion)
            select_related = 'documento'
        else:
            filtro = Q(documentodetalle__documento__in=documentos_anteriores_edicion)
            select_related = 'documentodetalle__documento'

        filtro &= Q(**{campo_producto: producto, 'estado': estado})

        # Bloqueo de fila con select_for_update()
        queryset = (
            modelo.objects
                .filter(filtro)
                .select_for_update()
                .select_related(select_related)
                .only(campo_cantidad, 'operacion')
        )

        expr = ExpressionWrapper(
            F(campo_cantidad) * F('operacion'),
            output_field=DecimalField(max_digits=20, decimal_places=6)
        )

        suma = (
                queryset
                .annotate(resultado=expr)
                .aggregate(total=Sum('resultado'))['total'] or Decimal('0.0')
        )

        total_anterior += suma

    existencia = ExistenciaDpto.objects.select_for_update().filter(departamento=departamento, estado=estado,
                                                                   producto=producto, ueb=ueb).first()
    cantidad_existencia = 0 if not existencia else existencia.cantidad_final

    existencia_product = Decimal(cantidad_existencia) + Decimal(cantidad) * operacion + Decimal(total_anterior)

    return existencia_product, hay_error or existencia_product<0

def dame_fecha(ueb, departamento, key=ChoiceFechas.PROCESAMIENTO):
    fechas = FechaPeriodo.objects.get_cached_data()
    fecha = ''
    if fechas and ueb in fechas.keys() and departamento in fechas[ueb].keys():
        fecha = fechas[ueb][departamento][key]
    return fecha

@transaction.atomic
def dame_precio_salida(producto, estado, doc):
    # documentos anteriores que son entradas y no están confirmados
    dicc = {'documento__estado': EstadosDocumentos.EDICION,
            'documento__departamento': doc.departamento, 'documento__ueb': doc.ueb,
            'documento__tipodocumento__operacion': OperacionDocumento.ENTRADA,
            'documento__numeroconsecutivo__lt': doc.numeroconsecutivo,
            'producto': producto,
            'estado': estado}

    anteriores = DocumentoDetalle.objects.select_for_update().filter(**dicc). \
        aggregate(cantidad_ant=Coalesce(Sum('cantidad'), Value(0.0), output_field=DecimalField()),
                  importe_ant=Coalesce(Sum(F('precio') * F('cantidad')), Value(0.0), output_field=DecimalField())
                  )
    cantidad_anterior = anteriores['cantidad_ant']
    importe_anterior = anteriores['importe_ant']

    dicc = {'departamento': doc.departamento, 'ueb': doc.ueb,
            'producto': producto,
            'estado': estado,
            'anno': doc.fecha.year,
            'mes': doc.fecha.month}

    existencias = ExistenciaDpto.objects.select_for_update().filter(**dicc)
    cantidad_existencia = Decimal('0.00')
    importe_existencia = Decimal('0.00')

    if existencias.exists():
        existe = existencias.first()
        cantidad_existencia = existe.cantidad_final
        importe_existencia = round(existe.cantidad_final * existe.precio, 2)

    cantidad_total = cantidad_existencia + cantidad_anterior
    importe_total = importe_existencia + importe_anterior

    precio = importe_total / cantidad_total if cantidad_total > 0 else 0.00
    return round(precio, 7)