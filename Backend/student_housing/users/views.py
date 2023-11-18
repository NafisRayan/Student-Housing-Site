from django.shortcuts import render, redirect
from users.models import Register
from .models import Register
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from users.models import DormRoom
from django.shortcuts import get_object_or_404
from .forms import CommentForm



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
        # print("Those data are already saved in db")
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

def create_post(request,username):
    created_by = request.session.get('username')
    if request.method=="POST":
        title=request.POST['title']
        content=request.POST['content']
        type= request.POST['type']
        price=request.POST['price']
        register_instance = get_object_or_404(Register, username=created_by)
       
        ins= DormRoom(title=title,content=content, type=type,  price=price, posted_by = register_instance)
        ins.save()
        
    return render(request, 'create_post.html', {'username' : created_by})

def users_logout(request):
    request.session.clear()
    return redirect('users_login')


def Comment_view(request,pk):   # pk >> primary key
    commentform= CommentForm()
    if request.method== 'POST':
        commentform= CommentForm(request.POST)
        if commentform.is_valid():
            cd= commentform.cleaned_data
            print(cd)
            new_comment= commentform.save(commit=False)
            new_comment.post= post.objects.get(pk=pk)
            new_comment.save()
            
            
    return render(request , 'comment_post.html', {'commentform':commentform})

    
