from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.common.menus.cache import get_user_menu

class MenuView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        menu = get_user_menu(request)
        return Response(menu)

