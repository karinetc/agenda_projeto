from django.contrib import admin

from .models import Categoria, Contato

class ContatoAdmin(admin.ModelAdmin):  #como mostra na página
    list_display = ('id','nome', 'sobrenome', 'telefone', 'email','data_criacao',
                    'categoria', 'mostrar')
    list_display_links = ('id','nome', 'sobrenome')  #onde posso clicar
    #list_filter = ('nome', 'sobrenome')  #adição de por onde filtrar
    list_per_page = 20  #10 contatos por páginas
    search_fields = ('nome', 'sobrenome', 'telefone')  #por onde posso procurar
    list_editable = ('telefone', 'mostrar')  #fica editável na primeira página

admin.site.register(Categoria)  #adicionei categoria
admin.site.register(Contato, ContatoAdmin)  #adicionei contato
