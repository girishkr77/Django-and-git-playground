from django.contrib import admin,messages
from store import models
from django.urls import reverse
from django.utils.html import format_html, urlencode
from store.models import Product,Collection,Order,Customer
from django.db.models.aggregates import Count
from tags.models import TaggedItem

class inventory_filter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<5','Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<5':
            return queryset.filter(inventory__lt=5)
    



@admin.register(models.Product)
class productAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title']
    }
    exclude = ['promotioms']
    actions = ['clear_inventory']
    list_display = ['title','price','inventry_status','collection']
    list_editable = ['price']
    list_per_page = 15
    list_filter = ['collection','last_updated',inventory_filter]
    search_fields = ['product']

    @admin.display(ordering='inventory')
    def inventry_status(self,Product):
        if Product.inventory  < 5:
            return 'low'
        return 'ok'
    
    @admin.action(description='clear inventory')
    def clear_inventory(self,request, queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated'
        )


@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self,Collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id' : str(Collection.id)
            }))
        return format_html('<a href = "{}">{}</a>',url, Collection.product_count)
 
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count = Count('products'))

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['first_name','Last_name','member_ship','orders_count']
    list_editable = ['member_ship']
    list_per_page = 10
    ordering = ['first_name','Last_name']
    search_fields = ['first_name__istartswith','Last_name__istartswith']
    
    @admin.display(ordering='orders_count')
    def orders_count(self,Customer):
        return str(Customer.orders_count) + (' ') + 'orders'
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count = Count('order'))

class orderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    


@admin.register(Order)
class orderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [orderItemInline]
    list_display = ['payment_status','placed_at','customer']
    
