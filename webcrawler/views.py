from django.shortcuts import render


# Create your views here.

# não é preciso informar que ele está na pasta de templates
# o django automaticamente reconhece isso
# se você clikar ctrl+click em render, ele mostra o que a função
# pede e faz

def home(request):
    return render(request, 'webcrawler/home.html') # se refere a pasta web
# dentro de templates, o django ja reconhece os templates

# a principio na views vai ter as requisições, pode mudar esse home a vontade
# o principal aqui é cuidar das requisições que o webcrawler terá que
# pegar 