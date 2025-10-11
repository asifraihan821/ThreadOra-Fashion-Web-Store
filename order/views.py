from order import serializers,models
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,CreateModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from order.services import OrderService
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet,ListModelMixin):
    """"Creating cart for the user who is selecting his products to order"""
    
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary = "user saves with new create object"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    def perform_create(self, serializer):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return models.Cart.objects.prefetch_related('items__product').filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    """for clothes which are selected by the user in the cart """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch', 'delete']

    @swagger_auto_schema(
            operation_summary="" \
            "inside the carts of products that selected by the user"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return models.CartItem.objects.select_related('product').filter(cart_id = self.kwargs['cart_pk'])
    


class OrderViewSet(ModelViewSet):

    http_method_names = ['get','post','delete','patch','head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self,request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status':'your order cancelled'})

    @action(detail=True, methods=['patch'])
    def update_status(self,request, pk=None):
        order = self.get_object()
        serializer = serializers.OrderUpdateSerializer(order,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Order status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ['update_status','destroy']:
            return[IsAdminUser()]
        return [IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.action == 'cancel':
            return serializers.EmptySerializer
        if self.action == 'create':
            return serializers.CreateOrderSerializer
        elif self.action == 'update_status':
            return serializers.OrderUpdateSerializer
        return serializers.OrderSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return {'user_id': self.request.user.id, 'user':self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        if self.request.user.is_staff:
            return models.Order.objects.prefetch_related('items__product').all()
        return models.Order.objects.prefetch_related('items__product').filter(user=self.request.user)