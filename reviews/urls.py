from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from reviews.views import ProductViewSet, ImageViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='Product')
router.register(r'image', ImageViewSet, basename='Image')

urlpatterns = [
    path('', include(router.urls)),
]
