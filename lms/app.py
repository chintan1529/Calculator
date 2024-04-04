from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# List to store details of issued books
issued_books = []

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return data['items']
    else:
        return []

@app.route('/')
def home():
    return render_template('home.html', issued_books=issued_books)

@app.route('/search-book', methods=['GET', 'POST'])
def search_book():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = search_books(query)
    return render_template('search_book.html', results=results)

@app.route('/issue-book', methods=['POST'])
def issue_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        name = request.form['name']
        number = request.form['number']
        date_issued = request.form['date_issued']
        # Store the details of the issued book in the database
        issued_books.append({'title': title, 'author': author, 'isbn': isbn, 'name': name, 'number': number, 'date_issued': date_issued})
        return redirect(url_for('home'))  # Redirect to the home page after issuing the book

@app.route('/return-book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        input_name = request.form['input_name']
        # Check if the input is a book name or a person's name
        for book in issued_books:
            if input_name.lower() in book['title'].lower() or input_name.lower() == book['name'].lower():
                issued_books.remove(book)
                return render_template('return_success.html')  # Render success template if book is returned
        return "Book or borrower not found. Please try again."
    else:
        return render_template('return.html')
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
