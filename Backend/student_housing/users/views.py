from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def users_intro(request):
    return HttpResponse("Welcome")

def users_login(request):
    return render(request, 'login.html')

def users_register(request):
    return render(request, 'register.html')