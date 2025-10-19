from rest_framework import serializers
from product import models
from django.contrib.auth import get_user_model




class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = models.ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 
    class Meta:
        model = models.Product
        fields = ['id', 'name','images', 'slug','category', 'description', 'price','color', 'stock_status', 'brand', 'size', 'created_at', 'updated_at']
        read_only_fields = ['images', 'color','size']


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    class Meta:
        model = models.Review
        fields = [
            'id','ratings', 'comment','user'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return models.Review.objects.create(product_id=product_id, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name','slug','description','created_at']



class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = ['coupon_code','discount_type','discount_value','min_purchase_amount','expiry_date','Is_active']


