from django.shortcuts import render
from users.models import Register

# Create your views here.
from django.http import HttpResponse


def users_intro(request):
    return HttpResponse("Welcome")

def users_login(request):
    return render(request, 'login.html')

def users_register(request):
    if request.method=="POST":
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        nid= request.POST['nid']
        # Location= request.POST['Location']
        #print(username, email, password, nid)
        ins= Register(username=username, email=email, password=password, nid=nid)
        ins.save()
        print("Those data are alredy save in db")
    return render(request, 'register.html')