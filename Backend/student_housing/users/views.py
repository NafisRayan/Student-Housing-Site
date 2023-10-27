from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def users_intro(request):
    return HttpResponse("Welcome")