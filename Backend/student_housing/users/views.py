from django.shortcuts import render, redirect
from users.models import Register
from .models import Register, Comment, Notification, Discussion, ProposalResponse
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from users.models import DormRoom
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from sslcommerz_lib import SSLCOMMERZ 
from datetime import date, timedelta


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

def show_posted_profile(request, username, pk):
    post = DormRoom.objects.get(id=pk)
    acc_of = Register.objects.filter(username=post.posted_by.username)

    return render(request, 'show_posted_profile.html', {'username' : username, 'posted_by': acc_of[0]})

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
    posted_by_url = 'http://127.0.0.1:8000/users/'+ post_username+'/profile/'+pk

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
    
    return render(request, 'dorm_room_post_detail.html', {'details' : post, 'username' : username, 'delButton' : show_del, 'bookRemButton' : show_bookmark, 'checkProposal' : has_sent_proposal, 'own' : own, 'url' : posted_by_url})


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
        proposal = ProposalResponse(notification=notification, paid=False)
        proposal.save()

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
    sent_proposals = Notification.objects.filter(user=viewer)
    proposal_res = ProposalResponse.objects.filter(notification__in=sent_proposals)

    return render(request, 'notifications.html', {'dorm_rooms' : notifications, 'username' : username, 'sent':sent_proposals, 'res':proposal_res})

    

def send_email_view(request,username, pk):
    # Your logic to send the email goes here
    username = request.session['username']
    
    return render(request, 'email.html', {'username' : username})

def email_success(request, username):
    username = request.session['username']

    if request.method=="POST":
        # message= request.POST['message']
        # email= request.POST['email']
        # name= request.POST['name']
        message = request.POST.get('message', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        send_mail(
            'Contect from', #for title
            message, #for read massage
            "settings.EMAIL_HOST_USER",
            [email, "jane@example.com"],
        )

    return render(request, 'email_success.html', {'username' : username})


# def sendEmailPage(request):
#     return render(request,'email.html',{})
# def send_email_view(request, username, pk):
#     if request.method == "POST":
#         message = request.POST.get('message', '')
#         email = request.POST.get('email', '')
#         name = request.POST.get('name', '')

#         # Check if required fields are not empty
#         if message and email:
#             send_mail(
#                 'Contact from',  # for title
#                 message,  # for read message
#                 settings.EMAIL_HOST_USER,
#                 [email, "jane@example.com"],
#             )

#     return render(request, 'email.html',  {'username' : username})

@csrf_exempt
def group_chat(request, username):
    username = request.session['username']
    user = Register.objects.get(username=username)
    if(request.method == "POST"):
        chat = request.POST['sendtext']
        ins = Discussion(user=user, message=chat)
        ins.save()

    discussions = Discussion.objects.all()

    return render(request, 'discussion.html', {'username': username, 'dis':discussions})

def manage_proposal(request, username, pk):
    try:
        username = request.session['username']
        notif = Notification.objects.get(id=pk)
        proposal_res = ProposalResponse.objects.get(notification=notif)
        print(proposal_res.response)
        return render(request, 'manage.html', {'username': username, 'notif': notif, 'res':proposal_res})
    except Notification.DoesNotExist:
        # Handle the case where the Notification doesn't exist
        # You might want to redirect or display an error message
        return HttpResponse("Notification not found.")

def accept_proposal(request, username, pk):
    username = request.session['username']
    notif = Notification.objects.get(id=pk)
    exists = ProposalResponse.objects.get(notification=notif)


    if(request.method == 'POST'):
        exists.response = 'accepted'
        exists.save()

    return render(request, 'proposal_accepted.html', {'username':username, 'notif':notif})

def deny_proposal(request, username, pk):
    username = request.session['username']
    notif = Notification.objects.get(id=pk)
    exists = ProposalResponse.objects.get(notification=notif)

    if(request.method == 'POST'):
        exists.response = 'deny'
        exists.save()
        notif.delete()

    return render(request, 'proposal_denied.html', {'username':username, 'notif':notif})

@csrf_exempt
def payment(request, username, pk):
    # user_info = request.session.get('user_info')
    # book_details = request.session.get('book_details')
    username = request.session['username']
    user = Register.objects.get(username=username)
    print(user)
    notif = Notification.objects.get(user=user)
    print(notif)
    proposal = ProposalResponse.objects.get(notification=notif)

    try:
        print(username)
        # book_details = request.session.get('book_details')
        # # print(book_details)
        # chosen_book = request.session.get('chosen_book')
        # print(chosen_book)
        settings = { 'store_id': 'onlin64dd360da6a67', 'store_pass': 'onlin64dd360da6a67@ssl', 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = str(notif.post.price)
        post_body['currency'] = "BDT"
        post_body['tran_id'] = "1"
        post_body['success_url'] = f"http://127.0.0.1:8000/users/{username}/profile/payment/confirmed/"
        post_body['fail_url'] = "http://127.0.0.1:8000/"
        post_body['cancel_url'] = "http://127.0.0.1:8000/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = username
        post_body['cus_email'] = user.email
        post_body['cus_phone'] = '01711111111111'
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body) # API response
        # print(user_info)
        print(response)

        if(response['status'] == "SUCCESS"):
            proposal.paid = True
            proposal.save()
        return redirect(response['GatewayPageURL'])
    
    except:
        return render(request, 'manage.html', {"username":username, 'notif':notif, 'user':user})
    
@csrf_exempt
def confirm_pay(request, username):
    # username = request.session['username']
    return render(request, 'confirm_pay.html', {'username':username})
