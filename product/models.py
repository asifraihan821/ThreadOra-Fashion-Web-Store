from django.db import models
from django.utils.text import slugify
from django.conf import settings
from .validators import validate_file_size
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.

                        #Model --> Category

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, unique=True,blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}"
    
    
                        # Model --> Product

class Product(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('STOCK_OUT', 'Stock Out'),
        ('NOT_AVAILABLE', 'Not Available')
    ]
    SIZE_CHOICES = [
        ('SMALL', 'S'),
        ('MEDIUM', 'M'),
        ('LARGE', 'L'),
        ('XTRA_LARGE', 'XL'),
        ('DOUBLE_EXTRA_LARGE', 'XXL')
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveBigIntegerField()
    stock_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=200,blank=True, null=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True, null=True)
    color = models. CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


                        #Model --> ProductImage

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    


                        #Model --> Review

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"reviewed by{self.user.first_name} on {self.product.name}"
    
    
                        #Model --> Discount

class Discount(models.Model):
    DISCOUNT_CHOICES = [
        ('PERCENTEAGE', 'Parcentage'),
        ('FIXED', 'Fixed'),
    ]
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField()
    Is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.coupon_code} - {self.discount_value}"
    
    def is_valid(self):
        "check if coupon is still valid"
        from django.utils import timezone
        return self.Is_active and self.expiry_date > timezone.now()