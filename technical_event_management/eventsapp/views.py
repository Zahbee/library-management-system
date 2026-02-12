from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, VendorRegisterForm, VendorProductForm, CheckoutForm
from .models import CustomUser, VendorProduct, CartItem, Order, OrderItem, Guest
from django.utils import timezone
from decimal import Decimal

# role-check decorators
from functools import wraps

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role != role:
                messages.error(request, 'Access denied.')
                return redirect('/')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

# index / landing

def index(request):
    return render(request, 'index.html')

# registration choice

def register_choice(request):
    return render(request, 'registration/register.html')

# user register

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'USER'
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'type': 'user'})

# vendor register

def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'VENDOR'
            user.vendor_category = form.cleaned_data.get('vendor_category')
            user.save()
            messages.success(request, 'Vendor registered. Please login.')
            return redirect('login')
    else:
        form = VendorRegisterForm()
    return render(request, 'registration/register.html', {'form': form, 'type': 'vendor'})

# custom login view (wrap built-in auth)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # redirect based on role
            if user.role == 'VENDOR':
                return redirect('vendor_main')
            elif user.role == 'ADMIN':
                return redirect('admin_main')
            else:
                return redirect('user_main')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    return redirect('index')

# vendor views

@role_required('VENDOR')
def vendor_main(request):
    return render(request, 'vendor/vendor_main.html')

@role_required('VENDOR')
def your_items(request):
    products = VendorProduct.objects.filter(vendor=request.user)
    return render(request, 'vendor/your_items.html', {'products': products})

@role_required('VENDOR')
def add_item(request):
    if request.method == 'POST':
        form = VendorProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.vendor = request.user
            prod.save()
            messages.success(request, 'Product added')
            return redirect('your_items')
    else:
        form = VendorProductForm()
    return render(request, 'vendor/add_item.html', {'form': form})

@role_required('VENDOR')
def view_products(request):
    products = VendorProduct.objects.filter(vendor=request.user)
    return render(request, 'vendor/view_products.html', {'products': products})

@role_required('VENDOR')
def product_status(request):

    # get all order items belonging to this vendor
    order_items = OrderItem.objects.filter(vendor=request.user)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        status = request.POST.get('status')

        item = get_object_or_404(OrderItem, id=item_id, vendor=request.user)
        item.status = status
        item.save()

        messages.success(request, "Order item status updated")
        return redirect('product_status')

    return render(request, 'vendor/product_status.html', {
        'order_items': order_items
    })


# user views

@role_required('USER')
def user_main(request):
    return render(request, 'user/user_main.html')

@role_required('USER')
def vendor_list(request):
    category = request.GET.get('category')
    vendors = None
    if category:
        vendors = CustomUser.objects.filter(role='VENDOR', vendor_category=category)
    return render(request, 'user/vendor_list.html', {'vendors': vendors})

@role_required('USER')
def shop_items(request, category, vendor_id):
    vendor = get_object_or_404(CustomUser, id=vendor_id, role='VENDOR')
    products = VendorProduct.objects.filter(vendor=vendor)
    return render(request, 'user/shop_items.html', {'products': products, 'vendor': vendor})

@role_required('USER')
def add_to_cart(request, product_id):
    product = get_object_or_404(VendorProduct, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Added to cart')
    return redirect('cart')

@role_required('USER')
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum([item.line_total() for item in items])
    return render(request, 'user/cart.html', {'items': items, 'total': total})

@role_required('USER')
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@role_required('USER')
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.error(request, 'Cart is empty')
        return redirect('user_main')
    total = sum([item.line_total() for item in items])
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total=Decimal(total),
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pin_code=form.cleaned_data['pin_code'],
                phone=form.cleaned_data['phone'],
                payment_method=form.cleaned_data['payment_method'],
            )
            # create order items
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    vendor=item.product.vendor,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                # reduce product stock
                if item.product.quantity >= item.quantity:
                    item.product.quantity -= item.quantity
                    item.product.save()
            items.delete()
            messages.success(request, 'Order placed successfully')
            return render(request, 'user/checkout.html', {'order': order, 'success': True})
    else:
        form = CheckoutForm(initial={'name':request.user.username, 'email':request.user.email})
    return render(request, 'user/checkout.html', {'items':items, 'total':total, 'form':form})

@role_required('USER')
def order_status(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user/order_status.html', {'orders': orders})

@role_required('USER')
def guest_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        Guest.objects.create(user=request.user, name=name, phone=phone, email=email)
        return redirect('guest_list')
    guests = Guest.objects.filter(user=request.user)
    return render(request, 'user/guest_list.html', {'guests': guests})


@role_required('USER')
def user_membership(request):

    if request.method == "POST":

        if request.POST.get("cancel"):
            request.user.membership_expiry = timezone.now()

        else:
            membership = request.POST.get("membership")
            request.user.membership = membership
            request.user.membership_expiry = None  # auto recalculated in save()

        request.user.save()
        return redirect("user_membership")

    return render(request, "user/membership.html")


# admin views

@role_required('ADMIN')
def admin_main(request):

    users = CustomUser.objects.filter(role='USER')
    vendors = CustomUser.objects.filter(role='VENDOR')

    active_users = users.filter(membership_expiry__gt=timezone.now())
    expired_users = users.filter(membership_expiry__lt=timezone.now())

    active_vendors = vendors.filter(membership_expiry__gt=timezone.now())
    expired_vendors = vendors.filter(membership_expiry__lt=timezone.now())

    return render(request, 'admin/admin_main.html', {
        'users': users,
        'vendors': vendors,
        'active_users': active_users,
        'expired_users': expired_users,
        'active_vendors': active_vendors,
        'expired_vendors': expired_vendors,
    })

@role_required('ADMIN')
def manage_users(request):

    users = CustomUser.objects.filter(role='USER')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user = get_object_or_404(CustomUser, id=user_id, role='USER')

        if action == 'cancel':
            user.membership_expiry = timezone.now()
        elif action == 'extend_6m':
            user.membership_expiry = timezone.now() + timedelta(days=180)
        elif action == 'extend_1y':
            user.membership_expiry = timezone.now() + timedelta(days=365)

        user.save()
        messages.success(request, "Membership updated")
        return redirect('manage_users')

    return render(request, 'admin/manage_users.html', {'users': users})


@role_required('ADMIN')
def manage_vendors(request):

    vendors = CustomUser.objects.filter(role='VENDOR')

    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id')
        action = request.POST.get('action')

        vendor = get_object_or_404(CustomUser, id=vendor_id, role='VENDOR')

        if action == 'cancel':
            vendor.membership_expiry = timezone.now()
        elif action == 'extend_6m':
            vendor.membership_expiry = timezone.now() + timedelta(days=180)
        elif action == 'extend_1y':
            vendor.membership_expiry = timezone.now() + timedelta(days=365)

        vendor.save()
        messages.success(request, "Vendor membership updated")
        return redirect('manage_vendors')

    return render(request, 'admin/manage_vendors.html', {'vendors': vendors})




@role_required('VENDOR')
def delete_product(request, product_id):
    product = get_object_or_404(VendorProduct, id=product_id, vendor=request.user)
    product.delete()
    messages.success(request, "Product deleted")
    return redirect('your_items')


@role_required('VENDOR')
def vendor_membership(request):
    if request.method == 'POST':
        membership = request.POST.get('membership')
        request.user.membership = membership
        request.user.membership_expiry = None  # will auto update in save()
        request.user.save()
        messages.success(request, "Membership updated")
        return redirect('vendor_main')
    return render(request, 'vendor/membership.html')


