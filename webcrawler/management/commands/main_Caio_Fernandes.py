import requests
from bs4 import BeautifulSoup
import csv
#import time
import re
# IMPORTANTE: Para descobrir o tempo do script descomente as linhas.
url = 'https://caiofernandes.com.br/busca?situacao_id=&busca=natal'

lista_imoveis = []

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

    
    if caracteristicas:
        caracteristicas = re.sub(r'\s+', ' ', caracteristicas).strip()
        caracteristicas = re.sub(r'\s*,\s*', ',', caracteristicas)
        caracteristicas = caracteristicas.replace(' ,', ',').replace(', ', ',')

    dados_imovel = {
        'titulo': titulo,
        'tipo': tipo,
        'preco': preco,
        'caracteristicas': caracteristicas
    }

    if dados_imovel not in lista_imoveis:
        lista_imoveis.append(dados_imovel)

with open('imoveis.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['titulo', 'tipo', 'preco', 'caracteristicas'])
    writer.writeheader()
    writer.writerows(lista_imoveis)

#end_time = time.time()
#tempo = end_time - start_time

#print(f"Total de imóveis encontrados: {len(lista_imoveis)}")
#print(f"Tempo: {tempo:.2f} segundos")