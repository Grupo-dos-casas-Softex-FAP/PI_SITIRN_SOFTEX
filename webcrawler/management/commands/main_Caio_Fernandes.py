import requests
from bs4 import BeautifulSoup
import os
from django.core.management.base import BaseCommand
from webcrawler.models import Imovel_Caio  # Importa o modelo do Django
#import time
import re

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
        # IMPORTANTE: Para descobrir o tempo do script descomente as linhas.
        url = 'https://caiofernandes.com.br/busca?situacao_id=&busca=natal'

        lista_imoveis = []
        codigo = 0

        #start_time = time.time()

        response = requests.get(url)
        raw_code = response.text

        soup = BeautifulSoup(raw_code, 'html.parser')
        imoveis = soup.find_all('div', class_='legenda')

        def filtrar_tipo(tipo):
            tipo = tipo.lower()
            if 'casa' in tipo:
                return 'casa'
            elif 'apartamento' in tipo:
                return 'apartamento'
            elif 'terreno' in tipo:
                return 'terreno'
            elif 'ponto comercial' in tipo or 'comercial' in tipo:
                return 'comercial'
            else:
                return 'outro'

        for imovel in imoveis:
            titulo = imovel.find('h3').text.strip() if imovel.find('h3') else 'NULL'
            tipo = imovel.find('span', class_='chamada').text.strip() if imovel.find('span', class_='chamada') else 'NULL'
            tipo = filtrar_tipo(tipo)
            preco = imovel.find('span', class_='preco').text.strip() if imovel.find('span', class_='preco') else 'NULL'
            caracteristicas = imovel.find('strong').text.strip() if imovel.find('strong') else 'NULL'
            codigo = codigo + 1


            if caracteristicas:
                caracteristicas = re.sub(r'\s+', ' ', caracteristicas).strip()
                caracteristicas = re.sub(r'\s*,\s*', ',', caracteristicas)
                caracteristicas = caracteristicas.replace(' ,', ',').replace(', ', ',')

            dados_imovel = {
                'titulo': titulo,
                'tipo': tipo,
                'preco': tratar_preco(preco),
                'caracteristicas': caracteristicas,
                'codigo': codigo,
            }

            if dados_imovel not in lista_imoveis:
                lista_imoveis.append(dados_imovel)

        # with open('imoveis.csv', mode='w', newline='', encoding='utf-8') as file:
        #     writer = csv.DictWriter(file, fieldnames=['titulo', 'tipo', 'preco', 'caracteristicas'])
        #     writer.writeheader()
        #     writer.writerows(lista_imoveis)

        #end_time = time.time()
        #tempo = end_time - start_time

        #print(f"Total de imóveis encontrados: {len(lista_imoveis)}")
        #print(f"Tempo: {tempo:.2f} segundos")
                # Obtenha os códigos dos imóveis existentes no banco de dados
        codigos_existentes = set(Imovel_Caio.objects.values_list('imovel_codigo', flat=True))

        # Liste os códigos que foram processados
        codigos_processados = set()

        # Salva ou atualiza cada imóvel no banco de dados
        for dados in lista_imoveis:
            codigo = dados['codigo']
            
            # Validação: Pule imóveis com códigos inválidos
            if not codigo or codigo == 'Código não informado':
                self.stdout.write(self.style.WARNING("Imóvel ignorado devido a código inválido."))
                continue
            
            imovel, criado = Imovel_Caio.objects.update_or_create(
                # ele tenta acessar nesse codigo, e caso não exista, ele cria
                imovel_codigo=codigo,
                # esses são os dados que vão ser criados ou atualizados
                defaults={
                    'imovel_titulo': dados['titulo'],
                    'imovel_tipo': dados['tipo'],
                    'imovel_valor': dados['preco'],
                    'imovel_caracteristicas': dados['caracteristicas'],
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
            Imovel_Caio.objects.filter(imovel_codigo__in=codigos_nao_encontrados).delete()
            for codigo in codigos_nao_encontrados:
                self.stdout.write(self.style.WARNING(f"Imóvel com código '{codigo}' foi excluído do banco de dados."))
        else:
            self.stdout.write(self.style.SUCCESS("Nenhum imóvel foi excluído."))