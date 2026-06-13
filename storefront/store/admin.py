from django.contrib import admin
from store import models

# Register your models here.
@admin.register(models.Product)
class productAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    list_editable = ['price']
    list_per_page = 15

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title','id']

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['first_name','Last_name','member_ship']
    list_editable = ['member_ship']
    list_per_page = 10
    ordering = ['first_name','Last_name']
