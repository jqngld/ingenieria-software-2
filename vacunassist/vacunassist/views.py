from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    return HttpResponse('Página home.')


def login(request):

    return render(request, 'paciente/login.html')