import sys
import os

# Setup Django environment
projectRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if projectRoot not in sys.path:
    sys.path.insert(0, projectRoot)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "querysets.settings")

import django
django.setup()


from books.models import Book, Author
from django.db.models import Count, Avg, Q


def runQuerySetPractice():
    print(" QuerySet Practice for Beginners\n")


    print(" All Books:")
    allBooks = Book.objects.all()
    for book in allBooks:
        print(f"{book.title}")
    
    print("\n First Book:")
    firstBook = Book.objects.first()
    if firstBook:
        print(f"- {firstBook.title}")
    
    # Filter books by title
    print("\n Books with 'farm' in the title (case-insensitive):")
    farmBooks = Book.objects.filter(title__icontains='farm')
    for book in farmBooks:
        print(f"- {book.title}")
    
    print("\n Books published after 2000:")
    booksAfter2000 = Book.objects.filter(published_year__gt=2000)
    for book in booksAfter2000:
        print(f"- {book.title} ({book.published_year})")
    
    print("\n Books in genre 'Fiction':")
    fictionBooks = Book.objects.filter(genre='Fiction')
    for book in fictionBooks:
        print(f"- {book.title}")
    
    print("\n Distinct genres:")
    distinctGenres = Book.objects.values_list('genre', flat=True).distinct()
    for genre in distinctGenres:
        print(f"- {genre}")

    print("\n Total number of books:")
    totalBooks = Book.objects.count()
    print(f"Total books: {totalBooks}")

 
    print("\n Average published year of books:")
    averageYear = Book.objects.aggregate(Avg('published_year'))['published_year__avg']
    if averageYear:
        print(f"Average year: {averageYear:.2f}")
    else:
        print("No books in the database.")

    print("\n All Authors:")
    allAuthors = Author.objects.all()
    for author in allAuthors:
        print(f"- {author.name}")
    
    print("\n Count of books for each author:")
    authorsWithCount = Author.objects.annotate(bookCount=Count('book'))
    for author in authorsWithCount:
        print(f"- {author.name}: {author.bookCount} books")


    print("\n Books ordered by published year (latest first):")
    orderedBooks = Book.objects.order_by('-published_year')
    for book in orderedBooks:
        print(f"- {book.title} ({book.published_year})")

    print("\n Books that are NOT Fiction:")
    nonFictionBooks = Book.objects.exclude(genre='Fiction')
    for book in nonFictionBooks:
        print(f"- {book.title} ({book.genre})")

    print("\n Fiction books published after 2000:")
    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=2000)
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")

    print("\n Fiction books published after 1903:")
    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=1903).exclude(title__icontains = 'farm')
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")


    print("\n Books with 'war' in title OR genre is 'History':")
    qBooks = Book.objects.filter(Q(title__icontains='farm') | Q(genre='History'))

    for book in qBooks:
        print(f"- {book.title} ({book.genre})")

    print("\n Books with author (using select_related):")
    booksWithAuthor = Book.objects.select_related('author')
    for book in booksWithAuthor:
        print(f"- {book.title} by {book.author.name}")




if __name__ == "__main__":
    runQuerySetPractice()
