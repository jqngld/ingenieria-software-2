from django.shortcuts import render

def home_admin(request):
    return render(request, 'admin/index.html')