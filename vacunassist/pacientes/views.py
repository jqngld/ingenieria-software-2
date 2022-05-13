import email
from email import message
from lib2to3.pgen2 import token
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserSignUpForm,UserSign
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django import forms
from django.contrib.auth import authenticate
def home(request):

    return HttpResponse('Página home de pacientes.')


def login(request):   
    if request.method == 'POST':
       form = UserSign(request.POST)
       if form.is_valid(): 
            form.save()
            mail= form.cleaned_data.get("email")
            password= form.cleaned_data.get("contraseña")
            tok= form.cleaned_data.get("token")
            usuario= authenticate(email = mail,contraseña = password , token = tok )
            if usuario is not None:
                login(request,usuario)
                return redirect('/pacientes/')
            else:
                 messages.error(request, "usuario no valido")  
       else: 
             messages.error(request, "informacion")                     
    else:
       form = UserSign()      
    context = {'form' : form}
    return render(request, 'pacientes/login.html', context)




def signup(request):

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/pacientes/')
    else:
        form = UserSignUpForm()

    context = {'form' : form}
    return render(request, 'pacientes/signup.html', context)


