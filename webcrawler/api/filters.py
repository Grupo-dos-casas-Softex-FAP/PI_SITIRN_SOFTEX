# from dj_rql.filter_cls import RQLFilterClass
from dj_rql.filter_cls import AutoRQLFilterClass
from ..models import Imovel_Caio, Imovel_MG

class Imovel_caio_RQLFilterClass(AutoRQLFilterClass):
    MODEL = Imovel_Caio

class Imovel_MG_RQLFilterClass(AutoRQLFilterClass):
    MODEL = Imovel_MG




# filtros personalizados
# class Imovel_caio_RQLFilterClass(RQLFilterClass): 
#     MODEL = Imovel_Caio
#     FILTERS = [
#         'id',               # Campo básico
#         {'field': 'imovel_valor', 'lookups': ['eq', 'gt', 'lt', 'gte', 'lte']},  # Com lookups
#         {'field': 'imovel_titulo', 'lookups': ['eq', 'in']},                     # Com lookups
#     ]

# ?eq(name,apartamento)