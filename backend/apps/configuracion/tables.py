from apps.cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from .models import *

# ------ Conexiones a las BD de sistemas externos / Table ------
class ConexionBaseDatoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ConexionBaseDato

        fields = (
            'sistema',
            'database_name',
            'host',
            'port',
            'unidadcontable',
        )
