from django.urls import path,include
from product import views as productviews
from order import views as orderviews
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', productviews.AllProductViewSet, basename='products')
router.register('categories', productviews.CategoryViewSet, basename='product-category')
router.register('carts',orderviews.CartViewset, basename='carts')


product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', productviews.ReviewViewSet, basename='product-review')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', orderviews.CartItemViewSet, basename='cart-item')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls))
]
