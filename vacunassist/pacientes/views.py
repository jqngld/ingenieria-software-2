from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserSignUpForm

def home(request):

    return HttpResponse('Página home de pacientes.')


def login(request):

    return render(request, 'pacientes/login.html')


def signup(request):

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'pacientes/')
    else:
        form = UserSignUpForm()

    context = {'form' : form}
    return render(request, 'pacientes/signup.html', context)