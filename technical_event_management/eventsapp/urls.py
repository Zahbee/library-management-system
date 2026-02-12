from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # auth
    path('register/', views.register_choice, name='register_choice'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # vendor
    path('vendor/', views.vendor_main, name='vendor_main'),
    path('vendor/items/', views.your_items, name='your_items'),
    path('vendor/items/add/', views.add_item, name='add_item'),
    path('vendor/items/view/', views.view_products, name='view_products'),
    path('vendor/items/status/', views.product_status, name='product_status'),

    # user
    path('user/', views.user_main, name='user_main'),
    path('user/vendors/', views.vendor_list, name='vendor_list'),
    path('user/vendors/<str:category>/shop/<int:vendor_id>/', views.shop_items, name='shop_items'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_status, name='order_status'),
    path('guestlist/', views.guest_list, name='guest_list'),

    # admin
    path('admin-dashboard/', views.admin_main, name='admin_main'),
    #delete
    path('vendor/items/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('vendor/membership/', views.vendor_membership, name='vendor_membership'),
    path('admin-dashboard/', views.admin_main, name='admin_main'),
    path('admin-dashboard/users/', views.manage_users, name='manage_users'),
    path('admin-dashboard/vendors/', views.manage_vendors, name='manage_vendors'),
    path('user/membership/', views.user_membership, name='user_membership'),
]