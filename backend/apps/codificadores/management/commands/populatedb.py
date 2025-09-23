from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.core.management import call_command
from apps.configuracion.models import UserUeb, UnidadContable
from apps.codificadores.models import ProductoDepartamento, TipoProductoDepartamento, ProductoFlujo, \
    LineaSalida, Medida, MarcaSalida, TipoProducto, ActividadDepartamento, TipoActividadDepartamento
import os
from django.conf import settings
import json
from django.db import transaction
from apps.codificadores import ChoiceTiposProd
from django.contrib.auth import get_user_model

dicc_list_perm_group = {}
DICC_GROUP_PERMISSION = {
    (1, 2, 3, 4, 5):
        {
            'tipodocumento': ['view'],
            'tipoproducto': ['view'],
            'documento': ['view'],
            'cuenta': ['view'],
            'unidadcontable': ['view'],
            'cambioproducto': ['view'],
            'centrocosto': ['view'],
            'confcentroselementosotros': ['view'],
            'confcentroselementosotrosdetalle': ['view'],
            'confcentroselementosotrosdetallegrouped': ['view'],
            'departamento': ['view'],
            'lineasalida': ['view'],
            'marcasalida': ['view'],
            'medida': ['view'],
            'medidaconversion': ['view'],
            'motivoajuste': ['view'],
            'normaconsumo': ['view'],
            'normaconsumodetalle': ['view'],
            'normaconsumogrouped': ['view'],
            'normaoperativa': ['view'],
            'normaoperativaproducto': ['view'],
            'normaoperativadetalle': ['view'],
            'numeraciondocumentos': ['view'],
            'productoflujo': ['view'],
            'productscapasclapesadas': ['view'],
            'vitola': ['view'],
            'loggedinuser': ['view', 'change', 'delete', 'add'],
            'clasificadorcargos': ['view'],
            'fichacostofilas': ['view'],
            'configuracionesgen': ['view'],
            'fichacostoproducto': ['view'],
            'fichacostoproductofilas': ['view'],
            'fichacostoproductofiladesglosempmat': ['view'],
            'fichacostogrouped': ['view'],
            'costovarglobales': ['view'],
            'varglobalescosto': ['view'],
            'varglobalescostogrouped': ['view'],
            'fechaprocesamientocosto': ['view'],
        },
    (1, 5):
        {'userueb': ['view', 'change', 'delete', 'add'],
         'conexionbasedato': ['view', 'change', 'delete', 'add'],
         },
    (5,):
        {
            'tipodocumento': ['change'],
            'tipoproducto': ['change'],
            'cuenta': ['change'],
            'unidadcontable': ['change'],
            'cambioproducto': ['change', 'delete', 'add'],
            'centrocosto': ['view', 'change'],
            'confcentroselementosotros': ['change'],
            'confcentroselementosotrosdetalle': ['change'],
            'confcentroselementosotrosdetallegrouped': ['change'],
            'departamento': ['change', 'delete', 'add'],
            'lineasalida': ['change', 'delete', 'add'],
            'marcasalida': ['change', 'delete', 'add'],
            'medida': ['change'],
            'medidaconversion': ['change', 'delete', 'add'],
            'motivoajuste': ['change', 'delete', 'add'],
            'normaconsumo': ['change', 'delete', 'add'],
            'normaconsumodetalle': ['change', 'delete', 'add'],
            'normaconsumogrouped': ['change', 'delete', 'add'],
            'normaoperativa': ['change', 'delete', 'add'],
            'normaoperativaproducto': ['change', 'delete', 'add'],
            'normaoperativadetalle': ['change', 'delete', 'add'],
            'numeraciondocumentos': ['change', 'delete', 'add'],
            'productoflujo': ['change', 'delete', 'add'],
            'productscapasclapesadas': ['change', 'delete', 'add'],
            'vitola': ['change', 'delete', 'add'],
            'clasificadorcargos': ['change', 'delete', 'add'],
            'fichacostofilas': ['change', 'delete', 'add'],
            'configuracionesgen': ['change', 'delete', 'add'],
            'fichacostoproducto': ['change', 'delete', 'add'],
            'fichacostoproductofilas': ['change', 'delete', 'add'],
            'fichacostoproductofiladesglosempmat': ['change', 'delete', 'add'],
            'fichacostogrouped': ['change', 'delete', 'add'],
            'costovarglobales': ['change', 'delete', 'add'],
            'fechaprocesamientocosto': ['change', 'add'],
        },
    (2,): {
        'documento': ['change', 'delete', 'add'],
        'documentodetalle': ['change', 'delete', 'add', 'view'],
        'documentodetalleproductonc': ['change', 'delete', 'add', 'view'],
        'documentodetalleproductono': ['change', 'delete', 'add', 'view'],
    },
    (3,): {
            'varglobalescosto': ['change', 'delete', 'add', 'view'],
            'varglobalescostogrouped': ['change', 'delete', 'add', 'view'],
    },
}


class Command(BaseCommand):
    def departamento_poducto(self):
        print("PRODUCTOS DE SALIDA POR DEPARTAMENTOS")
        departamento_poducto = [
            ProductoDepartamento(pk=TipoProductoDepartamento.MATERIAPRIMA),
            ProductoDepartamento(pk=TipoProductoDepartamento.MANOJOS),
            ProductoDepartamento(pk=TipoProductoDepartamento.CAPASINCLASIFICAR),
            ProductoDepartamento(pk=TipoProductoDepartamento.CAPACLASIFICADA),
            ProductoDepartamento(pk=TipoProductoDepartamento.PESADA),
            ProductoDepartamento(pk=TipoProductoDepartamento.LINEASINTERMINAR),
            ProductoDepartamento(pk=TipoProductoDepartamento.LINEASALIDA),
            ProductoDepartamento(pk=TipoProductoDepartamento.VITOLA),
        ]
        try:
            ProductoDepartamento.objects.bulk_create(departamento_poducto)
        except Exception as e:
            print(f"ERROR al crear o actualizar producto departamento {e}")

    def departamento_actividad(self):
        print("ACTIVIDAD QUE SE REALIZA EN LOS DEPARTAMENTOS")
        departamento_actividad = [
            ActividadDepartamento(pk=TipoActividadDepartamento.PREPMATERIAPRIMA),
            ActividadDepartamento(pk=TipoActividadDepartamento.CLASIFICADODEHOJAS),
            ActividadDepartamento(pk=TipoActividadDepartamento.DESPACHO),
            ActividadDepartamento(pk=TipoActividadDepartamento.TORCIDO),
        ]
        try:
            ActividadDepartamento.objects.bulk_create(departamento_actividad)
        except Exception as e:
            print(f"ERROR al crear o actualizar actividad departamento {e}")

    def grupos(self):
        print("CREANDO GRUPOS")
        print("    Administrador")
        print("    Administrador Empresa")
        print("    Operador Flujo")
        print("    Operador Costo")
        print("    Consultor")
        groups = [
            Group(pk=1, name='Administrador'),
            Group(pk=2, name='Operador Flujo'),
            Group(pk=3, name='Operador Costo'),
            Group(pk=4, name='Consultor'),
            Group(pk=5, name='Administrador Empresa'),
        ]
        try:
            Group.objects.bulk_create(groups)
        except Exception as e:
            print("GRUPO YA EXISTEN")

    def group_user(self):
        print("CREANDO USUARIOS ")
        uebs_all = UnidadContable.objects.all()
        groups_all = Group.objects.all()
        print("CREANDO USUARIOS ADMINISTRADORES")
        try:
            users = [
                UserUeb(pk="000603fa-af2d-4713-b0e5-c2991a289f4b",
                        first_name="Administrador UEB-01",
                        last_name="",
                        username="admin01",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='01'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="003820bb-9dc1-4cbb-b8cf-93f28322c697",
                        first_name="Administrador UEB-02",
                        last_name="",
                        username="admin02",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='02'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="003dec56-d3ac-452d-a2be-9c07539be90f",
                        first_name="Administrador UEB-03",
                        last_name="",
                        username="admin03",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='03'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009bfd05-0357-4614-ba5b-c9876272a460",
                        first_name="Administrador UEB-04",
                        last_name="",
                        username="admin04",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='04'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009c9e8f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-05",
                        last_name="",
                        username="admin05",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='05'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009c9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-06",
                        last_name="",
                        username="admin06",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='06'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009d9e9f-4064-4214-a051-a1f78ea26b85",
                        first_name="Administrador UEB-07",
                        last_name="",
                        username="admin07",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='07'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="109d9e9f-4064-4214-a051-a1f78ea28b65",
                        first_name="Administrador UEB-08",
                        last_name="",
                        username="admin08",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='08'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="209d9e9f-4064-4214-a051-a1f99ea26b65",
                        first_name="Administrador UEB-09",
                        last_name="",
                        username="admin09",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='09'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="309d9e9f-4064-4214-a051-a1f78ea66b65",
                        first_name="Administrador UEB-10",
                        last_name="",
                        username="admin10",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='10'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="400d9e9f-4084-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-13",
                        last_name="",
                        username="admin13",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='13'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="409f9e9f-4064-4214-a051-a1f78ea26b66",
                        first_name="Administrador UEB-14",
                        last_name="",
                        username="admin14",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='14'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="409f9e9f-4094-4214-a051-a1f78ea26b66",
                        first_name="Administrador UEB-16",
                        last_name="",
                        username="admin16",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='16'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="889d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-22",
                        last_name="",
                        username="admin22",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='22'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="879d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-23",
                        last_name="",
                        username="admin23",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='23'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els=")
            ]
            UserUeb.objects.bulk_create(users)
            print(f'USUARIOS ueb {users}')
            user_emp = [
                UserUeb(pk="809d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador Empresa",
                        last_name="",
                        username="adminempresa",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='21'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els=")
            ]
            UserUeb.objects.bulk_create(user_emp)
            print(f'USUARIO EMPRESA {user_emp}')
            for user in users:
                user.groups.add(groups_all.get(pk=1))

            for user in user_emp:
                user.groups.add(groups_all.get(pk=5))

        except Exception as e:
            print("USUARIOS YA EXISTEN")

    def add_datos_group_permission(self):
        print("ASIGNANDO PERMISOS A LOS GRUPOS")
        try:
            keys_dicc = DICC_GROUP_PERMISSION.keys()
            list_permiss = []
            for k in keys_dicc:
                models = DICC_GROUP_PERMISSION[k].keys()
                list_keys_groups = list(k)
                list_permiss = []
                for m in models:
                    permiss = DICC_GROUP_PERMISSION[k][m]
                    for p in permiss:
                        list_permiss.append(p + '_' + m)
                dicc_list_perm_group[k] = list_permiss
        except Exception as e:
            print("PERMISOS A LOS GRUPOS YA EXISTEN")

    def permss_group(self):
        list_keys_groups = dicc_list_perm_group.keys()
        for k in list_keys_groups:
            list_permiss = dicc_list_perm_group[k]
            query_permiss = Permission.objects.filter(codename__in=list_permiss)
            for p in query_permiss:
                for g in k:
                    group = Group.objects.get(pk=g)
                    group.permissions.add(p)

    def add_marcas_salida(self, *args):
        print("ACTUALIZANDO MARCAS DE SALIDAS")
        json_file = os.path.join(settings.STATIC_ROOT, 'MarcasSalida.json')
        print(f"Desde el fichero {json_file}")
        try:
            with open(json_file, 'r') as file:
                datos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error al procesar fichero que contiene los datos de las Líneas de salida {json_file}")
            return

        data_array = datos['MARCAS DE SALIDA']
        cant_marcas_actualizadas = 0
        datos_marca = []
        for d in data_array:
            cant_marcas_actualizadas += 1
            nombre = d['Nombre']
            codigo = d['Codigo']

            print(f"Marca de Salida => {codigo} - {nombre}")
            objmarca = MarcaSalida(codigo=codigo,
                                   descripcion=nombre
                                   )
            datos_marca.append(objmarca)

        print(f"  Cantidad de Marcas de salida procesadas ==> {cant_marcas_actualizadas}")
        try:
            MarcaSalida.objects.bulk_create(datos_marca)
        except Exception as e:
            pass

    def add_lineas_salida(self, *args):
        print("ACTUALIZANDO LINEAS DE SALIDAS")
        json_file = os.path.join(settings.STATIC_ROOT, 'LineasSalida.json')
        print(f"Desde el fichero {json_file}")
        try:
            with open(json_file, 'r') as file:
                datos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error al procesar fichero que contiene los datos de las Líneas de salida {json_file}")
            return

        data_array = datos['LINEAS DE SALIDA']
        datos_prod = []
        datos_linea = []
        cant_lineas_actualizadas = 0
        tipoprodLS = TipoProducto.objects.get(pk=ChoiceTiposProd.LINEASALIDA)
        for d in data_array:
            nombre = d['Nombre']
            codigo = d['Codigo']
            codigo_marca = d['Marca']
            codigo_vitola = d['Vitola']
            umedida = d['UM']

            medida = Medida.objects.filter(clave=umedida)
            if not medida.exists():
                mensaj = f"UM {umedida} no existe"

            marcasalida = MarcaSalida.objects.filter(codigo=codigo_marca)
            if not marcasalida.exists():
                mensaj = f"Marca de Salida {codigo_marca} no existe"

            vitola = ProductoFlujo.objects.filter(codigo=codigo_vitola)
            if not vitola.exists():
                mensaj = f"Vitola {codigo_vitola} no existe"

            if medida.exists() and marcasalida.exists() and vitola.exists():
                cant_lineas_actualizadas += 1
                print(f"Linea de Salida => {codigo} - {nombre}")
                prod = ProductoFlujo(codigo=codigo, descripcion=nombre, medida=medida.first(),
                                     tipoproducto=tipoprodLS)
                datos_prod.append(prod)
                objlinea = LineaSalida(marcasalida=marcasalida.first(),
                                       producto = prod,
                                       vitola = vitola.first()
                                       )
                datos_linea.append(objlinea)

        print(f"  Cantidad de Líneas de salida procesadas ==> {cant_lineas_actualizadas}")
        try:
            ProductoFlujo.objects.bulk_create(datos_prod)
            LineaSalida.objects.bulk_create(datos_linea)
        except Exception as e:
            pass

    def create_super_user(self, *args):
        User = get_user_model()

        # Datos del superusuario
        username = "admin"
        email = "admin@example.com"
        password = "admin"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado con éxito."))
        else:
            self.stdout.write(self.style.WARNING(f"El superusuario '{username}' ya existe."))

    def handle(self, *args, **options):
        self.departamento_poducto()
        self.departamento_actividad()
        with transaction.atomic():
            self.grupos()
            self.group_user()
            self.add_datos_group_permission()
        self.create_super_user()
        self.permss_group()
        # self.add_marcas_salida()
        # self.add_lineas_salida()

