from django.contrib import admin
from .models import Register, Comment, DormRoom
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'nid')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Comment)
admin.site.register(DormRoom)