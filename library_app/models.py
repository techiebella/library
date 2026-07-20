from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User


# =====================================================
# CATEGORY MODEL
# =====================================================
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



# =====================================================
# AUTHOR MODEL
# =====================================================
class Author(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True
    )

    biography = models.TextField(
        blank=True,
        null=True
    )

    photo = models.ImageField(
        upload_to="authors/",
        blank=True,
        null=True
    )


    def __str__(self):
        return self.name



# =====================================================
# PUBLISHER MODEL
# =====================================================
class Publisher(models.Model):

    name = models.CharField(
        max_length=150
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )


    def __str__(self):
        return self.name



# =====================================================
# BOOK MODEL
# =====================================================
class Book(models.Model):

    # matches form field book_name
    book_name = models.CharField(
        max_length=250
    )


    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )


    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    isbn = models.CharField(
        max_length=20,
        unique=True
    )


    edition = models.CharField(
        max_length=50,
        blank=True
    )


    language = models.CharField(
        max_length=50,
        default="English"
    )


    description = models.TextField(
        blank=True,
        null=True
    )


    cover_image = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True
    )


    pdf = models.FileField(
        upload_to="books/pdf/",
        blank=True,
        null=True
    )


    shelf_number = models.CharField(
        max_length=30,
        blank=True
    )


    quantity = models.PositiveIntegerField(
        default=1
    )


    available_quantity = models.PositiveIntegerField(
        default=1
    )


    STATUS = (
        ("Available","Available"),
        ("Unavailable","Unavailable"),
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Available"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.book_name



# =====================================================
# STUDENT MODEL
# =====================================================
class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    roll_no = models.CharField(
        max_length=30,
        unique=True
    )


    classroom = models.CharField(
        max_length=20
    )


    branch = models.CharField(
        max_length=50
    )


    semester = models.PositiveIntegerField(
        default=1
    )


    phone = models.CharField(
        max_length=15
    )


    address = models.TextField(
        blank=True,
        null=True
    )


    image = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )


    admission_date = models.DateField(
        auto_now_add=True
    )


    active = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.user.username} ({self.roll_no})"



# =====================================================
# ISSUE BOOK MODEL
# =====================================================
def default_due_date():
    return timezone.now().date() + timedelta(days=7)



class IssuedBook(models.Model):

    STATUS = (
        ("Issued","Issued"),
        ("Returned","Returned"),
        ("Overdue","Overdue"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    issue_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField(
        default=default_due_date
    )

    return_date = models.DateField(
        null=True,
        blank=True
    )

    fine = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Issued"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def calculate_fine(self):

        today = self.return_date or date.today()

        days = (today - self.due_date).days

        if days > 0:
            return days * 5

        return 0



    def save(self,*args,**kwargs):

        self.fine = self.calculate_fine()


        if self.return_date:
            self.status = "Returned"

        elif date.today() > self.due_date:
            self.status = "Overdue"


        super().save(*args,**kwargs)



    def __str__(self):
        return f"{self.student} → {self.book}"



# =====================================================
# RESERVATION MODEL
# =====================================================
class Reservation(models.Model):

    STATUS = (
        ("Pending","Pending"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled"),
    )


    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )


    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )


    reserved_on = models.DateTimeField(
        auto_now_add=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )



# =====================================================
# REVIEW MODEL
# =====================================================
class Review(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )


    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )


    rating = models.PositiveSmallIntegerField(
        default=5
    )


    comment = models.TextField(
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



# =====================================================
# NOTIFICATION MODEL
# =====================================================
class Notification(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )


    message = models.TextField()


    is_read = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



# =====================================================
# ACTIVITY LOG
# =====================================================
class ActivityLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    action = models.CharField(
        max_length=255
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )