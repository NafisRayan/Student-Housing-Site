from django.shortcuts import render, redirect
from users.models import Register
from .models import Register, Comment, Notification
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from users.models import DormRoom
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings


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
       
        ins= DormRoom(title=title,content=content, type=type,  price=price, link='', posted_by = register_instance)
        ins.save()

        ins.link = f'http://127.0.0.1:8000/users/{created_by}/posts/learn_more/{ins.id}'
        ins.save()

        
    return render(request, 'create_post.html', {'username' : created_by})

def users_logout(request):
    request.session.clear()
    return redirect('users_login')

def show_posts(request, username):
    username = request.session.get('username')
    posts = DormRoom.objects.all()
    
    print(posts)

    return render(request, 'dorm_room_details.html', {'dorm_rooms' : posts, 'username' : username})

def learn_more(request, pk, username):
    username = request.session.get('username')
    post = DormRoom.objects.get(id = pk)
    show_del = False
    post_username = post.posted_by.username
    show_bookmark = False

    if(post_username == username):
        show_del = True

    #show if bookmarked or not
    find_user = get_object_or_404(Register, username= username)
    check_bookmark = DormRoom.objects.filter(bookmarked_by = find_user, id=post.id)

    if(len(check_bookmark) > 0):
        show_bookmark = True

    else:
        show_bookmark = False

    #show if proposal already sent
    post_find = get_object_or_404(DormRoom, id=pk)
    has_sent_proposal = Notification.objects.filter(post=post_find, user=find_user).exists()
    check_own_post = DormRoom.objects.filter(id=pk)

    own=False

    if(check_own_post[0].posted_by.username == username):
        own = True
    
    return render(request, 'dorm_room_post_detail.html', {'details' : post, 'username' : username, 'delButton' : show_del, 'bookRemButton' : show_bookmark, 'checkProposal' : has_sent_proposal, 'own' : own})


def own_posts(request, username):
    username = request.session.get('username')
    user = get_object_or_404(Register, username=username)
    posts = DormRoom.objects.filter(posted_by = user)

    return render(request, 'own_posts.html', {'details' : posts, 'username' : username})

def delete_post(request, pk, username):
    username = request.session.get('username')
    post = DormRoom.objects.get(id = pk)
    post.delete()
    return render(request, 'delete_post.html', {'details' : post, 'username' : username})

def comment_dorm_room(request, username, pk):
    username = request.session.get('username')
    dorm_room = get_object_or_404(DormRoom, id=pk)
    commentor = get_object_or_404(Register, username= username)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            
            # Create a new Comment instance
            new_comment = Comment(comment=comment_text, commented_by=commentor)
            new_comment.save()
            
            # Append the new comment to the DormRoom instance
            dorm_room.comments.add(new_comment)

    return redirect('learn_more', pk=pk, username=username)

def search_res(request, username):
    
    return render(request, 'search.html', {'username' : username})

def bookmark_a_post(request, username, pk):
    username = request.session['username']
    dorm_room = get_object_or_404(DormRoom, id=pk)
    user = get_object_or_404(Register, username=username)

    if(request.method == 'POST'):
        dorm_room.bookmarked_by.add(user)
        dorm_room.save()

    return render(request, 'bookmark_success.html', {'details' : dorm_room, 'username' : username})

def bookmarked(request, username):
    find_user = get_object_or_404(Register, username= username)
    bookmarked_posts = DormRoom.objects.filter(bookmarked_by = find_user)
    return render(request, 'bookmarked_posts.html', {'username' : username, 'details' : bookmarked_posts})

def remove_bookmark(request, username, pk):
    username = request.session['username']
    find_user = get_object_or_404(Register, username= username)
    dorm_room = get_object_or_404(DormRoom, id=pk)

    if(request.method == 'POST'):
        dorm_room.bookmarked_by.remove(find_user)
        dorm_room.save()

    return render(request, 'bookmark_remove_success.html', {'username' : username, 'details' : dorm_room})

def search(request, username):
    username = request.session['username']
    res = DormRoom.objects.none()
    if(request.method == 'POST'):
        q = request.POST['query']
        res = DormRoom.objects.filter(title__icontains=q)
    # print(res)
    return render(request, 'searching.html', {'username' : username, 'res' : res})

def sort(request):
    sort = request.GET.get('sort')
    if sort == None or sort == 'low':
        sort = 'low'
        posts = DormRoom.objects.all().order_by('price')
    elif sort == 'high':
        posts = DormRoom.objects.all().order_by('-price')
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    print(f'Inside sorting page!, {sort}')
    
    return render(request, 'sorting.html', {'username' : username,'posts':posts})



def show_posts(request, username):
    username = request.session.get('username')
    posts = DormRoom.objects.all()

    # Sorting logic
    sort_option = request.POST.get('sort', 'default')
    if sort_option == 'price_high_to_low':
        posts = posts.order_by('-price')  # Sort by price in descending order (highest to lowest)
    # Add more sorting options as needed

    return render(request, 'dorm_room_details.html', {'dorm_rooms': posts, 'username': username, 'sort_option': sort_option})

def send_rent_proposal(request, username, pk):
    username = request.session.get('username')
    post = get_object_or_404(DormRoom, id=pk)
    user = get_object_or_404(Register, username=username)

    if(request.method == "POST"):
        notification = Notification(post=post, user=user)
        notification.save()

    return render(request, 'rent_proposal_success.html', {'details' : post, 'username' : username})

def unsend_rent_proposal(request, username, pk):
    username = request.session.get('username')
    post = get_object_or_404(DormRoom, id=pk)
    user = get_object_or_404(Register, username=username)
    notification_inst = Notification.objects.filter(post = post, user = user)

    if(request.method == 'POST'):
        if(request.method == 'POST'):
            notification_inst.delete()

    return render(request, 'unsend_proposal.html', {'details' : post, 'username' : username})

def notifications(request, username):
    viewer_username = request.session.get('username')
    viewer = get_object_or_404(Register, username=viewer_username)
    notifications = Notification.objects.filter(post__posted_by=viewer)

    return render(request, 'notifications.html', {'dorm_rooms' : notifications, 'username' : username})

    

# def send_email_view(request,username, pk):
#     # Your logic to send the email goes here
#     if request.method=="POST":
#         message= request.POST['message']
#         email= request.POST['email']
#         name= request.POST['name']
#         send_mail(
#             'Contect from', #for title
#             messege, #for read massage
#         )
#     return render(request, 'dorm_room_post_details.html')

def sendEmailPage(request):
    return render(request,'email.html',{})

