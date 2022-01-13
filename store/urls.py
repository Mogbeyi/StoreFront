from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

#parent routers
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

#child routers
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='products-reviews')

urlpatterns = router.urls + products_router.urls
    
