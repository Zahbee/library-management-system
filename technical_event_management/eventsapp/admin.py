from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VendorProduct, CartItem, Order, OrderItem, Guest

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username','email','role','vendor_category','membership','membership_expiry']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields':('role','vendor_category','membership','membership_expiry')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VendorProduct)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Guest)