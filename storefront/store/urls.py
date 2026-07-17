from . import views
from django.urls import path
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register(r'products',views.ProductViewSet,basename='products')
router.register(r'collections',views.CollectionViewSet)
router.register(r'carts',views.Cartsetview,basename='carts')
router.register(r'profiles',views.Customerviewset,basename='profiles')
router.register(r'orders',views.OrderViewset,basename='orders')

product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartitemViewset,basename='cart-item')

urlpatterns = router.urls + product_router.urls + cart_router.urls

