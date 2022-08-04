from django.contrib import admin
from .models import *

# Register your models here.
class SharpeAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio', 'security')

admin.site.register(Client)
admin.site.register(Portfolio)
admin.site.register(Security)
#admin.site.register(User)