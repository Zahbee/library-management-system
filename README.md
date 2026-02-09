
# Library Management System

This is a simple library management system built with Django. It allows users to register, log in, view available books, borrow books, and view their borrowed books. It also includes an admin dashboard for managing books.

## Features

*   User registration and login
*   View all available books
*   Borrow books
*   View borrowed books
*   Admin dashboard for adding and managing books

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/library-management-system.git
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd library-management-system
    ```

3.  **Install the dependencies:**

    Since there is no `requirements.txt` file, you will need to install Django.

    ```bash
    pip install Django
    ```

4.  **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Register a new user:**

    *   Go to `http://127.0.0.1:8000/register/`
    *   Fill in the registration form and click "Register"

2.  **Log in:**

    *   Go to `http://127.0.0.1:8000/login/`
    *   Enter your username and password and click "Login"

3.  **View available books:**

    *   After logging in, you will be redirected to the dashboard.
    *   Click on "All Books" to see a list of all available books.

4.  **Borrow a book:**

    *   From the "All Books" page, click the "Borrow" button next to the book you want to borrow.

5.  **View your borrowed books:**

    *   Click on "My Books" to see a list of the books you have borrowed.

6.  **Admin Dashboard:**

    *   Go to `http://127.0.0.1:8000/admin/`
    *   Log in with your superuser credentials.
    *   From the admin dashboard, you can add, edit, and delete books.

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.
