from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from library_app.models import (
    Book,
    Student,
    Category,
    Author,
    Publisher,
    IssuedBook
)


class Command(BaseCommand):

    help = "Delete all library data"

    def handle(self, *args, **kwargs):

        IssuedBook.objects.all().delete()
        Book.objects.all().delete()
        Student.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

        # Delete all users except admin
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(
            self.style.SUCCESS(
                "Database cleared successfully!"
            )
        )