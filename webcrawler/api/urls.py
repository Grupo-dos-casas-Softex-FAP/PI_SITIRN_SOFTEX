from rest_framework.routers import DefaultRouter
from .views import Imovel_caio_ViewSet_rql, Imovel_MG_ViewSet

imovel_router = DefaultRouter()

imovel_router.register(r'imoveis_caio', Imovel_caio_ViewSet_rql)

imovel_router.register(r'imoveis_mg', Imovel_MG_ViewSet)