from rest_framework import serializers
from ..models import Imovel

class ImovelSerializer(serializers.ModelSerializer):
    # criei um metodo
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Imovel
        fields = (
            'id',
            'imovel_tipo',
            'imovel_codigo',
            'imovel_endereco',
            'imovel_valor',
            'created_at',
        )
    # obrigatoriamente devo criar um metodo da classe
    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')