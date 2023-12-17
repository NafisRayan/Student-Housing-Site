from django.contrib import admin
from .models import Register, Comment, DormRoom, Notification, Discussion, ProposalResponse
# Register your models here.

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'nid')

admin.site.register(Register, RegisterAdmin)
admin.site.register(Comment)
admin.site.register(DormRoom)
admin.site.register(Notification)
admin.site.register(Discussion)
admin.site.register(ProposalResponse)