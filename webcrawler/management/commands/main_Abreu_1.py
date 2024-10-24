from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

driver = webdriver.Firefox()

url = "https://abreuimoveis.com.br/venda/residencial_comercial/natal/" 
driver.get(url)

scroll_pause_time = 0.1
scroll_increment = 300
# Elemento para Scrollar 
elemento_scroll = driver.find_element(By.XPATH, "/html/body/main/section[1]/div[2]/div")
lista_imoveis = []

# Obtém a altura total do elemento scrollável
scroll_height = driver.execute_script("return arguments[0].scrollHeight;", elemento_scroll)
current_scroll = 0

# Loop para rolar a página e extrair dados
while current_scroll < scroll_height:
    # Scrolla a página para baixo

    driver.execute_script(f"arguments[0].scrollTop += {scroll_increment};", elemento_scroll)
    current_scroll += scroll_increment

    # Aguarda um momento para a página carregar
    time.sleep(scroll_pause_time)

    #"Janela" para o contéudo de tag HTML
    page_source = elemento_scroll.get_attribute('innerHTML')

    soup = BeautifulSoup(page_source, 'html.parser')
    imoveis = soup.find_all('div', class_='col-xs-12 grid-imovel')

    for imovel in imoveis:
        titulo = imovel.find('h2', class_='titulo-grid').text.strip()
        tipo = imovel.find('span', class_='thumb-status').text.strip() if imovel.find('span', class_='thumb-status') else 'Tipo não informado'
        preco = imovel.find('span', class_='thumb-price').text.strip() if imovel.find('span', class_='thumb-price') else 'Preço não informado'
        condominio = imovel.find('span', class_='item-price-condominio').text.strip() if imovel.find('span', class_='item-price-condominio') else 'Condomínio não informado'
        iptu = imovel.find('span', class_='item-price-iptu').text.strip() if imovel.find('span', class_='item-price-iptu') else 'IPTU não informado'
        endereco = imovel.find('h3', itemprop='streetAddress').text.strip() if imovel.find('h3', itemprop='streetAddress') else 'endereco não informada'
        
        codigo_tag = imovel.find('p')
        codigo = None
        if codigo_tag and codigo_tag.find('b'):
            codigo_texto = codigo_tag.get_text().replace(codigo_tag.find('b').text, '').strip()
            codigo = codigo_texto if codigo_texto else 'Código não informado'

        caracteristicas = imovel.find('div', class_='property-amenities amenities-main').text.strip().replace('\n', ' ').replace('\r', ' ')
        
        dados_imovel = {
            'titulo': titulo,
            'tipo': tipo,
            'preco': preco,
            'caracteristicas': caracteristicas,
            'condominio': condominio,
            'iptu': iptu,
            'endereco': endereco,
            'codigo': codigo
        }

        if dados_imovel not in lista_imoveis:
            lista_imoveis.append(dados_imovel)

    scroll_height = driver.execute_script("return arguments[0].scrollHeight;", elemento_scroll)

#CSV
with open('imoveis.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['titulo', 'tipo', 'preco', 'caracteristicas', 'condominio', 'iptu', 'endereco', 'codigo'])
    writer.writeheader()
    writer.writerows(lista_imoveis)

driver.quit()