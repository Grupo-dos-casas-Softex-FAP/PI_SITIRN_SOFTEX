from rest_framework import serializers
from ..models import Imovel_Caio, Imovel_MG
from unidecode import unidecode

natal_zonas = {
    "centro": [
        "cidade alta", "ribeira", "tirol", "petropolis", "arena", "lagoa seca", "barro vermelho", "alecrim", "cidade da esperanca"
    ],
    "zona norte": [
        "igapo", "redinha", "pajucara", "nova descoberta", "planalto", "nordeste", "potengi", "lagoa do barro", "lagoa azul"
    ],
    "zona sul": [
        "capim macio", "neopolis", "ponta negra", "candelaria", "lagoa nova", "emaus", "belo horizonte", "cohabinal", "lagoa seca"
    ],
    "zona leste": [
        "mae luiza", "rocas", "areia preta", "cidade alta", "nossa senhora da apresentacao", "ponta negra"
    ],
    "zona oeste": [
        "boa vista", "nova natal", "vila progresso", "lagoa do meio", "quintas", "morro do careca", "redinha nova"
    ]
}

def normalizar_texto(texto):
    return unidecode(texto.lower())  # Converte para minúsculas e remove acentos

def identificar_zona_bairro(imovel_titulo):
    imovel_titulo_normalizado = normalizar_texto(imovel_titulo)
    for zona, bairros in natal_zonas.items():
        for bairro in bairros:
            if normalizar_texto(bairro) in imovel_titulo_normalizado:
                return zona, bairro
    return "desconhecido", "desconhecido"



class Imovel_Caio_Serializer(serializers.ModelSerializer):
    # criei um metodo
    zona = serializers.SerializerMethodField()
    bairro = serializers.SerializerMethodField()
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
            'zona',
            'bairro',
            'created_at',
            'updated_at',
        )
    # obrigatoriamente devo criar um metodo da classe
    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_zona(self, obj):
        zona, _ = identificar_zona_bairro(obj.imovel_titulo)
        return zona

    def get_bairro(self, obj):
        _, bairro = identificar_zona_bairro(obj.imovel_titulo)
        return bairro
    
class Imovel_MG_Serializer(serializers.ModelSerializer):
    # criei um metodo
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Imovel_MG
        fields = (
            'id',
            'imovel_titulo',
            'imovel_tipo',
            'imovel_valor',
            'imovel_caracteristicas',
            'created_at',
        )
    # obrigatoriamente devo criar um metodo da classe
    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')