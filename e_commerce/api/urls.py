from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,CartViewSet,ProductViewSet,CartItemViewSet

router = DefaultRouter()
router.register(r'categories',CategoryViewSet,basename='cart')
router.register(r'carts',CartViewSet)
router.register(r'products',ProductViewSet)
router.register(r'cartitems',CartItemViewSet,basename='cartitem')

urlpatterns = [
    path('',include,(router.urls))
]