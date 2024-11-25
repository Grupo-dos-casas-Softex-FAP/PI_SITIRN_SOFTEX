from rest_framework.routers import DefaultRouter
from .views import ImovelViewSet

imovel_router = DefaultRouter()

imovel_router.register(r'imoveis', ImovelViewSet)