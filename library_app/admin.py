from django.contrib import admin

from .models import (
    Category,
    Author,
    Publisher,
    Book,
    Student,
    IssuedBook,
    Reservation,
    Review,
    Notification,
    ActivityLog,
)


# =====================================================
# CATEGORY
# =====================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )



# =====================================================
# AUTHOR
# =====================================================
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )



# =====================================================
# PUBLISHER
# =====================================================
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "website",
    )

    search_fields = (
        "name",
    )



# =====================================================
# BOOK
# =====================================================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "book_name",
        "author",
        "category",
        "publisher",
        "isbn",
        "quantity",
        "available_quantity",
        "status",
    )


    search_fields = (
        "book_name",
        "isbn",
        "author__name",
    )


    list_filter = (
        "category",
        "publisher",
        "status",
        "language",
    )


    ordering = (
        "book_name",
    )



# =====================================================
# STUDENT
# =====================================================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "roll_no",
        "user",
        "branch",
        "semester",
        "phone",
        "active",
    )


    search_fields = (
        "roll_no",
        "user__username",
        "user__first_name",
        "user__last_name",
    )


    list_filter = (
        "branch",
        "semester",
        "active",
    )



# =====================================================
# ISSUED BOOK
# =====================================================
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "book",
        "issue_date",
        "due_date",
        "return_date",
        "fine",
        "status",
    )


    list_filter = (
        "status",
        "issue_date",
        "due_date",
    )


    search_fields = (
        "student__roll_no",
        "student__user__username",
        "book__book_name",
    )



# =====================================================
# RESERVATION
# =====================================================
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "book",
        "reserved_on",
        "status",
    )


    list_filter = (
        "status",
    )


    search_fields = (
        "student__roll_no",
        "book__book_name",
    )



# =====================================================
# REVIEW
# =====================================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "book",
        "rating",
        "created_at",
    )


    list_filter = (
        "rating",
    )


    search_fields = (
        "book__book_name",
        "student__roll_no",
    )



# =====================================================
# NOTIFICATION
# =====================================================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "student",
        "message",
        "is_read",
        "created_at",
    )


    list_filter = (
        "is_read",
    )



# =====================================================
# ACTIVITY LOG
# =====================================================
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "action",
        "created_at",
    )


    search_fields = (
        "user__username",
        "action",
    )