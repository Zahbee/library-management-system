from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('VENDOR', 'Vendor'),
        ('ADMIN', 'Admin'),
    )
    MEMBERSHIP_CHOICES = (
        ('6m', '6 months'),
        ('1y', '1 year'),
        ('2y', '2 years'),
    )
    VENDOR_CATEGORY = (
        ('catering', 'Catering'),
        ('florist', 'Florist'),
        ('decoration', 'Decoration'),
        ('lighting', 'Lighting'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    # vendor-only fields
    vendor_category = models.CharField(max_length=20, choices=VENDOR_CATEGORY, blank=True, null=True)
    membership = models.CharField(max_length=2, choices=MEMBERSHIP_CHOICES, default='6m')
    membership_expiry = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # set expiry based on membership (if not already set or membership changed)
        if self.membership and not self.membership_expiry:
            if self.membership == '6m':
                self.membership_expiry = timezone.now() + timedelta(days=30*6)
            elif self.membership == '1y':
                self.membership_expiry = timezone.now() + timedelta(days=365)
            elif self.membership == '2y':
                self.membership_expiry = timezone.now() + timedelta(days=365*2)
        super().save(*args, **kwargs)

class VendorProduct(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('ready', 'Ready for Shipping'),
        ('out', 'Out For Delivery'),
    )
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'VENDOR'})
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.vendor.username}"

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'USER'})
    product = models.ForeignKey(VendorProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def line_total(self):
        return self.quantity * self.product.price

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('upi','UPI'),
        ('cash','Cash'),
    )
    STATUS = (
        ('placed','Placed'),
        ('processing','Processing'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):

    STATUS_CHOICES = (
        ('received', 'Received'),
        ('ready', 'Ready for Shipping'),
        ('out', 'Out For Delivery'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(VendorProduct, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='vendor_orders')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )


class Guest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'USER'})
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)