from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# -----------------------------
# Book Model
# -----------------------------
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField(unique=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="student_images/", blank=True)

    @property
    def student_id(self):
        # Using username as ID, you can change to roll_no if needed
        return self.user.username

    def __str__(self):
        return f"{self.user.username} [{self.branch}] [{self.classroom}]"


# -----------------------------
# Default expiry date
# -----------------------------
def default_expiry_date():
    return date.today() + timedelta(days=14)


# -----------------------------
# IssuedBook Model
# -----------------------------
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(default=default_expiry_date)
    return_date = models.DateField(null=True, blank=True)
    fine = models.PositiveIntegerField(default=0)

    def calculate_fine(self):
        if self.return_date:
            overdue_days = (self.return_date - self.expiry_date).days
        else:
            overdue_days = (date.today() - self.expiry_date).days

        if overdue_days > 0:
            self.fine = overdue_days * 5  # ₹5 per day
        else:
            self.fine = 0
        return self.fine

    def __str__(self):
        return f"{self.student.user.username} → {self.book.name}"
