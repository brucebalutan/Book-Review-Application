def read_file():
    # Importing all necessary modules
    from reviews.models import Publisher, Book, BookContributor, Contributor, Review
    from datetime import datetime, date
    from django.contrib.auth.models import User
    # Read from file and initializing content variable
    in_file = open("WebDevWithDjangoData.csv", "r")
    lines = in_file.readlines()
    content = ''
    # Going through the lines array
    for line in lines:
        # Split all the commas
        row = line.split(",")
        print(row)
        print(content)
        # Making sure the indexes are in the correct spot
        # Checking if content is in the first element
        if 'content' in row[0]:
            # Checking what type of Model is needed
            if 'Publisher' in row[0]:
                content = 'Publisher'
            elif 'BookContributor' in row[0]:
                content = 'BookContributor'
            elif 'Book' in row[0]:
                content = 'Book'
            elif 'Contributor' in row[0]:
                content = 'Contributor'
            elif 'Review' in row[0]:
                content = 'Review'
        # If first element is empty, continue to next iteration
        elif row[0] == '':
            content = ''
            continue
        # Publisher Model Block
        if content == 'Publisher':
            publisher_name = row[0]
            # Continue to next iteration if publisher_name is column listing
            if publisher_name == 'publisher_name' or publisher_name=='content:Publisher':
                continue
            publisher_website = row[1]
            publisher_email = row[2]
            # Create and save Publisher
            publisher = Publisher(name=publisher_name, website=publisher_website, email=publisher_email)
            publisher.save()
        # Book Model Block
        elif content == 'Book':
            book_title = row[0]
            # Continue to next iteration if first element is book_title
            if book_title == 'book_title' or book_title == 'content:Book':
                continue
            book_publication_date = row[1]
            # Split by / and initialize the date
            if book_publication_date:
                book_publication_date = book_publication_date.split('/')
                book_date = date(int(book_publication_date[0]), int(book_publication_date[1]),
                                 int(book_publication_date[2]))
                print(book_date)
            else:
                book_date = None
            book_isbn = row[2]
            book_publisher_name = row[3]
            # Get the publisher for foreign key
            publisher = Publisher.objects.get(name=book_publisher_name)
            # Create and save Book object
            book = Book(title=book_title, publication_date=book_date,
                        isbn=int(book_isbn),
                        publisher=publisher)
            book.save()
        # Contributor Model Block
        elif content == 'Contributor':
            contributor_first_names = row[0]
            # If first element is contributor_first_names, continue to next iteration
            if contributor_first_names == 'contributor_first_names' or contributor_first_names == 'content:Contributor':
                continue
            contributor_last_names = row[1]
            contributor_email = row[2]
            # Create and save Contributor object
            contributor = Contributor(first_names=contributor_first_names,
                                      last_names=contributor_last_names,
                                      email=contributor_email)
            contributor.save()
        # BookContributor Model Block
        elif content == 'BookContributor':
            book_contributor_book = row[0]
            # If first element is book_contributor_book, go to next iteration
            if book_contributor_book == 'book_contributor_book' or book_contributor_book == 'content:BookContributor':
                continue
            book_contributor_contributor = row[1]
            book_contributor_role = row[2]
            # Get the book using the get method
            book = Book.objects.get(title=book_contributor_book)
            # Get the contributor using the get method
            contributor = Contributor.objects.get(email=book_contributor_contributor)
            # Create and save BookContributor object
            book_contributor = BookContributor(book=book, contributor=contributor, role=book_contributor_role)
            book_contributor.save()
            # Save these contributors to the book foreign key
            book.contributors.add(contributor, through_defaults={'role': book_contributor_role})
            book.save()
        # Review Model Block
        elif content == 'Review':
            review_content = row[0]
            # If the first element is review_content continue to next iteration
            if review_content == 'review_content' or review_content == 'content:Review':
                continue
            review_rating = row[1]
            # Use date time to create the date
            review_date_created = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f")
            review_date_edited = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f")
            review_creator = row[4].strip('\n')
            # Create a user object
            user = User.objects.create_user(username=review_creator[:4], email=review_creator, last_login=datetime.now())
            # Get a book based on title for foreign key
            review_book = Book.objects.get(title=row[5].strip('\n'))
            # Create and save Review object
            review = Review(content=review_content,
                            rating=int(review_rating),
                            date_created=review_date_created,
                            date_edited=review_date_edited,
                            book=review_book,
                            creator=user)
            review.save()
