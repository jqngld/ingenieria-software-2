from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserSignUpForm 
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm

def home(request):

    return HttpResponse('Página home de pacientes.')


def login(request):
    form = AuthenticationForm()
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


