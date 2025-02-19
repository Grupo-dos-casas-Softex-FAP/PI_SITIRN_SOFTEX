"""
URL configuration for Projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# aqui são as urls do projeto geral
# '', include(tanantanan) ele sempre vai começar com "/" e após 
# será todos os links do url de cada path
# "/home" , "/about-us" e por ai vai

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('web.urls')),
    path('api/', include('Projeto.api.urls')),
]

