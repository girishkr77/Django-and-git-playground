from . import views
from django.urls import path
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register(r'products',views.ProductViewSet,basename='products')
router.register(r'collections',views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

urlpatterns = router.urls + product_router.urls

