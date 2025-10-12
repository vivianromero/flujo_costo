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
    def limpiar_validadores_recursivo(item):
        item.pop("validators", None)
        if "submenu" in item:
            item["submenu"] = [
                limpiar_validadores_recursivo(subitem)
                for subitem in item["submenu"]
                if ejecutar_validadores(subitem.get("validators", []), request)
            ]
        return item

    resultado = []
    for modulo in menu:
        if ejecutar_validadores(modulo.get("validators", []), request):
            resultado.append(limpiar_validadores_recursivo(modulo))
    return resultado



