from django.shortcuts import render


# Create your views here.

# não é preciso informar que ele está na pasta de templates
# o django automaticamente reconhece isso
# se você clikar ctrl+click em render, ele mostra o que a função
# pede e faz

def home(request):
    return render(request, 'web/home.html') # se refere a pasta web
# dentro de templates, o django ja reconhece os templates

