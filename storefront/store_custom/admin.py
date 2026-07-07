from django.contrib import admin
from store.admin import productAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline


class taginline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class customproductAdmin(productAdmin):
    inlines = [taginline]

admin.site.unregister(Product)
admin.site.register(Product,customproductAdmin)
