import base64
import json

import sweetify
from django.conf import settings
from django.db.models import Q, Max
from django.utils.translation import gettext_lazy as _

from apps.codificadores.models import FichaCostoFilas

KEY_ENCRIP = "DATAZUCAR-ETTVC-SISGESFC"

YES_NO = (
    (1, "Si"),
    (0, "No"),
)

EMPTY_LABEL = '-- Todos --'
EMPTY_LABEL_F = '-- Todas --'

def codificar(clear):
    enc = []
    key = KEY_ENCRIP
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)

    return base64.urlsafe_b64encode((''.join(enc)).encode("utf-8", "replace")).decode()


def decodificar(enc):
    dec = []
    enc = (base64.urlsafe_b64decode(enc)).decode("utf-8", "replace")
    key = KEY_ENCRIP
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)

    return ''.join(dec)


def obtener_version():
    app_version_file = open(settings.APP_VERSION, 'r')
    valor = app_version_file.read()

    return decodificar(valor)


def obtener_numero_fila(pk_padre):
    if pk_padre:
        # Obtener el padre directamente
        padre = FichaCostoFilas.objects.get(pk=pk_padre)

        # Obtener el máximo número de fila entre los hijos
        ultima_fila = padre.children.aggregate(ultima=Max('fila'))['ultima']

        # Calcular el nuevo número de fila
        siguiente_numero = int(ultima_fila.split('.')[-1]) + 1 if ultima_fila else 1
        return f"{padre.fila}.{siguiente_numero}"

    # Caso sin padre: obtener la última fila de nivel superior
    ultima_fila = FichaCostoFilas.objects.filter(
        ~Q(fila__contains='.'),
        encabezado=True
    ).aggregate(ultima=Max('fila'))['ultima']

    # Calcular el nuevo número de fila de nivel superior
    return str(int(ultima_fila) + 1) if ultima_fila else '1'


def message_error(request, title, text):
    sweetify.error(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )


def message_success(request, title, text):
    sweetify.success(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )


def message_warning(request, title, text):
    sweetify.warning(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )

def paginate_queryset(qs, page, limit):
    total = qs.count()
    offset = (page - 1) * limit
    return qs[offset:offset + limit], total

# def json_response(message=None, success=True, **data):
#     """
#     Args:
#         message:
#         success:
#         **data:
#     """
#     if not message:
#         json_object = {'success': success}
#     else:
#         json_object = {'success': success, 'message': message}
#
#     json_object.update(data)
#     return json.dumps(json_object)


# def dame_fechas_inicio_procesamiento(ueb, departamento):
#     fecha_procesamiento = None
#     fecha_inicio = None
#     fechas_procesamiento_actual = FechaPeriodo.objects.get_cached_data()
#     if fechas_procesamiento_actual and ueb in fechas_procesamiento_actual.keys() and departamento in \
#             fechas_procesamiento_actual[ueb].keys():
#         fecha_procesamiento = fechas_procesamiento_actual[ueb][departamento]['fecha_procesamiento']
#         fecha_inicio = fechas_procesamiento_actual[ueb][departamento]['fecha_inicio']
#
#     return (fecha_procesamiento, fecha_inicio)

# #TODO ver si se va a usar
# def crear_superusuario(credentials):
#
#     user, created = User.objects.get_or_create(
#         username = credentials["username"],
#         email=credentials["email"],
#         defaults={"is_active": True, "is_staff": True, "is_superuser": True},
#     )
#     if created:
#         user.set_password(credentials["password"])
#         user.save()
#         msg = "Superusuario - %(email)s creado satisfactoriamente " % credentials
#     else:
#         msg = "Superusuario - %(email)s ya existe " % credentials
#     return msg


