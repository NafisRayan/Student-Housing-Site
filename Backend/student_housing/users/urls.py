from django.urls import path

from . import views

urlpatterns = [
    path("", views.users_intro, name="users_intro"),
    path("login/", views.users_login, name="users_login"),
    path("register/", views.users_register, name="users_register"),
    path("profile/<str:username>/", views.users_profile, name="users_profile"),
    path("<str:username>/create-post/", views.create_post, name="create_post"),
    path('<str:username>/posts/', views.show_posts, name='show_posts'),
    path('<str:username>/posts/own/', views.own_posts, name='own_posts'),
    path('<str:username>/posts/learn_more/<str:pk>', views.learn_more, name='learn_more'),
    path('<str:username>/posts/learn_more/<str:pk>/comment/', views.comment_dorm_room, name='comment_dorm_room'),
    path('<str:username>/posts/delete/<str:pk>', views.delete_post, name='delete_post'),
    path('<str:username>/posts/search/', views.search_res, name='search_res'),
    path('<str:username>/posts/bookmark-success/<str:pk>', views.bookmark_a_post, name='bookmark_a_post'),
    path('<str:username>/posts/bookmarked/', views.bookmarked, name='bookmarked'),
    path('<str:username>/posts/remove-bookmark-success/<str:pk>', views.remove_bookmark, name='remove_bookmark'),
    path('<str:username>/posts/search', views.search, name='search'),
    path('posts/sort', views.sort, name='sort'),
    path('<str:username>/posts/', views.show_posts, name='show_posts'),
    path('<str:username>/posts/proposal-sent/<str:pk>', views.send_rent_proposal, name='send_rent_proposal'),
    path('<str:username>/posts/proposal-unsent/<str:pk>', views.unsend_rent_proposal, name='unsend_rent_proposal'),
    path('<str:username>/posts/notifications', views.notifications, name='notifications'),
    path('<str:username>/posts/notifications/manage/<str:pk>', views.manage_proposal, name='manage_proposal'),
    path("logout/", views.users_logout, name="users_logout"),
    path('<str:username>/posts/send-email/<str:pk>', views.send_email_view, name='send_email_view'),
    path('<str:username>/posts/email-success', views.email_success, name='email_success'),
    path('<str:username>/profile/<str:pk>', views.show_posted_profile, name='show_posted_profile'),
   # path('users/posts/sendemailview', views.sendEmailPage, name='sendEmailPage'), 
   path('<str:username>/chat', views.group_chat, name='group_chat'),

]