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
    print(allBooks.query)

    for book in allBooks:
        print(f"{book.title}")
    
    print("\n First Book:")
    firstBook = Book.objects.first()
    # print(firstBook.query)
    if firstBook:
        print(f"- {firstBook.title}")
    
    # Filter books by title
    print("\n Books with 'farm' in the title (case-insensitive):")
    farmBooks = Book.objects.filter(title__icontains='farm')
    print(farmBooks.query)
    for book in farmBooks:
        print(f"- {book.title}")
    
    print("\n Books published after 2000:")
    booksAfter2000 = Book.objects.filter(published_year__gt=2000)
    print(booksAfter2000.query)
    for book in booksAfter2000:
        print(f"- {book.title} ({book.published_year})")
    
    print("\n Books in genre 'Fiction':")
    fictionBooks = Book.objects.filter(genre='Fiction')
    print(fictionBooks.query)
    for book in fictionBooks:
        print(f"- {book.title}")
    
    print("\n Distinct genres:")
    distinctGenres = Book.objects.values_list('genre', flat=True).distinct()
    print(distinctGenres.query)
    for genre in distinctGenres:
        print(f"- {genre}")

    print("\n Total number of books:")
    totalBooks = Book.objects.count()
    # print(totalBooks.query)
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


    print("\n Books ordered by published year (latest first):")
    orderedBooks = Book.objects.order_by('-published_year')
    print(orderedBooks.query)
    for book in orderedBooks:
        print(f"- {book.title} ({book.published_year})")

    print("\n Books that are NOT Fiction:")
    nonFictionBooks = Book.objects.exclude(genre='Fiction')
    print(nonFictionBooks.query)
    for book in nonFictionBooks:
        print(f"- {book.title} ({book.genre})")

    print("\n Fiction books published after 2000:")
    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=2000)
    print(recentFiction.query)
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")

    print("\n Fiction books published after 1903:")
    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=1903).exclude(title__icontains = 'farm')
    print(recentFiction.query)
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")


    print("\n Books with 'war' in title OR genre is 'History':")
    qBooks = Book.objects.filter(Q(title__icontains='farm') | Q(genre='History'))
    print(qBooks.query)
    for book in qBooks:
        print(f"- {book.title} ({book.genre})")


    # JOIN QUERY
    print("\n Books with author (using select_related):")
    booksWithAuthor = Book.objects.select_related('author')
    print(booksWithAuthor.query)
    for book in booksWithAuthor:
        print(f"- {book.title} by {book.author.name}")

    print("\nBooks written by author 'George Orwell':")
    orwellBooks = Book.objects.filter(author__name='George Orwell')
    print(orwellBooks.query)
    for book in orwellBooks:
        print(f"- {book.title}")

    print("\nFirst 3 books and their authors (using select_related):")
    top_books = Book.objects.select_related('author')[:1]
    print(top_books.query)
    for book in top_books:
        print(f"- {book.title} written by {book.author.name}")


    print("\nAuthors and their books (using prefetch_related):")
    authors = Author.objects.prefetch_related('book_set')
    print("authors and thier books",authors.query)
    for author in authors:
        print(f"- {author.name}")
        for book in author.book_set.all():
            print(f"   -{book.title}")

    print("\nAuthors with at least one book after 1903:")
    authorsWithBooks = Author.objects.filter(book__published_year__gt=1903).distinct()
    print("Authors with book",authorsWithBooks.query)
    for author in authorsWithBooks:
        print(f"- {author.name}")

    print("\nAuthors and their books:")
    authors = Author.objects.prefetch_related('book_set')
    print("Check query ",authors.query)
    for author in authors:
        print(f"- {author.name}")
        for book in author.book_set.all():
            print(f"   • {book.title}")

    print("\n Count of books for each author:")
    authorsWithCount = Author.objects.annotate(bookCount=Count('book'))
    print("count query",authorsWithCount.query)
    for author in authorsWithCount:
        print(f"- {author.name}: {author.bookCount} books")

    print("\n raw query for join author and book")
    books = Book.objects.raw("""
        SELECT b.id, b.title, b.published_year, a.name AS author_name
        FROM books_book b
        JOIN books_author a ON b.author_id = a.id
        WHERE b.published_year > 1903
    """)

    for book in books:
        print(f"{book.title} ({book.published_year}) by {book.author_name}")

    # changes in the main branch


if __name__ == "__main__":
    runQuerySetPractice()
