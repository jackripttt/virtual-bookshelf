from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_unique_library.db"
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# Function to add initial books to the database
def add_initial_books():
    initial_books = [
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "rating": 9.2
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "rating": 8.7
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "rating": 8.9
        }
    ]

    for book_data in initial_books:
        new_book = Book(
            title=book_data["title"],
            author=book_data["author"],
            rating=book_data["rating"]
        )
        db.session.add(new_book)
    db.session.commit()

# Route to add initial books
@app.route('/add_initial_books')
def add_initial_books_route():
    add_initial_books()
    return redirect(url_for('home'))

# Route to display all books on the bookshelf
@app.route('/bookshelf')
def bookshelf():
    all_books = Book.query.order_by(Book.title).all()
    return render_template("bookshelf.html", books=all_books)

# Route to display the home page
@app.route('/')
def home():
    all_books = Book.query.order_by(Book.title).all()
    return render_template("index.html", books=all_books)

# Route to add a new book
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

# Route to edit a book's rating
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = Book.query.get_or_404(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get_or_404(book_id)
    return render_template("edit_rating.html", book=book_selected)

# Route to delete a book
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get_or_404(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
