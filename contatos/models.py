from django.db import models
from django.utils import timezone
# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):  #o nome fica certo
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=255)  #limitando o texto
    sobrenome = models.CharField(max_length=255, blank=True)  #é opcional
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now )
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)  #relação de tabelas
    mostrar = models.BooleanField(default=True)  #V ou F
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/d')  #uma pasta para cada dia do mês

    def __str__(self):  #o nome fica certo
        return self.nome


#python manage.py makemigrations
#não mexer na pasta migrations
#python manage.py migrations
#criou as tabelas nos bancos de dados (id é automático)

#serve para criação e alteração