from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<Book {self.title}>'

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Extract form data
        book_title = request.form.get('bookTitle')
        author = request.form.get('author')
        year = request.form.get('year')
        quantity = request.form.get('quantity')
        
        # Print form data to terminal
        print(f"Book Title: {book_title}")
        print(f"Author: {author}")
        print(f"Publication Year: {year}")
        print(f"Quantity: {quantity}")
        
        # Create a new book object
        new_book = Book(
            title=book_title,
            author=author,
            year=int(year),
            quantity=int(quantity)
        )
        
        # Add to database
        db.session.add(new_book)
        db.session.commit()
        
        # Redirect back to the form
        return redirect(url_for('add_book'))
    
    return render_template('add-book.html')
    
@app.route('/view-books')
def view_books():
    # Query all books from the database
    books = Book.query.all()
    return render_template('view-books.html', books=books)
   
if __name__ == '__main__':
    app.run(debug=True)
