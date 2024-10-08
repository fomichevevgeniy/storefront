from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
# urlpatterns = [
#     path('product_list/', ProductList.as_view(), name='product-list'),
#     path('product_detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
#     path('collection_list/', CollectionList.as_view(), name='collection-list'),
#     path('collection_detail/<int:pk>/', CollectionDetail.as_view(), name='collection-detail')
# ]

router = routers.DefaultRouter()

router.register('collections', CollectionViewSet, basename='collections')
router.register('products', ProductViewSet, basename='products')
router.register('carts', CartViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')  # product_pk
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls

# 4f1cdba4-ac23-482c-99cf-28e53c40e3d6
