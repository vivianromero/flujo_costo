MENU = [
  {
    "id": "id_nav_link_configuracion",
    "name": "Configuración",
    "icon_class": "fa fa-tools",
    "submenu": [
      {
        "id": "id_nav_link_flujo",
        "name": "🧭 Flujo Operativo",
        "icon_class": "fa fa-project-diagram",
        "submenu": [
          {
            "id": "id_nav_link_unidades_contables",
            "name": "Unidades Contables",
            "icon_class": "fa fa-building",
            "url": "flujo/uc"
          },
          {
            "id": "id_nav_link_departamentos",
            "name": "Departamentos",
            "icon_class": "fa fa-sitemap",
            "url": "flujo/departamento"
          },
          {
            "id": "id_nav_link_unidades_de_medida",
            "name": "Unidades de Medida",
            "icon_class": "fa fa-balance-scale",
            "url": "flujo/um"
          },
          {
            "id": "id_nav_link_conversion_de_unidades",
            "name": "Conversión de Medidas",
            "icon_class": "fa fa-exchange-alt",
            "url": "flujo/conversionmed"
          },
          {
            "id": "id_nav_link_tipodocumento_de_ajuste",
            "name": "Tipos de Documento",
            "icon_class": "fa fa-file-alt",
            "url": "flujo/tipodocumento"
          },
          {
            "id": "id_nav_link_tipoproducto",
            "name": "Tipos de Productos",
            "icon_class": "fa fa-tags",
            "url": "flujo/tipoproducto"
          },
          {
            "id": "id_nav_link_tipohabiitaciones",
            "name": "Tipos de Habilitaciones",
            "icon_class": "fa fa-door-open",
            "url": "flujo/tiposhabilitacion"
          },
          {
            "id": "id_nav_link_motivos_de_ajuste",
            "name": "Motivos de Ajuste",
            "icon_class": "fa fa-pencil-alt",
            "url": "flujo/motivoajuste"
          },
          {
            "id": "id_nav_link_marcas_de_salida",
            "name": "Marcas de Salida",
            "icon_class": "fa fa-sign-out-alt",
            "url": "flujo/marcassalida"
          },
          {
            "id": "id_nav_link_productos",
            "name": "Productos",
            "icon_class": "fa fa-boxes",
            "submenu": [
              {
                "id": "id_nav_link_productos_mp",
                "name": "Mat. Primas y Subproductos",
                "icon_class": "fa fa-box",
                "url": "flujo/productos"
              },
              {
                "id": "id_nav_link_productos_vitola",
                "name": "Vitolas",
                "icon_class": "fa fa-certificate",
                "url": "flujo/vitolas"
              },
              {
                "id": "id_nav_link_productos_cap_pes",
                "name": "Pesadas y Capas Clasificadas",
                "icon_class": "fa fa-weight",
                "url": "flujo/capaspesadas"
              },
              {
                "id": "id_nav_link_productos_ls",
                "name": "Líneas de Salida",
                "icon_class": "fa fa-share-square",
                "url": "flujo/lineassalida"
              },
              {
                "id": "id_nav_link_normasconsumo",
                "name": "Normas",
                "icon_class": "fa fa-file-contract",
                "url": "flujo/normas"
              },
              {
                "id": "id_nav_link_cambio_de_productos",
                "name": "Cambio de Productos",
                "icon_class": "fa fa-retweet",
                "url": "flujo/cambioproducto"
              }
            ]
          },
          {
            "id": "id_nav_link_usonumeraciodoc",
            "name": "Numeración de Documentos",
            "icon_class": "fa fa-list-ol",
            "url": "flujo/numeraciondoc"
          }
        ]
      },
      {
        "id": "id_nav_link_conf_costo",
        "name": "💰 Configuración de Costos",
        "icon_class": "fa fa-chart-line",
        "submenu": [
          {
            "id": "id_nav_link_cuentas_contables",
            "name": "Cuentas Contables",
            "icon_class": "fa fa-book",
            "url": "costo/cuentascontables"
          },
          {
            "id": "id_nav_link_centros_de_costo",
            "name": "Centros de Costo",
            "icon_class": "fa fa-building",
            "url": "costo/centros"
          },
          {
            "id": "id_nav_link_elementos_centros_de_costo",
            "name": "Centros y Elementos de Gasto",
            "icon_class": "fa fa-layer-group",
            "url": "costo/centroselemntos"
          },
          {
            "id": "id_nav_link_conf_var_globales_costo",
            "name": "Variables Globales",
            "icon_class": "fa fa-sliders-h",
            "url": "costo/varglobales"
          },
          {
            "id": "id_nav_link_elementos_filas_ficha_costo",
            "name": "Filas de la Ficha de Costo",
            "icon_class": "fa fa-table",
            "url": "costo/filasficha"
          },
          {
            "id": "id_nav_link_elementos_clasificador_de_cargo",
            "name": "Clasificador de Cargos",
            "icon_class": "fa fa-user-tag",
            "url": "costo/cargos"
          },
          {
            "id": "id_nav_link_elementos_fechainiciocosto",
            "name": "Fechas de Inicio",
            "icon_class": "fa fa-calendar-alt",
            "url": "costo/fechainicio"
          }
        ]
      },
      {
        "id": "id_nav_link_config_gen",
        "name": "⚙️ Otras Configuraciones",
        "icon_class": "fa fa-cogs",
        "url": "/otrasconfig"
      },
      {
        "id": "id_nav_link_import_all_config",
        "name": "📥 Importar todas las Configuraciones",
        "icon_class": "fa fa-upload",
        "url": "/importartodas"
      }
    ]
  }
]


