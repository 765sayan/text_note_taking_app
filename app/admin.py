from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(User)
class useradmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'password']

@admin.register(Note)
class noteadmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'note']