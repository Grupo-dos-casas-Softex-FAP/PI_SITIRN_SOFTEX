from rest_framework.viewsets import ModelViewSet
from dj_rql.drf import RQLFilterBackend
from .serializers import Imovel_Caio_Serializer, Imovel_MG_Serializer
from ..models import Imovel_Caio, Imovel_MG
from .filters import Imovel_caio_RQLFilterClass, Imovel_MG_RQLFilterClass

# class Imovel_caio_ViewSet(viewsets.ModelViewSet):
#     queryset = Imovel_Caio.objects.all()
#     serializer_class = Imovel_Caio_Serializer

class Imovel_MG_ViewSet(ModelViewSet):
    queryset = Imovel_MG.objects.all()
    serializer_class = Imovel_MG_Serializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = Imovel_MG_RQLFilterClass
    
class Imovel_caio_ViewSet_rql(ModelViewSet):
    queryset = Imovel_Caio.objects.all()
    serializer_class = Imovel_Caio_Serializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = Imovel_caio_RQLFilterClass