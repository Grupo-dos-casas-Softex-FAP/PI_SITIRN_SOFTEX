import requests
from bs4 import BeautifulSoup
import csv
import time

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

def extrair_dados(imóveis):
    lista_imóveis = []
    for imóvel in imóveis:
        título = imóvel.find('h3', class_ = 'lead text-body text-truncate mb-3').text.strip() if imóvel.find('h3', class_ = 'lead text-body text-truncate mb-3') else 'NULL'
        tipo = imóvel.find('p', class_='text-body mb-3').text.strip() if imóvel.find('p', class_='text-body mb-3') else ''
        tipo = filtrar_tipo(tipo)
        preço = imóvel.find('span', class_='badge rounded-pill bg-dark fw-light').text.strip() if imóvel.find('span', class_='badge rounded-pill bg-dark fw-light') else 'NULL'
        características = imóvel.find('ul', class_ = 'list-inline text-truncate mt-auto m-0').text.strip() if imóvel.find('ul', class_ = 'list-inline text-truncate mt-auto m-0') else 'NULL'
        endereço = imóvel.find('div', class_ = 'card-footer text-body text-truncate mt-auto').text.strip() if imóvel.find('div', class_ = 'card-footer text-body text-truncate mt-auto') else 'NULL'

        dados_imóvel = {
            'título': título,
            'tipo': tipo,
            'preço': preço,
            'características': características,
            'endereço': endereço
        }
        
        if dados_imóvel not in lista_imóveis:
            lista_imóveis.append(dados_imóvel)
    return lista_imóveis

def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def paginas(base_url, max_pages):
    all_imoveis = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        start_time = time.time()
        html = obter_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        imoveis = soup.find_all('section', class_='col-12 col-md-6 col-xl-4 mb-4')  
        all_imoveis.extend(extrair_dados(imoveis))
        end_time = time.time()
        print(f'Página {page} raspada em {end_time - start_time:.2f} segundos')
    return all_imoveis

base_url = 'https://www.mgfimoveis.com.br/venda/imoveis/rn-natal' 
max_pages = 504  

imoveis = paginas(base_url, max_pages)
save_to_csv(imoveis, 'imoveis.csv')
