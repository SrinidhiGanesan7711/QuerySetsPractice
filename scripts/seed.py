import os
import sys
import django

# Point to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "querysets.settings")
django.setup()

# Now it's safe to import models
from books.models import Book, Author


def run():
    # Clear existing data
    Book.objects.all().delete()
    Author.objects.all().delete()

    # Create authors
    a1 = Author.objects.create(name="Alice Walker", birth_year=1944)
    a2 = Author.objects.create(name="George Orwell", birth_year=1903)

    # Create books
    Book.objects.create(title="The Color Purple", genre="Fiction", published_year=1982, author=a1)
    Book.objects.create(title="1984", genre="Dystopian", published_year=1949, author=a2)
    Book.objects.create(title="Animal Farm", genre="Satire", published_year=1945, author=a2)

    print("✅ Database seeded successfully.")


if __name__ == "__main__":
    run()
