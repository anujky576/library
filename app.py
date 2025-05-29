from flask import Flask, render_template, request, redirect, url_for  # type: ignore
from flask_mysqldb import MySQL  # type: ignore
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# 🛠️ Configure MySQL using environment variables
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# 🔹 Home Page
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('home.html', books=books)


@app.route('/available_books')
def available_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT serial_number, title, author, publication FROM books WHERE borrower_id IS NULL")
    books = cur.fetchall()
    cur.close()
    return render_template('available_books.html', books=books)

@app.route('/borrowed_books')
def borrowed_books():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT books.serial_number, books.title, books.author, books.publication, borrowers.name AS borrower_name,
               books.issue_date, books.due_date
        FROM books
        INNER JOIN borrowers ON books.borrower_id = borrowers.id
        WHERE books.borrower_id IS NOT NULL
    """)
    borrowed_books = cur.fetchall()
    cur.close()

    # Debugging: Print the fetched data
    print("Borrowed Books Data:", borrowed_books)

    # Pass the current date to the template
    current_date = datetime.now().date()
    return render_template('borrowed_books.html', borrowed_books=borrowed_books, current_date=current_date)

# 🔹 Borrowers Page
@app.route('/add_borrower', methods=['POST'])
def add_borrower():
    print("Add Borrower route called")  # Debugging statement
    name = request.form['name']
    email = request.form['email']

    # Insert the borrower into the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO borrowers (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('borrowers'))

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        # Fetch form data
        serial_number = request.form['serial_number']
        borrower_id = request.form['borrower_id']

        # Validate and parse the issue date
        try:
            issue_date = datetime.strptime(request.form['issue_date'], '%Y-%m-%d').date()
        except ValueError:
            return "Invalid issue date format. Please use YYYY-MM-DD.", 400

        # Calculate the due date (14 days from the issue date)
        due_date = issue_date + timedelta(days=14)

        # Check if the book is available
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM books WHERE serial_number = %s AND borrower_id IS NULL", (serial_number,))
        book = cur.fetchone()

        if book:  # If the book is available
            book_id = book[0]

            # Update the book with borrower_id, issue_date, and due_date
            cur.execute("""
                UPDATE books
                SET borrower_id = %s, issue_date = %s, due_date = %s
                WHERE id = %s
            """, (borrower_id, issue_date, due_date, book_id))

            # Commit the changes and close the cursor
            mysql.connection.commit()
            cur.close()

            # Redirect to the borrowed books page
            return redirect(url_for('borrowed_books'))
        else:  # If the book is not available
            cur.close()
            return "Book not available or already borrowed", 404

    # Handle GET request: Fetch available books and borrowers for the dropdown
    cur = mysql.connection.cursor()
    cur.execute("SELECT serial_number, title FROM books WHERE borrower_id IS NULL")
    available_books = cur.fetchall()
    cur.execute("SELECT id, name FROM borrowers")
    borrowers = cur.fetchall()
    cur.close()
    # Render the borrow book form
    return render_template('borrow_book.html', available_books=available_books, borrowers=borrowers)

@app.route('/borrowers')
def borrowers():
    cur = mysql.connection.cursor()

    # Fetch borrowers and check if they have due books
    cur.execute("""
        SELECT borrowers.id, borrowers.name, borrowers.email,
               EXISTS (
                   SELECT 1
                   FROM books
                   WHERE books.borrower_id = borrowers.id
               ) AS has_due_books
        FROM borrowers
    """)
    borrower_data = cur.fetchall()
    cur.close()

    return render_template('borrowers.html', borrowers=borrower_data)

@app.route('/return_book', methods=['POST'])
def return_book():
    serial_number = request.form['serial_number']

    cur = mysql.connection.cursor()

    # Reset the borrower_id for the returned book
    cur.execute("""
        UPDATE books
        SET borrower_id = NULL
        WHERE serial_number = %s
    """, (serial_number,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('borrowed_books'))

@app.route('/return_with_penalty', methods=['POST'])
def return_with_penalty():
    serial_number = request.form['serial_number']

    cur = mysql.connection.cursor()

    # Reset the borrower_id, issue_date, and due_date for the returned book
    cur.execute("""
        UPDATE books
        SET borrower_id = NULL, issue_date = NULL, due_date = NULL
        WHERE serial_number = %s
    """, (serial_number,))

    # Optionally, log the penalty (e.g., store in a penalties table)
    # Example:
    # cur.execute("INSERT INTO penalties (serial_number, penalty_amount) VALUES (%s, %s)", (serial_number, penalty_amount))

    mysql.connection.commit()
    cur.close()
    return redirect(url_for('borrowed_books'))

@app.route('/remove_borrower', methods=['POST'])
def remove_borrower():
    borrower_id = request.form['borrower_id']

    try:
        cur = mysql.connection.cursor()

        # Remove the borrower from the database
        cur.execute("DELETE FROM borrowers WHERE id = %s", (borrower_id,))

        # Commit the changes
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('borrowers'))  # Redirect back to the Borrowers page
    except Exception as e:
        return f"An error occurred: {e}", 500


# 🔹 Due Books Page
@app.route('/due_books')
def due_books():
    cur = mysql.connection.cursor()

    # Fetch books that are overdue (no longer applicable since due_date is removed)
    cur.execute("""
        SELECT books.title, books.author, borrowers.name AS borrower_name
        FROM books
        LEFT JOIN borrowers ON books.borrower_id = borrowers.id
        WHERE books.borrower_id IS NOT NULL
    """)
    due_books = cur.fetchall()

    sanitized_due_books = [
        {
            "title": book[0],
            "author": book[1],
            "borrower_name": book[2]
        }
        for book in due_books
    ]

    cur.close()

    return render_template('due_books.html', due_books=sanitized_due_books)

@app.route('/clean_borrowed_books', methods=['POST'])
def clean_borrowed_books():
    try:
        cur = mysql.connection.cursor()

        # Reset borrower_id, issue_date, and due_date for all borrowed books
        cur.execute("""
            UPDATE books
            SET borrower_id = NULL, issue_date = NULL, due_date = NULL
            WHERE borrower_id IS NOT NULL
        """)

        # Commit the changes
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('borrowed_books'))  # Redirect back to the Borrowed Books page
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    books = []
    if query:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT serial_number, title, author, publication
            FROM books
            WHERE title LIKE %s OR author LIKE %s OR serial_number LIKE %s
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        books = cur.fetchall()
        cur.close()
    return render_template('available_books.html', books=books, search_query=query)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)