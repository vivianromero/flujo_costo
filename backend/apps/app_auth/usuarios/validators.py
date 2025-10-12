def is_superuser(request):
    """
    Returns True if request.user is superuser else returns False
    """
    return is_authenticated(request) and request.user.is_superuser


def is_staff(request):
    """
    Returns True if request.user is staff else returns False
    """
    return is_authenticated(request) and request.user.is_staff


def is_authenticated(request):
    """
    Returns True if request.user authenticated else returns False
    """
    return request.user.is_authenticated


def is_anonymous(request):
    """
    Returns True if request.user is not authenticated else returns False
    """
    return not request.user.is_authenticated


def user_has_permission(request, permission):
    """
    Returns True if request.user has the permission else returns False
    :param request: HttpRequest
    :param permission: Permission to be searched
    """
    return request.user.has_perm(permission)


def is_adminempresaoradmin(request):
    """
    Retorna verdadero si el usuario es 'Administrator', si no devuelve falso
    """
    return is_authenticated(request) and (
                request.user.is_admin or request.user.is_superuser or request.user.is_adminempresa)


def is_admin(request):
    """
    Retorna verdadero si el usuario es 'Administrator', si no devuelve falso
    """
    return is_authenticated(request) and (request.user.is_admin or request.user.is_superuser)


def is_operflujo(request):
    """
    Retorna verdadero si el usuario es operador de flujo, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_operflujo


def is_opercosto(request):
    """
    Retorna verdadero si el usuario es operador de costo, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_opercosto


def is_consultor(request):
    """
    Retorna verdadero si el usuario es consultor, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_consultor


def is_adminempresa(request):
    """
    Retorna verdadero si el usuario es admin de empresa, si no devuelve falso
    """
    print(f'Is adminempresa {request.user} {is_authenticated(request) and (request.user.is_adminempresa or request.user.is_superuser)}')
    return is_authenticated(request) and (request.user.is_adminempresa or request.user.is_superuser)


def is_consultoremp(request):
    """
    Retorna verdadero si el usuario es consultor de empresa, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_consultoremp


def is_adminoroperador(request):
    """
    Retorna verdadero si el usuario es 'Administrator', si no devuelve falso
    """
    return is_authenticated(request) and (request.user.is_admin or request.user.is_superuser or request.user.is_adminempresa or request.user.is_opercosto or request.user.is_operflujo)

def is_adminoroperadorcosto(request):
    """
    Retorna verdadero si el usuario es 'Administrator', si no devuelve falso
    """
    return is_authenticated(request) and (request.user.is_admin or request.user.is_superuser or request.user.is_adminempresa or request.user.is_opercosto)