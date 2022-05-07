from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def home(request):

    return HttpResponse('Página home de pacientes.')


def login(request):

    return render(request, 'pacientes/login.html')


def register_credentials(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, 'Usuario %s creado con éxito.' % (username))
    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request, 'pacientes/register_credentials.html', context)