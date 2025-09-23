# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver
#
# from apps.codificadores.models import FichaCostoFilas, NumeracionDocumentos, TipoDocumento, ConfiguracionesGen
# from apps.flujo.models import FechaPeriodo
#
#
# @receiver(post_delete, sender=FichaCostoFilas)
# def _renumerar_filas(sender, instance, **kwargs):
#     """
#     Renumera las filas restantes después de eliminar una.
#     """
#     # Descomponer la jerarquía de la fila eliminada (ej. "2" -> ["2"])
#     nivel_eliminado = instance.fila.split('.')
#     nivel_padre = '.'.join(nivel_eliminado[:-1])  # El nivel superior, si existe
#
#     # Identificar filas que deben ser renumeradas
#     if nivel_padre:
#         # Filtrar filas que comparten el mismo prefijo y que siguen al eliminado
#         filas_a_renumerar = FichaCostoFilas.objects.filter(
#             fila__startswith=nivel_padre + '.'
#         ).order_by('fila')
#     else:
#         # Filtrar filas del nivel más alto (sin padre) después del eliminado
#         filas_a_renumerar = FichaCostoFilas.objects.filter(
#             fila__regex=r'^\d+(\.\d+)*$'
#         ).order_by('fila')
#
#     # Mantener un mapeo para las renumeraciones
#     nueva_fila_padres = {}
#
#     # Renumerar las filas
#     for fila in filas_a_renumerar:
#         partes = fila.fila.split('.')
#
#         # Si estamos en el mismo nivel jerárquico
#         if len(partes) == len(nivel_eliminado) and int(partes[-1]) > int(nivel_eliminado[-1]):
#             partes[-1] = str(int(partes[-1]) - 1)  # Reducir el último número
#             nueva_fila = '.'.join(partes)
#             nueva_fila_padres[fila.fila] = nueva_fila
#             fila.fila = nueva_fila
#             fila.save()
#
#         # Para los hijos de las filas renumeradas
#         elif any(p in fila.fila for p in nueva_fila_padres):
#             # Actualizar hijos con el nuevo prefijo
#             prefijo_antiguo = next((k for k in nueva_fila_padres if fila.fila.startswith(k)), None)
#             if prefijo_antiguo:
#                 fila.fila = fila.fila.replace(prefijo_antiguo, nueva_fila_padres[prefijo_antiguo], 1)
#                 fila.save()
#
# @receiver([post_save, post_delete], sender=NumeracionDocumentos)
# @receiver([post_save, post_delete], sender=TipoDocumento)
# @receiver([post_save, post_delete], sender=FechaPeriodo)
# @receiver([post_save, post_delete], sender=ConfiguracionesGen)
# def invalidate_config_cache(sender, instance, **kwargs):
#     """
#     Limpiar la cache.
#     """
#     if sender == NumeracionDocumentos:
#         NumeracionDocumentos.objects_cache.clear_cache()
#     elif sender == TipoDocumento:
#         TipoDocumento.objects.clear_cache()
#     elif sender == FechaPeriodo:
#         FechaPeriodo.objects.clear_cache()
#     elif sender == ConfiguracionesGen:
#         ConfiguracionesGen.objects.clear_cache()




