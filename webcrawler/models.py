from django.db import models

# Create your models here.

class Imovel(models.Model):
    # baseado no abreu imoveis
    imovel_tipo = models.CharField(max_length=65)
    imovel_codigo = models.IntegerField()
    imovel_m2 = models.IntegerField()
    imovel_endereco = models.IntegerField()
    imovel_valor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)