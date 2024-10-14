# faça o coodigo do webscrapper aqui


# os argumentos do model, preço, codigo do imovel estão em models
# e são os seguintes: 

# imovel_tipo # é um terreno, casa, chalé
# imovel_codigo # usei o abreu imovel como ref tem bonitinho nas info
# imovel_m2  # metros quadrados, area total
# imovel_endereco # onde é
# imovel_valor # quanto é
# created_at # esses servem apenas para mencionar quando foram criados
# updated_at # não mexa neles, servem apenas para informar a data/hora

# veja que abaixo darei uma sugestão mas o local dessas 5 variáveis
# DEVEM SER COLOCADAS, são parte do model e são necessarias para
# salvar corretamente, tente também implementar um filtro, caso
# o dado salvo já exista para ele não salvar novamente darei outro exemplo
# após o de baixo

# sugestão do chatgpt:

# from django.core.management.base import BaseCommand # cria o comando pra executar no terminal
# from meu_app.models import Imovel  # Substitua 'meu_app' pelo nome do seu app
# import requests  # Biblioteca para realizar requisições HTTP

# class Command(BaseCommand):
#     help = 'Realiza scraping de dados de imóveis e salva no banco de dados'

#     def handle(self, *args, **kwargs):
#         url = 'https://exemplo.com/api/imoveis'  # URL do site para scraping
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()  # Processa a resposta como JSON, se for uma API
#             for item in data:
#                 Imovel.objects.create(
#                     nome=item['nome'],
#                     endereco=item['endereco'],
#                     preco=item['preco']
#                 )
#             self.stdout.write(self.style.SUCCESS('Dados de imóveis salvos com sucesso!'))
#         else:
#             self.stdout.write(self.style.ERROR('Falha ao obter dados de imóveis'))

# sugestão do chatgpt com filtro:

# from django.core.management.base import BaseCommand
# from meu_app.models import Imovel
# import requests

# class Command(BaseCommand):
#     help = 'Realiza scraping de dados de imóveis e salva no banco de dados'

#     def handle(self, *args, **kwargs):
#         url = 'https://exemplo.com/api/imoveis'
#         try:
#             response = requests.get(url)
#             response.raise_for_status()  # Levanta uma exceção para erros de requisição
#         except requests.RequestException as e:
#             self.stdout.write(self.style.ERROR(f'Erro ao acessar a URL: {e}'))
#             return

#         data = response.json()
#         for item in data:
#             if not Imovel.objects.filter(nome=item['nome']).exists():
#                 Imovel.objects.create(
#                     nome=item['nome'],
#                     endereco=item['endereco'],
#                     preco=item['preco']
#                 )
#         self.stdout.write(self.style.SUCCESS('Scraping e salvamento concluídos com sucesso!'))


# no final após o aplicativo estar ok basta executar o seguinte comando
# no terminal: "python manage.py scrape_imoveis"
