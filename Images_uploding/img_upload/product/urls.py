from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.urls.conf import include
from product import views
from product.views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Product', ProductViewSet, basename='Product')

urlpatterns = [
    path('', views.ima_upload, name="product"),
    path('img/', include(router.urls))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)