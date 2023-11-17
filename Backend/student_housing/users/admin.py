from django.contrib import admin
from .models import Register, DormRoom, Comment
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'nid')

admin.site.register(Register, RegisterAdmin)
admin.site.register(DormRoom)
admin.site.register(Comment)