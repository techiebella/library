from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # HOME
    # ==========================
    path("", views.index, name="index"),

    # ==========================
    # AUTHENTICATION
    # ==========================
    path("auth/admin_login/", views.admin_login, name="admin_login"),
    path("auth/student_login/", views.student_login, name="student_login"),
    path("auth/student_registration/", views.student_registration, name="student_registration"),
    path("auth/logout/", views.Logout, name="logout"),

    # ==========================
    # ADMIN DASHBOARD
    # ==========================
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Books
    path("dashboard/add_book/", views.add_book, name="add_book"),
    path("dashboard/view_books/", views.view_books, name="view_books"),
    path("dashboard/delete_book/<int:id>/", views.delete_book, name="delete_book"),

    # Students
    path("dashboard/view_students/", views.view_students, name="view_students"),
    path("dashboard/delete_student/<int:id>/", views.delete_student, name="delete_student"),

    # Book Issue
    path("dashboard/issue_book/", views.issue_book, name="issue_book"),
    path("dashboard/view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("dashboard/mark_returned/<int:id>/", views.mark_as_returned, name="mark_as_returned"),
    path("update_issue_status/<int:id>/",views.update_issue_status,name="update_issue_status"),

    # ==========================
    # STUDENT
    # ==========================
    path('student/dashboard/',views.student_dashboard,name='student_dashboard'),
    path("student/profile/", views.profile, name="profile"),
    path("student/edit_profile/", views.edit_profile, name="edit_profile"),
    path("student/change_password/", views.change_password, name="change_password"),
    path("student/issued_books/", views.student_issued_books, name="student_issued_books"),
    path("student/books/", views.student_view_books, name="student_view_books"),
]