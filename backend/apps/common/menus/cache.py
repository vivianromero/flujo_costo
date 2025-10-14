from copy import deepcopy
from django.core.cache import cache
from apps.common.menus.menus import MENU
from apps.common.filters import filtrar_menu_por_usuario


def get_user_menu(request):
    # cache_key = f"menu:{request.user.id}"
    # menu = cache.get(cache_key)
    menu = None
    if menu is None:
        menu_copy = deepcopy(MENU)
        print(f'MENU  {MENU}')
        menu = filtrar_menu_por_usuario(menu_copy, request)
        # cache.set(cache_key, menu, timeout=3600)  # 1 hora

    return menu
