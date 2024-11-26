from django.db import models

# Create your models here.

class Imovel(models.Model):
    # baseado no abreu imoveis
    imovel_tipo = models.CharField(max_length=100)
    imovel_codigo = models.IntegerField(null=True, blank=True)
    imovel_m2 = models.IntegerField(null=True, blank=True)
    imovel_endereco = models.CharField(max_length=500)
    imovel_rua = models.CharField(max_length=100,null=True, blank=True)
    imovel_bairro = models.CharField(max_length=100,null=True, blank=True)
    imovel_cidade = models.CharField(max_length=100,null=True, blank=True)
    imovel_site = models.CharField(max_length=100,null=True, blank=True)
    imovel_valor = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.imovel_tipo} - Código: {self.imovel_codigo} - Valor R$: {self.imovel_valor}"

class Imovel_Caio(models.Model):
    imovel_titulo = models.CharField(max_length=500)
    imovel_tipo = models.CharField(max_length=100)
    imovel_codigo = models.IntegerField(null=True, blank=True)
    imovel_valor = models.FloatField()
    imovel_caracteristicas = models.CharField(max_length=500)
    imovel_codigo = models.IntegerField(null=True, blank=True)
    imovel_site = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f"{self.imovel_titulo} - Código: {self.imovel_codigo} - Valor R$: {self.imovel_valor}"