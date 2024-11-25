from rest_framework.routers import DefaultRouter
from django.urls import path, include
from webcrawler.api.urls import imovel_router

router = DefaultRouter()

# app 1
# app 2

# webcrawler imovel
router.registry.extend(imovel_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
