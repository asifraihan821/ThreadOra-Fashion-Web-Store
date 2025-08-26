from rest_framework.viewsets import ModelViewSet
from product import models
from product import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from product.permissions import IsReviewAuthorOrReadOnly
# Create your views here.

class AllProductViewSet(ModelViewSet):
    """for viewing all the products 
     - only admin can view,delete,update products
     """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination
    filterset_fields = ['category', 'color','size']
    search_fields = ['slug','name','brand', 'price']
    ordering_fields = ['price',]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
        
class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return models.Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return {'product_id':self.kwargs['product_pk']}
    

class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]



class ProductImageViewSet(ModelViewSet):
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return models.ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
    
    def perform_create(self, serializer):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        serializer.save(product_id = self.kwargs['product_pk'])    ##id pathailam jno not null constraint na dei