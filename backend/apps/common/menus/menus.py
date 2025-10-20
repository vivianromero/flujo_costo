MENU = [
        {
            "id": 'id_nav_link_dashboard',
            "name": "Dashboard",
            "icon_class": 'fa fa-tachometer-alt',
            "submenu": [
                {
                    "id": 'id_nav_link_cuadro_mando',
                    "name": "Balanced scorecard",
                    "icon_class": 'nav-icon fas fa-tools',
                    "url": "/dashboard",
                },
            ]
        },
        {
            "id": 'id_nav_link_configuracion',
            "name": "Configuración",
            "icon_class": 'fa fa-tools',
            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
            "submenu": [
                {
                    "id": 'id_nav_link_flujo',
                    "name": "Flujo",
                    "icon_class": 'fa fa-project-diagram',
                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                    "submenu": [
                        {
                            "id": 'id_nav_link_unidades_contables',
                            "name": "Unidades Contable",
                            "icon_class": 'fa fa-building',
                            "url": "/configuracion/flujo/unidadescontables",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_departamentos',
                            "name": "Departamentos",
                            "icon_class": 'fa fa-sitemap',
                            "url": "/configuracion/flujo/departamento",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_unidades_de_medida',
                            "name": "Unidades de Medida",
                            "icon_class": 'fa fa-balance-scale',
                            "url": "/configuracion/flujo/um",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_conversion_de_unidades',
                            "name": "Conversión de Medidas",
                            "icon_class": 'fa fa-exchange-alt',
                            "url": "/configuracion/flujo/conversionmed",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_tipodocumento_de_ajuste',
                            "name": "Tipos de Documento",
                            "icon_class": 'fa fa-file-alt',
                            "url": "/configuracion/flujo/tipodocumento",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_tipoproducto',
                            "name": "Tipos de Productos",
                            "icon_class": 'fa fa-tags',
                            "url": "/configuracion/flujo/tipoproducto",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_tipohabiitaciones',
                            "name": "Tipos de Habilitacones",
                            "icon_class": 'fa fa-door-open',
                            "url": "/configuracion/flujo/tiposhabilitacion",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_motivos_de_ajuste',
                            "name": "Motivos de Ajuste",
                            "icon_class": 'fa fa-pencil-alt',
                            "url": "/configuracion/flujo/motivoajuste",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_marcas_de_salida',
                            "name": "Marcas de Salida",
                            "icon_class": 'fa fa-sign-out-alt',
                            "url": "/configuracion/flujo/marcassalida",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                        {
                            "id": 'id_nav_link_productos',
                            "name": "Productos",
                            "icon_class": 'fa fa-boxes',
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                            "submenu": [
                                {
                                    "id": 'id_nav_link_productos_mp',
                                    "name": "Mat.Primas, Materiales, Habilitaciones y Subproductos",
                                    "icon_class": 'fa fa-box',
                                    "url": "/configuracion/flujo/productos",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                                {
                                    "id": 'id_nav_link_productos_vitola',
                                    "name": "Vitolas",
                                    "icon_class": 'fa-solid fa-smoking',
                                    "url": "/configuracion/flujo/vitolas",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                                {
                                    "id": 'id_nav_link_productos_cap_pes',
                                    "name": "Pesadas y Capas Clasificadas",
                                    "icon_class": 'fa fa-weight',
                                    "url": "/configuracion/flujo/capaspesadas",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                                {
                                    "id": 'id_nav_link_productos_ls',
                                    "name": "Líneas de Salida",
                                    "icon_class": 'fa fa-share-square',
                                    "url": "/configuracion/flujo/lineassalida",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                                {
                                    "id": 'id_nav_link_normasconsumo',
                                    "name": "Normas",
                                    "icon_class": 'fa fa-file-contract',
                                    "url": "/configuracion/flujo/normas",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                                {
                                    "id": 'id_nav_link_cambio_de_productos',
                                    "name": "Cambio de Productos",
                                    "icon_class": 'fa fa-retweet',
                                    "url": "/configuracion/flujo/cambioproducto",
                                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                                },
                            ]
                        },
                        {
                            "id": 'id_nav_link_usonumeraciodoc',
                            "name": "Numeración de los documentos",
                            "icon_class": 'fa fa-list-ol',
                            "url": "/configuracion/flujo/numeraciondoc",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                        },
                    ]
                },
                {
                    "id": 'id_nav_link_conf_costo',
                    "name": "Costo",
                    "icon_class": 'fa fa-chart-line',
                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                    "submenu": [
                        {
                            "id": 'id_nav_link_cuentas_contables',
                            "name": "Cuentas Contables",
                            "icon_class": 'fa fa-book',
                            "url": "/configuracion/costo/cuentascontables",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_centros_de_costo',
                            "name": "Centros de Costo",
                            "icon_class": 'fa fa-building',
                            "url": "/configuracion/costo/centros",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_elementos_centros_de_costo',
                            "name": "Centros de Costo y Elementos de Gasto",
                            "icon_class": 'fa fa-layer-group',
                            "url": "/configuracion/costo/centroselemntos",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_conf_var_globales_costo',
                            "name": "Variables Globales del Costo",
                            "icon_class": 'fa fa-sliders-h',
                            "url": "/configuracion/costo/varglobales",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_elementos_filas_ficha_costo',
                            "name": "Filas de la Ficha de Costo",
                            "icon_class": 'fa fa-table',
                            "url": "/configuracion/costo/filasficha",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_elementos_clasificador_de_cargo',
                            "name": "Clasificador de Cargos",
                            "icon_class": 'fa fa-user-tag',
                            "url": "/configuracion/costo/cargos",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                        {
                            "id": 'id_nav_link_elementos_fechainiciocosto',
                            "name": "Fechas de Inicio del Costo",
                            "icon_class": 'fa fa-calendar-alt',
                            "url": "/configuracion/costo/fechainicio",
                            "validators": ["apps.app_auth.usuarios.validators.is_adminoroperadorcosto"],
                        },
                    ]
                },
                {
                    "id": 'id_nav_link_config_gen',
                    "name": "Otras Configuraciones",
                    "icon_class": 'fa fa-cogs',
                    "url": "/configuracion/otrasconfig",
                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                },
                {
                    "id": 'id_nav_link_export_all_config',
                    "name": "Exportar todas las Configuraciones",
                    "icon_class": 'fa fa-upload',
                    "url": "/configuracion/exportartodas",
                    "validators": ["apps.app_auth.usuarios.validators.is_adminempresa"],
                },
                {
                    "id": 'id_nav_link_import_all_config',
                    "name": "Importar todas las Configuraciones",
                    "icon_class": 'fa fa-download',
                    "url": "/configuracion/importartodas",
                    "validators": ["apps.app_auth.usuarios.validators.is_adminoroperador"],
                },
            ]
        }
    ]