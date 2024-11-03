from django.urls import path
from .views import dashboard, configuracao, relatorio, vizualizacao

# coloque os urls dos app aqui

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('dashboard', dashboard, name="dashboard"),
    path('vizualização', vizualizacao, name="vizualizacao"),
    path('relatórios', relatorio, name="relatorio"),
    path('configurações', configuracao, name="configuracao"),
]