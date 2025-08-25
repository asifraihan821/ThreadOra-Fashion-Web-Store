from rest_framework import serializers
from order import models
from product.models import Product
from product.serializers import ProductSerializer
from order.services import OrderService



class EmptySerializer(serializers.Serializer):
    pass

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product_id', 'quantity']
    


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = models.CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except models.CartItem.DoesNotExist:
            self.instance = models.CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance
    
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'product with id {value} does not exist')
        
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'product','total_price']

    def get_total_price(self,cart_item):
        return cart_item.quantity * cart_item.product.price
    


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = models.Cart
        fields = ['id', 'user','items', 'total_price']
        read_only_fields = ['user']
    
    def get_total_price(self,cart):
       return sum([item.product.price*item.quantity for item in cart.items.all()])


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not models.Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')
        if not models.CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = OrderService.create_order(user_id=user_id,cart_id=cart_id)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['status']

    # def update(self, instance, validated_data):
    #     user = self.context['user']
    #     new_status = validated_data['status']

    #     print(validated_data)
    #     print(new_status)

    #     if new_status == models.Order.CANCELLED:
    #         return OrderService.cancel_order(order=instance,user=user)
    #     #admn hoile
    #     if not user.is_staff:
    #         raise serializers.ValidationError({'detail': 'you cannot cancel an order'})
        
    #     return super().update(instance, validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = models.Order
        fields = ['id','user', 'status', 'total_price', 'created_at', 'items']