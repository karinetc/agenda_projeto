from django.db import models
from contatos.models import Contato  #uso o modelo de contatos, para o formulário ser igual
from django import forms  #cria o formulário


class FormContato(forms.ModelForm):  #importa o modelo de formulário
    class Meta:
        model = Contato  #o modelo
        exclude = ('mostrar',)  #e o que eu não quero que apareça no formulário