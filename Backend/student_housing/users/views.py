from django.shortcuts import render, redirect
from users.models import Register
from .models import Register
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages


def users_intro(request):
    return HttpResponse("Welcome")

def users_login(request):
    if(request.method == "POST"):
        username = request.POST['username']   
        password = request.POST['password']

        try:
            user_check = Register.objects.get(username=username, password=password)
            request.session['username'] = username
            a = request.session.get('username')
            print(a)
            return redirect('users_profile', username = a)

        except:
            messages.warning(request, 'Invalid username or password. Please Try again')


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
        print("Those data are already saved in db")
        # return render(request, 'login.html')
        return redirect('users_login')
    return render(request, 'register.html')

def users_profile(request, username):
    session_data = request.session.get('username')
    if(session_data is not None):
        session_data_db = Register.objects.get(username=session_data)

    else:
        messages.warning(request, 'Please log in again to continue')
    
    return render(request, 'profile.html', {'username' : username, 'database_output' : session_data_db})

def create_post(request, username):
    created_by = request.session.get('username')
    #created_by variable ta diye post model er posted_by field e entry hobe
    return render(request, 'create_post.html', {'username' : created_by})

def users_logout(request):
    request.session.clear()
    return redirect('users_login')