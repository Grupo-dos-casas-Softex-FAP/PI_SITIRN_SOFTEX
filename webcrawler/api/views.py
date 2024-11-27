from rest_framework import viewsets
from .serializers import ImovelSerializer
from ..models import Imovel_Caio

class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel_Caio.objects.all()
    serializer_class = ImovelSerializer
    