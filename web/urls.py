from django.urls import path
from web.views import home

# coloque os urls dos app aqui

urlpatterns = [
    path('', home),
]