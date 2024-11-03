from django.shortcuts import render
from django.core.paginator import Paginator
from webcrawler.models import Imovel


# Create your views here.

# não é preciso informar que ele está na pasta de templates
# o django automaticamente reconhece isso
# se você clikar ctrl+click em render, ele mostra o que a função
# pede e faz

def dashboard(request):
    return render(request, 'web/pages/dashboard.html') # se refere a pasta web
# dentro de templates, o django ja reconhece os templates
def vizualizacao(request):
    # pega os models de imoveis e converte em objetos
    objetos = Imovel.objects.all()
    # paginator
    paginator = Paginator(objetos, 30)
    
    # obtém o numero da pagina atual na url
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'web/pages/vizualizacao.html', {'page_obj': page_obj})

def relatorio(request):
    return render(request, 'web/pages/relatorios.html')

def configuracao(request):
    return render(request, 'web/pages/configuracoes.html')

