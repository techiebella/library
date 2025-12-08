from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Book, Student, IssuedBook
from .forms import IssueBookForm


# -----------------------------
# HOME PAGE
# -----------------------------
def index(request):
    return render(request, "index.html")


# ======================
# ADMIN VIEWS
# ======================

@login_required(login_url='/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        author = request.POST.get('author', '').strip()
        isbn = request.POST.get('isbn', '').strip()
        category = request.POST.get('category', '').strip()

        if name and author and isbn and category:
            Book.objects.create(name=name, author=author, isbn=isbn, category=category)
            return render(request, "add_book.html", {'alert': True})

    return render(request, "add_book.html")


@login_required(login_url='/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_book.html", {'books': books})


@login_required(login_url='/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students': students})


@login_required(login_url='/admin_login')
def issue_book(request):
    form = IssueBookForm()
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['name2']  # Student object
            book = form.cleaned_data['isbn2']     # Book object
            IssuedBook.objects.create(student=student, book=book)
            return render(request, "issue_book.html", {'form': IssueBookForm(), 'alert': True})

    return render(request, "issue_book.html", {'form': form})


@login_required(login_url='/admin_login')
def view_issued_book(request):
    issued_books = IssuedBook.objects.all()
    details = []

    for issued in issued_books:
        days = (date.today() - issued.issue_date).days
        fine = max(0, (days - 14) * 5)

        details.append((
            issued.student.user.username,     # i.0
            issued.student.id,                # i.1
            issued.book.name,                 # i.2
            issued.book.isbn,                 # i.3
            issued.issue_date,                # i.4
            issued.expiry_date,               # i.5
            fine,                             # i.6
            issued.id                         # i.7 → Delete ID
        ))

    return render(request, "view_issued_book.html", {'details': details})


@login_required(login_url='/admin_login')
def delete_book(request, myid):
    Book.objects.filter(id=myid).delete()
    return redirect("/view_book")


@login_required(login_url='/admin_login')
def delete_student(request, myid):
    Student.objects.filter(id=myid).delete()
    return redirect("/view_students")


@login_required(login_url='/admin_login')
def delete_issue(request, myid):
    issued_book = get_object_or_404(IssuedBook, id=myid)
    issued_book.delete()
    return redirect('view_issued_book')


# ======================
# STUDENT VIEWS
# ======================
@login_required(login_url='/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id).first()
    issued_books = IssuedBook.objects.filter(student=student) if student else []

    li1, li2 = [], []

    for issued in issued_books:
        li1.append((
            request.user.id,
            request.user.get_full_name(),
            issued.book.name,
            issued.book.author
        ))

        days = (date.today() - issued.issue_date).days
        fine = max(0, (days - 14) * 5)
        li2.append((issued.issue_date, issued.expiry_date, fine))

    issued_details = zip(li1, li2)

    return render(request, 'student_issued_books.html', {'issued_details': issued_details})
@login_required(login_url='/student_login')
def profile(request):
    return render(request, "profile.html")


@login_required(login_url='/student_login')
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        student.user.email = request.POST.get('email', student.user.email)
        student.phone = request.POST.get('phone', student.phone)
        student.branch = request.POST.get('branch', student.branch)
        student.classroom = request.POST.get('classroom', student.classroom)
        student.roll_no = request.POST.get('roll_no', student.roll_no)

        student.user.save()
        student.save()
        return render(request, "edit_profile.html", {'alert': True})

    return render(request, "edit_profile.html", {'student': student})


@login_required(login_url='/student_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return render(request, "change_password.html", {'alert': True})
        else:
            return render(request, "change_password.html", {'currpasswrong': True})

    return render(request, "change_password.html")


# ======================
# AUTH VIEWS
# ======================

def student_registration(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        branch = request.POST.get('branch', '').strip()
        classroom = request.POST.get('classroom', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        image = request.FILES.get('image')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if password != confirm_password:
            return render(request, "student_registration.html", {'passnotmatch': True})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Student.objects.create(
            user=user,
            phone=phone,
            branch=branch,
            classroom=classroom,
            roll_no=roll_no,
            image=image
        )

        return render(request, "student_registration.html", {'alert': True})

    return render(request, "student_registration.html")


def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            return render(request, "student_login.html", {'alert': True})

    return render(request, "student_login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            return render(request, "admin_login.html", {'alert': True})

    return render(request, "admin_login.html")


def Logout(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/admin_login')
def mark_as_returned(request, myid):
    issued_book = get_object_or_404(IssuedBook, id=myid)
    issued_book.delete()  # This will remove the record when returned
    return redirect('view_issued_book')
