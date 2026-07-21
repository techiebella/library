from datetime import date
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import request

from .models import (
    Book,
    Author,
    Category,
    Publisher,
    Student,
    IssuedBook,
)

from .forms import BookIssueForm


# ==========================
# HOME
# ==========================
def index(request):
    return render(request, "common/index.html")



# ==========================
# ADMIN LOGIN
# ==========================
def admin_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME =", username)
        print("PASSWORD =", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("AUTHENTICATED USER =", user)

        if user:

            print("IS SUPERUSER =", user.is_superuser)

            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            messages.error(request, "You are not an admin")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/admin_login.html")


# ==========================
# ADMIN DASHBOARD
# ==========================
@login_required(login_url="admin_login")
def admin_dashboard(request):

    return render(
        request,
        "admin/admin_dashboard.html"
    )



# ==========================
# LOGOUT
# ==========================
def Logout(request):

    logout(request)

    return redirect("index")



# ==========================
# ADD BOOK
# ==========================
@login_required(login_url="admin_login")
def add_book(request):

    if request.method == "POST":

        book_name = request.POST.get("book_name")
        author_name = request.POST.get("author")
        category_name = request.POST.get("category")
        isbn = request.POST.get("isbn")
        quantity = int(request.POST.get("quantity"))


        # Create author automatically
        author, created = Author.objects.get_or_create(
            name=author_name
        )


        # Create category automatically
        category, created = Category.objects.get_or_create(
            name=category_name
        )


        Book.objects.create(

            book_name=book_name,

            author=author,

            category=category,

            isbn=isbn,

            quantity=quantity,

            available_quantity=quantity,

            status="Available"
        )


        messages.success(
            request,
            "Book added successfully"
        )


        return redirect(
            "view_books"
        )


    return render(
        request,
        "admin/add_book.html"
    )



# ==========================
# VIEW BOOKS
# ==========================
@login_required(login_url="admin_login")
def view_books(request):

    books = Book.objects.all().order_by("-id")


    return render(
        request,
        "admin/view_book.html",
        {
            "books":books
        }
    )



# ==========================
# DELETE BOOK
# ==========================
@login_required(login_url="admin_login")
def delete_book(request,myid):

    book = get_object_or_404(
        Book,
        id=myid
    )

    book.delete()


    messages.success(
        request,
        "Book deleted successfully"
    )


    return redirect(
        "view_books"
    )



def student_registration(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        # Password check
        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect("student_registration")

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists. Please choose another username."
            )
            return redirect("student_registration")

        user = User.objects.create_user(
            username=username,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            password=password,
        )

        Student.objects.create(
            user=user,
            roll_no=request.POST.get("roll_no"),
            classroom=request.POST.get("classroom"),
            branch=request.POST.get("branch"),
            semester=request.POST.get("semester") or 1,
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            image=request.FILES.get("image"),
        )

        messages.success(
            request,
            "Registration successful"
        )

        return redirect("student_login")

    return render(
        request,
        "auth/student_registration.html"
    )


# ==========================
# STUDENT LOGIN
# ==========================
def student_login(request):

    if request.method=="POST":

        username=request.POST.get("username")

        password=request.POST.get("password")


        user=authenticate(

            request,

            username=username,

            password=password

        )


        if user:

            if user.is_superuser:

                messages.error(
                    request,
                    "Admin cannot login here"
                )

                return redirect(
                    "student_login"
                )


            login(
                request,
                user
            )


            return redirect(
                "profile"
            )


        messages.error(
            request,
            "Invalid login"
        )


    return render(
        request,
        "auth/student_login.html"
    )



# ==========================
# PROFILE
# ==========================
@login_required(login_url="student_login")
def profile(request):

    student=get_object_or_404(
        Student,
        user=request.user
    )


    return render(
        request,
        "student/profile.html",
        {
            "student":student
        }
    )



# ==========================
# ISSUE BOOK
# ==========================
@login_required(login_url="admin_login")
def issue_book(request):

    form=BookIssueForm(
        request.POST or None
    )


    if request.method=="POST":

        if form.is_valid():

            issued=form.save()

            book=issued.book


            if book.available_quantity > 0:

                book.available_quantity -= 1


                if book.available_quantity == 0:

                    book.status="Unavailable"


                book.save()


                messages.success(
                    request,
                    "Book issued successfully"
                )


                return redirect(
                    "view_issued_book"
                )


            messages.error(
                request,
                "Book unavailable"
            )


    return render(
        request,
        "admin/issue_book.html",
        {
            "form":form
        }
    )



# ==========================
# ISSUED BOOK LIST
# ==========================
@login_required(login_url="admin_login")
def view_issued_book(request):

    issued_books = IssuedBook.objects.all().order_by("-id")


    return render(
        request,
        "admin/view_issued_book.html",
        {
            "issued_books":issued_books
        }
    )



@login_required(login_url="admin_login")
def mark_as_returned(request, id):

    issued = get_object_or_404(
        IssuedBook,
        id=id
    )

    if not issued.return_date:
        issued.return_date = date.today()
        issued.save()

        book = issued.book

        if book.available_quantity < book.quantity:
            book.available_quantity += 1

        book.status = "Available"
        book.save()

    messages.success(request, "Book returned successfully")

    return redirect("view_issued_book")

# ==========================
# STUDENT ISSUED BOOKS
# ==========================
@login_required(login_url="student_login")
def student_issued_books(request):

    student = Student.objects.get(user=request.user)

    issued_books = IssuedBook.objects.filter(
        student=student
    )

    return render(
        request,
        "student/student_issued_books.html",
        {
            "issued_books": issued_books
        }
    )

# ==========================
# VIEW STUDENTS
# ==========================
@login_required(login_url="admin_login")
def view_students(request):

    students = Student.objects.select_related(
        "user"
    ).all().order_by("roll_no")


    return render(
        request,
        "admin/view_students.html",
        {
            "students": students
        }
    )



# ==========================
# DELETE STUDENT
# ==========================
@login_required(login_url="admin_login")
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    messages.success(
        request,
        "Student deleted successfully"
    )

    return redirect("view_students")

# ==========================
# EDIT PROFILE
# ==========================
@login_required(login_url="student_login")
def edit_profile(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )


    if request.method == "POST":

        # User details
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")

        request.user.save()


        # Student details
        student.roll_no = request.POST.get("roll_no")
        student.classroom = request.POST.get("classroom")
        student.branch = request.POST.get("branch")
        student.semester = request.POST.get("semester")
        student.phone = request.POST.get("phone")
        student.address = request.POST.get("address")


        if request.FILES.get("image"):

            student.image = request.FILES.get("image")


        student.save()


        messages.success(
            request,
            "Profile updated successfully"
        )


        return redirect(
            "profile"
        )


    return render(
        request,
        "student/edit_profile.html",
        {
            "student": student
        }
    )
@login_required(login_url="student_login")
def change_password(request):

    if request.method == "POST":

        old_password = request.POST.get(
            "current_password"
        )

        new_password = request.POST.get(
            "new_password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )


        if not request.user.check_password(old_password):

            messages.error(
                request,
                "Current password incorrect"
            )

            return redirect(
                "change_password"
            )


        if new_password != confirm_password:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect(
                "change_password"
            )


        request.user.set_password(
            new_password
        )

        request.user.save()


        logout(request)


        messages.success(
            request,
            "Password changed successfully"
        )


        return redirect(
            "student_login"
        )


    return render(
        request,
        "student/change_password.html"
    )

def update_issue_status(request, id):
    issue = get_object_or_404(IssuedBook, id=id)

    if request.method == "POST":
        status = request.POST.get("status")

        issue.status = status

        # If returned, set return date
        if status == "Returned":
            issue.return_date = date.today()

        else:
            issue.return_date = None

        issue.save()

    return redirect("view_issued_book")

def student_dashboard(request):

    total_books = Book.objects.count()

    issued_books = IssuedBook.objects.filter(
        student__user=request.user,
        status="Issued"
    ).count()


    fine = sum(
        book.fine 
        for book in IssuedBook.objects.filter(
            student__user=request.user
        )
    )


    context = {

        "total_books": total_books,
        "issued_books": issued_books,
        "fine": fine,

    }


    return render(
        request,
        "student/student_dashboard.html",
        context
    )

def student_view_books(request):

    books = Book.objects.all()

    query = request.GET.get("search")

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__name__icontains=query)
        )


    context = {
        "books": books
    }

    return render(
        request,
        "student/view_books.html",
        context
    )