from django.contrib import admin
from .models import Register, DormRooms
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'nid')

admin.site.register(Register, RegisterAdmin)

class DormRoomsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'content', 'popularity', 'type', 'price', 'link')



admin.site.register(DormRooms)