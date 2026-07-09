from . import views
from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter


router = SimpleRouter()
router.register(r'products',views.ProductViewSet)
router.register(r'collections',views.CollectionViewSet)
urlpatterns = router.urls

