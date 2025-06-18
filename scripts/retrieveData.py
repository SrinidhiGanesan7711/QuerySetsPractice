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
    # select * from books_book;

    for book in allBooks:
        print(f"{book.title}")
    
    print("\n First Book:")
    firstBook = Book.objects.first()
    # select * from books_book order by id Asc limit 1;

    if firstBook:
        print(f"- {firstBook.title}")
    
    # Filter books by title
    print("\n Books with 'farm' in the title (case-insensitive):")
    farmBooks = Book.objects.filter(title__icontains='farm')
    # select * from books_book where LOWER(title) LIKE '%farm%';

    for book in farmBooks:
        print(f"- {book.title}")
    
    print("\n Books published after 2000:")
    booksAfter2000 = Book.objects.filter(published_year__gt=2000)
    # select * from books_book where published_year > 2000;
    for book in booksAfter2000:
        print(f"- {book.title} ({book.published_year})")
    
    print("\n Books in genre 'Fiction':")
    fictionBooks = Book.objects.filter(genre='Fiction')
    # select * from books_books where genre = 'Fiction'
    for book in fictionBooks:
        print(f"- {book.title}")
    
    print("\n Distinct genres:")
    distinctGenres = Book.objects.values_list('genre', flat=True).distinct()
    # select distinct genre from books_book;

    for genre in distinctGenres:
        print(f"- {genre}")

    print("\n Total number of books:")
    totalBooks = Book.objects.count()
    # select count(*) from books_book
    print(f"Total books: {totalBooks}")

 
    print("\n Average published year of books:")
    averageYear = Book.objects.aggregate(Avg('published_year'))['published_year__avg']
    # select AVG(published_year) from books_book;

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
    # select * from books_book order by published_year desc;

    for book in orderedBooks:
        print(f"- {book.title} ({book.published_year})")

    print("\n Books that are NOT Fiction:")
    # select * from books_book where genre <> 'Fiction';

    nonFictionBooks = Book.objects.exclude(genre='Fiction')
    for book in nonFictionBooks:
        print(f"- {book.title} ({book.genre})")

    print("\n Fiction books published after 2000:")
    # select * from books_book
    # where genre = 'Fiction' AND published_year > 2000;

    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=2000)
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")

    print("\n Fiction books published after 1903:")
    # select * from books_book where genre = 'Fiction' AND published_year > 1903 AND LOWER(title) NOT LIKE '%farm%';

    recentFiction = Book.objects.filter(genre='Fiction').filter(published_year__gt=1903).exclude(title__icontains = 'farm')
    for book in recentFiction:
        print(f"- {book.title} ({book.published_year})")


    print("\n Books with 'war' in title OR genre is 'History':")
    # select * from books_book where LOWER(title) LIKE '%farm%' OR genre = 'History';

    qBooks = Book.objects.filter(Q(title__icontains='farm') | Q(genre='History'))

    for book in qBooks:
        print(f"- {book.title} ({book.genre})")


    # JOIN QUERY
    print("\n Books with author (using select_related):")
#     select b.*, a.name AS author_name from books_book b join books_author a on b.author_id = a.id;


    booksWithAuthor = Book.objects.select_related('author')
    for book in booksWithAuthor:
        print(f"- {book.title} by {book.author.name}")

    print("\nBooks written by author 'George Orwell':")
#     select b.* from books_book b  join books_author onON b.author_id = a.id where a.name = 'George Orwell';

    orwellBooks = Book.objects.filter(author__name='George Orwell')
    for book in orwellBooks:
        print(f"- {book.title}")

    print("\nFirst 3 books and their authors (using select_related):")
#     select b.*, a.name AS author_name from books_book b join books_author on b.author_id = a.id limit 1;

    top_books = Book.objects.select_related('author')[:1]
    for book in top_books:
        print(f"- {book.title} written by {book.author.name}")


    print("\nAuthors and their books (using prefetch_related):")
    authors = Author.objects.prefetch_related('book_set')
    # select
    #     a.name AS author_name,
    #     b.title AS book_title
    # from
    #     books_author a
    # left join
    #     books_book b ON a.id = b.author_id
    # order by
    #     a.name;

    for author in authors:
        print(f"- {author.name}")
        for book in author.book_set.all():
            print(f"   -{book.title}")

    print("\nAuthors with at least one book after 1903:")
    # select distinct a.* from books_author a join books_book b on a.id = b.author_id where b.published_year > 1903;
    authorsWithBooks = Author.objects.filter(book__published_year__gt=1903).distinct()
    for author in authorsWithBooks:
        print(f"- {author.name}")

    print("\nAuthors and their books:")
    # select a.id AS author_id, a.name AS author_name,b.id AS book_id, b.title AS book_title from books_author a
    # left join books_book b on a.id = b.author_id order by a.id;
    authors = Author.objects.prefetch_related('book_set')
    for author in authors:
        print(f"- {author.name}")
        for book in author.book_set.all():
            print(f"   • {book.title}")

    print("\n Count of books for each author:")
    authorsWithCount = Author.objects.annotate(bookCount=Count('book'))
    #select a.id, a.name, COUNT(b.id) AS bookCount
    # from books_author a
    # left join books_book b ON a.id = b.author_id
    # group by a.id, a.name;

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


if __name__ == "__main__":
    runQuerySetPractice()
