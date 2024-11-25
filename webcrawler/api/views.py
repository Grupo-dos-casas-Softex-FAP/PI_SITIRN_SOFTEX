from rest_framework import viewsets
from .serializers import ImovelSerializer
from ..models import Imovel


class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
    