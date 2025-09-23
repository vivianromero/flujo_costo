from django.http import HttpResponse

def usuario_actual(request):
    return HttpResponse("Funciona")

