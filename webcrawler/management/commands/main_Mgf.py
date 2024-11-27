import requests
from bs4 import BeautifulSoup
import time
import os
from django.core.management.base import BaseCommand
from webcrawler.models import Imovel_MG  # Importa o modelo do Django
def obter_html(url):
    resposta = requests.get(url)
    return resposta.text

def filtrar_tipo(tipo):
    tipo = tipo.lower()
    if 'casa' in tipo:
        return 'casa'
    elif 'apartamento' in tipo:
        return 'apartamento'
    elif 'terreno' in tipo:
        return 'terreno'
    elif 'ponto comercial' in tipo or 'comercial' in tipo:
        return 'ponto comercial'
    else:
        return 'outro'

def extrair_dados(imóveis, codigo):
    lista_imóveis = []
    for imóvel in imóveis:
        título = imóvel.find('h3', class_ = 'lead text-body text-truncate mb-3').text.strip() if imóvel.find('h3', class_ = 'lead text-body text-truncate mb-3') else 'NULL'
        tipo = imóvel.find('p', class_='text-body mb-3').text.strip() if imóvel.find('p', class_='text-body mb-3') else ''
        tipo = filtrar_tipo(tipo)
        preço = imóvel.find('span', class_='badge rounded-pill bg-dark fw-light').text.strip() if imóvel.find('span', class_='badge rounded-pill bg-dark fw-light') else 'NULL'
        características = imóvel.find('ul', class_ = 'list-inline text-truncate mt-auto m-0').text.strip() if imóvel.find('ul', class_ = 'list-inline text-truncate mt-auto m-0') else 'NULL'
        endereço = imóvel.find('div', class_ = 'card-footer text-body text-truncate mt-auto').text.strip() if imóvel.find('div', class_ = 'card-footer text-body text-truncate mt-auto') else 'NULL'
        codigo += 1

        dados_imóvel = {
            'título': título,
            'tipo': tipo,
            'preço': tratar_preco(preço),
            'codigo': codigo,
            'características': características,
            'endereço': endereço,
        }
        
        if dados_imóvel not in lista_imóveis:
            lista_imóveis.append(dados_imóvel)
    return lista_imóveis, codigo

def paginas(base_url, max_pages):
    codigo = 0
    all_imoveis = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        start_time = time.time()
        html = obter_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        imoveis = soup.find_all('section', class_='col-12 col-md-6 col-xl-4 mb-4')  
        dados_pagina, codigo = extrair_dados(imoveis, codigo)
        all_imoveis.extend(dados_pagina)
        end_time = time.time()
        print(f'Página {page} raspada em {end_time - start_time:.2f} segundos')
    return all_imoveis


def tratar_preco(preco_str):
    # Remove "R$", pontos e substitui vírgula por ponto
    if preco_str:
        preco_str = preco_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(preco_str)
        except ValueError:
            return 0.0
    return 0.0

# Configura o ambiente do Django antes de importar o modelo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PI_SITIRN_SOFTEX.settings')

# comando padrão que tem que vim para poder executar no manage.py do django
class Command(BaseCommand):
    help = 'Realiza scraping de imóveis do site Abreu Imóveis e atualiza o banco de dados'
    
    
    # só colocar dentro
    def handle(self, *args, **kwargs):
        base_url = 'https://www.mgfimoveis.com.br/venda/imoveis/rn-natal' 
        max_pages = 504  
        codigo = 0

        imoveis = paginas(base_url, max_pages)
        codigos_existentes = set(Imovel_MG.objects.values_list('imovel_codigo', flat=True))

        # Liste os códigos que foram processados
        codigos_processados = set()

        # Salva ou atualiza cada imóvel no banco de dados
        for dados in imoveis:
            codigo = dados['codigo']
            
            # Validação: Pule imóveis com códigos inválidos
            if not codigo or codigo == 'Código não informado':
                self.stdout.write(self.style.WARNING("Imóvel ignorado devido a código inválido."))
                continue
            
            criado = Imovel_MG.objects.update_or_create(
                # ele tenta acessar nesse codigo, e caso não exista, ele cria
                imovel_codigo=codigo,
                # esses são os dados que vão ser criados ou atualizados
                defaults={
                    'imovel_titulo': dados['título'],
                    'imovel_tipo': dados['tipo'],
                    'imovel_valor': dados['preço'],
                    'imovel_caracteristicas': dados['características'],
                    'imovel_endereco': dados['endereço'],
                    'imovel_site': 'CaioFernandes',
                }
            )
            codigos_processados.add(codigo)  # Adicione o código processado à lista
            
            if criado:
                self.stdout.write(self.style.SUCCESS(f"Imóvel '{dados['codigo']}' criado com sucesso."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Imóvel '{dados['codigo']}' atualizado com sucesso."))
        
        # Identifique os códigos que não foram processados
        codigos_nao_encontrados = codigos_existentes - codigos_processados
        
        # Exclua imóveis com os códigos não encontrados
        if codigos_nao_encontrados:
            Imovel_MG.objects.filter(imovel_codigo__in=codigos_nao_encontrados).delete()
            for codigo in codigos_nao_encontrados:
                self.stdout.write(self.style.WARNING(f"Imóvel com código '{codigo}' foi excluído do banco de dados."))
        else:
            self.stdout.write(self.style.SUCCESS("Nenhum imóvel foi excluído."))
        
