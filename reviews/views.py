from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .utils import *

# Create your views here.
"""
def index(request):
    return HttpResponse('Hello, world!')


def index(request):
    name = request.GET.get('name') or 'World!!!'
    return HttpResponse('Hello, {}!'.format(name))
"""


# Index html view
def index(request):
    return render(request, 'base.html')


# Book search view that takes a parameter
def book_search(request):
    search_text = request.GET.get('search')
    return render(request, 'search-results.html', {'search_text': search_text})


# A singular book's details along with its reviews
def book_detail(request, pk):
    from .models import Book
    # Get the book
    book = get_object_or_404(Book, pk=int(pk))
    reviews = book.review_set.all()
    # Use the average rating function
    book_rating = average_rating([review.rating for review in reviews])
    # Pass this information to the book_detail template
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews, 'book_rating': book_rating})


# List of all books with their information
def books_list(request):
    from .models import Book
    books = Book.objects.all()
    book_list = []
    # For loop that goes through every book
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        # Appends the book to book_list
        book_list.append({'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})
    context = {'book_list': book_list}
    # Render the books_list template with the context and request
    return render(request, 'books_list.html', context)


def email(request):
    if request.method == 'POST':
        sender_email = request.POST.get('sender')
        receiver_email = request.POST.get('receiver')
        cc_email = request.POST.get('cc', '')  # Optional field, default to empty string if not provided
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        # Now you can use the form data as needed, such as sending an email or saving it to the database

        # For now, let's just print the data to the console
        print(f"Sender: {sender_email}")
        print(f"Receiver: {receiver_email}")
        print(f"CC: {cc_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")

        # Add your email sending or database saving logic here

        return HttpResponse("Email sent successfully!" + "\n" + sender_email +
                            "\n" + receiver_email + "\n" +
                            cc_email + "\n" + subject + "\n" + body)  # You might want to redirect or render a success page instead

    return render(request, 'email.html')


"""
def index(request):
    n = 'world'
    return render(request, 'base.html', {'name': n})
"""
