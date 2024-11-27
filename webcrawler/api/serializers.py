from rest_framework import serializers
from ..models import Imovel_Caio

class ImovelSerializer(serializers.ModelSerializer):
    # criei um metodo
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Imovel_Caio
        fields = (
            'id',
            'imovel_titulo',
            'imovel_tipo',
            'imovel_valor',
            'imovel_caracteristicas',
            'imovel_site',
            'created_at',
        )
    # obrigatoriamente devo criar um metodo da classe
    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')