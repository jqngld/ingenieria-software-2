from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    return HttpResponse('Página home de pacientes.')


def login(request):

    return render(request, 'pacientes/login.html')