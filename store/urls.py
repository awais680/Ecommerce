from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import categoryviewset,productviewset,orderviewset,cartviewset

router = DefaultRouter()
router.register('categories',categoryviewset,basename='category')
router.register('products',productviewset,basename='product')
router.register('carts',cartviewset,basename='cart')
router.register('orders',orderviewset,basename='order')

urlpatterns = router.urls