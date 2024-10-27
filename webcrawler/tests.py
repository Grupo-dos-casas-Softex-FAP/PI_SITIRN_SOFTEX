from django.test import TestCase
from models import Imovel

# Create your tests here.
q = Imovel.objects.get(pk=1) 
print(q)
