# comando para o manage.py: python manage.py processar_precos
import re
from django.core.management.base import BaseCommand
from webcrawler.models import Imovel

class Command(BaseCommand):
    help = 'Processa e converte os preços de string para float'

    def handle(self, *args, **kwargs):
        imoveis = Imovel.objects.all()
        for imovel in imoveis:
            preco_str = imovel.imovel_valor
            preco_float = self.tratar_preco(preco_str)
            
            if preco_float is not None:
                imovel.imovel_valor = preco_float
                imovel.save()
                self.stdout.write(self.style.SUCCESS(f"Preço do imóvel '{imovel.imovel_codigo}' atualizado para {preco_float}"))
            else:
                self.stdout.write(self.style.WARNING(f"Preço do imóvel '{imovel.imovel_codigo}' não pôde ser convertido"))

    def tratar_preco(self, preco_str):
        # Remove "R$", pontos e substitui vírgula por ponto
        if preco_str:
            preco_str = preco_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
            try:
                return float(preco_str)
            except ValueError:
                return None
        return None
