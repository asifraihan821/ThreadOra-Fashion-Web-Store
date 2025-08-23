from django.shortcuts import render
from order import serializers,models
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,CreateModelMixin,ListModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CartViewset(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet,ListModelMixin):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Cart.filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])