import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from webcrawler.models import Imovel  # Importa o modelo do Django

def tratar_tipo(tipo):
    tipo = tipo.lower()
    if "casa" in tipo:
        return "casa"
    elif "apartamento" in tipo:
        return "apartamento"
    elif "terreno" in tipo:
        return "terreno"
    elif "comercial" in tipo or "ponto comercial" in tipo:
        return "comercial"
    else:
        return "outro"


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
        # Configuração e inicialização do driver do Selenium
        driver = webdriver.Chrome()
        url = "https://abreuimoveis.com.br/venda/residencial_comercial/natal/"
        driver.get(url)

        # Parâmetros de scroll e elemento de rolagem
        scroll_pause_time = 0.1
        scroll_increment = 300
        elemento_scroll = driver.find_element(By.XPATH, "/html/body/main/section[1]/div[2]/div")
        lista_imoveis = []
        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", elemento_scroll)
        current_scroll = 0

        # Loop para rolar a página e extrair dados
        while current_scroll < scroll_height:
            driver.execute_script(f"arguments[0].scrollTop += {scroll_increment};", elemento_scroll)
            current_scroll += scroll_increment
            time.sleep(scroll_pause_time)

            page_source = elemento_scroll.get_attribute('innerHTML')
            soup = BeautifulSoup(page_source, 'html.parser')
            imoveis = soup.find_all('div', class_='col-xs-12 grid-imovel')

            for imovel in imoveis:
                titulo = imovel.find('h2', class_='titulo-grid').text.strip()
                tipo = imovel.find('h2', class_='titulo-grid').text.strip()
                preco = imovel.find('span', class_='thumb-price').text.strip() if imovel.find('span', class_='thumb-price') else 'Preço não informado'
                condominio = imovel.find('span', class_='item-price-condominio').text.strip() if imovel.find('span', class_='item-price-condominio') else 'Condomínio não informado'
                iptu = imovel.find('span', class_='item-price-iptu').text.strip() if imovel.find('span', class_='item-price-iptu') else 'IPTU não informado'
                endereco = imovel.find('h3', itemprop='streetAddress').text.strip() if imovel.find('h3', itemprop='streetAddress') else 'endereço não informado'
                
                codigo_tag = imovel.find('p')
                codigo = None
                if codigo_tag and codigo_tag.find('b'):
                    codigo_texto = codigo_tag.get_text().replace(codigo_tag.find('b').text, '').strip()
                    codigo = codigo_texto if codigo_texto else 'Código não informado'

                caracteristicas = imovel.find('div', class_='property-amenities amenities-main').text.strip().replace('\n', ' ').replace('\r', ' ')

                dados_imovel = {
                    'titulo': titulo,
                    'tipo': tratar_tipo(tipo),
                    'preco': tratar_preco(preco),
                    'caracteristicas': caracteristicas,
                    'condominio': condominio,
                    'iptu': iptu,
                    'endereco': endereco,
                    'codigo': codigo,
                    # 'site': 1,
                }

                if dados_imovel not in lista_imoveis:
                    lista_imoveis.append(dados_imovel)

            # Atualiza a altura do scroll para continuar rolando
            scroll_height = driver.execute_script("return arguments[0].scrollHeight;", elemento_scroll)

        driver.quit()
        # Valide que a raspagem foi bem-sucedida antes de qualquer exclusão/inativação
        if len(lista_imoveis) == 0:
            self.stdout.write(self.style.ERROR("Erro na raspagem: Nenhum imóvel foi encontrado."))
            return
        
        # Obtenha os códigos dos imóveis existentes no banco de dados
        codigos_existentes = set(Imovel.objects.values_list('imovel_codigo', flat=True))

        # Liste os códigos que foram processados
        codigos_processados = set(dados['codigo'] for dados in lista_imoveis)

        # Salva ou atualiza cada imóvel no banco de dados
        for dados in lista_imoveis:
            codigo = dados['codigo']
            
            # Validação: Pule imóveis com códigos inválidos
            if not codigo or codigo == 'Código não informado':
                self.stdout.write(self.style.WARNING("Imóvel ignorado devido a código inválido."))
                continue
            
            imovel, criado = Imovel.objects.update_or_create(
                # ele tenta acessar nesse codigo, e caso não exista, ele cria
                imovel_codigo=codigo,
                # esses são os dados que vão ser criados ou atualizados
                defaults={
                    'imovel_titulo': dados['titulo'],
                    'imovel_tipo': dados['tipo'],
                    'imovel_endereco': dados['endereco'],
                    'imovel_caracteristicas': dados['caracteristicas'],
                    'imovel_valor': dados['preco'],
                    'imovel_site': 'Abreu',
                }
            )
            codigos_processados.add(codigo)  # Adicione o código processado à lista
            
            if criado:
                self.stdout.write(self.style.SUCCESS(f"Imóvel '{dados['codigo']}' criado com sucesso."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Imóvel '{dados['codigo']}' atualizado com sucesso."))
        
        # Identifique os códigos que não foram processados
        codigos_nao_encontrados = codigos_existentes - codigos_processados

        # Em vez de excluir, marque como inativos
        if codigos_nao_encontrados:
            Imovel.objects.filter(imovel_codigo__in=codigos_nao_encontrados).update(ativo=False)
            for codigo in codigos_nao_encontrados:
                self.stdout.write(self.style.WARNING(f"Imóvel com código '{codigo}' marcado como inativo."))
        else:
            self.stdout.write(self.style.SUCCESS("Nenhum imóvel foi marcado como inativo."))