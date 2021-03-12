from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email  #para validar o e-mail
from django.contrib.auth.models import User  #conferir se existe ou não o usuário
from django.contrib.auth.decorators import login_required
from .models import FormContato

# Create your views here.
#ADMINISTRADORES

def login(request):
    #volta pra o login se nada for postado
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)  #vê se o usuário autentica

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')  #manda pra dashboard quando dá certo

def logout(request):
    auth.logout(request)  #sair
    return redirect('index')  #voltar ao indice


def cadastro(request):
    if request.method != 'POST':  #não faz nada, se nada for postado
        return render(request, 'accounts/cadastro.html')

    #sempre voltar ao cadastro, quando dá um erro
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    #erro caso algo esteja vazio:
    if not nome or not sobrenome or not email or not usuario or not senha \
            or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio.')
        return render(request, 'accounts/cadastro.html')

    #olhar o e-mail
    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/cadastro.html')



    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter 6 caracteres ou mais.')
        return render(request, 'accounts/cadastro.html')

    #conferir se as duas senhas são iguais
    if senha != senha2:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'accounts/cadastro.html')


    #conferir se o usuário já existe
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/cadastro.html')

    #conferir se o e-mail já existe
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já existe.')
        return render(request, 'accounts/cadastro.html')

    #mensagem que deu certo
    messages.success(request, 'Registrado com sucesso! Agora faça login.')

    #criar o usuário
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')  #redirecionar para login, se não tiver logado
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)  #a postagem e a foto

    if not form.is_valid():  #se os dados do não formulário forem válidos
        messages.error(request, 'Erro ao enviar formulário.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')
    #conferir a descrição
    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais que 5 caracteres.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()  #salva
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')