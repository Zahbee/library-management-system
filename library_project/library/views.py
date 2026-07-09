from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, Borrow
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.user.is_staff:
        total_books = Book.objects.count()
        total_users = User.objects.count()
        total_borrowed = Borrow.objects.filter(status="Borrowed").count()

        context = {
            'total_books': total_books,
            'total_users': total_users,
            'total_borrowed': total_borrowed
        }

        return render(request, 'admin_dashboard.html', context)

    else:
        borrowed_count = Borrow.objects.filter(user=request.user, status="Borrowed").count()

        context = {
            'borrowed_count': borrowed_count
        }

        return render(request, 'user_dashboard.html', context)



def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def book_list(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'books.html', {'books': books})




@staff_member_required
def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        quantity = int(request.POST['quantity'])

        Book.objects.create(
            title=title,
            author=author,
            total_quantity=quantity,
            available_quantity=quantity
        )
        return redirect('books')

    return render(request, 'add_book.html')

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Prevent duplicate borrow
    already_borrowed = Borrow.objects.filter(
        user=request.user,
        book=book,
        status="Borrowed"
    ).exists()

    if already_borrowed:
        messages.error(request, "You already borrowed this book.")
        return redirect('books')

    if book.available_quantity > 0:
        now = timezone.now()
        due = now + timedelta(days=7)

        # Explicitly set borrow_date to ensure timestamp exists
        Borrow.objects.create(
            user=request.user,
            book=book,
            due_date=due,
            status="Borrowed"
        )

        book.available_quantity -= 1
        book.save()

        messages.success(request, "Book borrowed successfully!")
    else:
        messages.error(request, "Book not available.")

    return redirect('books')




@login_required
def my_books(request):
    borrowed_books = Borrow.objects.filter(user=request.user, status="Borrowed")
    return render(request, 'my_books.html', {'borrowed_books': borrowed_books})


@login_required
def return_book(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id, user=request.user)

    if borrow.status == "Borrowed":
        borrow.status = "Returned"
        borrow.return_date = timezone.now()
        borrow.save()

        book = borrow.book
        book.available_quantity += 1
        book.save()

    return redirect('my_books')
