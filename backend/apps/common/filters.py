import importlib

def ejecutar_validadores(validators, user):
    for path in validators:
        modulo_path, func_name = path.rsplit('.', 1)
        modulo = importlib.import_module(modulo_path)
        funcion = getattr(modulo, func_name)
        if not funcion(user):
            return False
    return True

def filtrar_menu_por_usuario(menu, request):
    resultado = []

    for modulo in menu:
        if not ejecutar_validadores(modulo.get("validators", []), request):
            continue

        subfiltradas = [
            op for op in modulo.get("submenu", [])
            if ejecutar_validadores(op.get("validators", []), request)
        ]


        resultado.append({
            "id": modulo["id"],
            "name": modulo["name"],
            "icon_class": modulo.get("icon_class", ""),
            "submenu": subfiltradas
        })

    return resultado

