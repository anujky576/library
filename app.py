"""
Updated Flask app.py for Normalized Database Schema (3NF)
This version uses the normalized collections structure
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Configure MongoDB
app.config['MONGO_URI'] = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/') + os.getenv('MONGODB_DB', 'library_management')
mongo = PyMongo(app)

# ====== VALIDATION HELPER FUNCTIONS ======

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_paginated_results(items, page, items_per_page=10):
    """
    Paginate a list of items
    Returns: (paginated_items, total_pages, current_page, total_items)
    """
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # ceiling division
    
    # Ensure page is valid
    if page < 1:
        page = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    # Calculate start and end indices
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    
    paginated_items = items[start_idx:end_idx]
    
    return paginated_items, total_pages, page, total_items


def book_with_details(book):
    """Enhance book document with author and publication details"""
    if book:
        author = mongo.db.authors.find_one({"_id": book.get("author_id")})
        publication = mongo.db.publications.find_one({"_id": book.get("publication_id")})
        
        book['author'] = author['name'] if author else "Unknown"
        book['publication'] = publication['name'] if publication else "Unknown"
    
    return book


def get_books_with_details(query=None):
    """Get books with author and publication details using aggregation"""
    if query is None:
        query = {}
    
    pipeline = [
        {"$match": query},
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author_details"
            }
        },
        {
            "$lookup": {
                "from": "publications",
                "localField": "publication_id",
                "foreignField": "_id",
                "as": "publication_details"
            }
        },
        {
            "$addFields": {
                "author": {
                    "$ifNull": [
                        {"$arrayElemAt": ["$author_details.name", 0]},
                        "$author"  # Fall back to existing author field if lookup fails
                    ]
                },
                "publication": {
                    "$ifNull": [
                        {"$arrayElemAt": ["$publication_details.name", 0]},
                        "$publication"  # Fall back to existing publication field if lookup fails
                    ]
                }
            }
        },
        {
            "$project": {
                "author_details": 0,
                "publication_details": 0
            }
        }
    ]
    
    return list(mongo.db.books.aggregate(pipeline))


def get_borrowed_books_with_details():
    """Get all borrowed books with borrower, book, author, and publication details"""
    pipeline = [
        {"$match": {"status": "borrowed"}},
        {
            "$lookup": {
                "from": "borrowers",
                "localField": "borrower_id",
                "foreignField": "_id",
                "as": "borrower"
            }
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book"
            }
        },
        {
            "$lookup": {
                "from": "authors",
                "localField": "book.author_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$lookup": {
                "from": "publications",
                "localField": "book.publication_id",
                "foreignField": "_id",
                "as": "publication"
            }
        },
        {
            "$unwind": "$borrower"
        },
        {
            "$unwind": "$book"
        },
        {
            "$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}
        },
        {
            "$unwind": {"path": "$publication", "preserveNullAndEmptyArrays": True}
        },
        {
            "$project": {
                "_id": 1,
                "serial_number": "$book.serial_number",
                "title": "$book.title",
                "isbn": "$book.isbn",
                "category": "$book.category",
                "author": {
                    "$ifNull": [
                        "$author.name",
                        "$book.author"  # Fall back to string author field if lookup fails
                    ]
                },
                "publication": {
                    "$ifNull": [
                        "$publication.name",
                        "$book.publication"  # Fall back to string publication field if lookup fails
                    ]
                },
                "borrower": 1,
                "issue_date": 1,
                "due_date": 1,
                "return_date": 1,
                "status": 1,
                "book_id": 1
            }
        }
    ]
    
    books = list(mongo.db.borrow_transactions.aggregate(pipeline))
    
    # Calculate fine for overdue books (2 rupees per day)
    current_date = datetime.now()
    for book in books:
        book['days_overdue'] = 0
        book['fine'] = 0
        if book.get('due_date') and book['due_date'] < current_date:
            days_overdue = (current_date.date() - book['due_date'].date()).days
            book['days_overdue'] = days_overdue
            book['fine'] = days_overdue * 2  # 2 rupees per day
    
    return books


# ====== ROUTES ======

@app.route('/')
def home():
    """Home page with all books"""
    books = get_books_with_details()
    return render_template('home.html', books=books)


@app.route('/available_books')
def available_books():
    """Show all available books with category filter, search, and pagination"""
    # Get category filter from query parameters
    category = request.args.get('category', '').strip()
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = {"quantity_available": {"$gt": 0}}
    if category:
        query["category"] = category
    
    # Add search query if provided
    if search_query:
        search_regex = {"$regex": search_query, "$options": "i"}  # Case-insensitive search
        query["$or"] = [
            {"serial_number": search_regex},
            {"title": search_regex},
            {"author": search_regex},
            {"publication": search_regex},
            {"isbn": search_regex},
            {"category": search_regex}
        ]
    
    # Get books
    all_books = get_books_with_details(query)
    
    # Apply pagination
    books, total_pages, current_page, total_items = get_paginated_results(all_books, page, items_per_page=10)
    
    # Get all unique categories
    all_categories = sorted(mongo.db.books.find().distinct("category"))
    all_categories = [cat for cat in all_categories if cat]  # Remove empty strings
    
    return render_template('available_books.html', 
                         books=books, 
                         categories=all_categories, 
                         selected_category=category,
                         search_query=search_query,
                         current_page=current_page,
                         total_pages=total_pages,
                         total_items=total_items)


@app.route('/borrowed_books')
def borrowed_books():
    """Show all currently borrowed books with pagination"""
    page = request.args.get('page', 1, type=int)
    
    borrowed_books_data = get_borrowed_books_with_details()
    current_date = datetime.now()
    
    # Apply pagination
    books, total_pages, current_page, total_items = get_paginated_results(borrowed_books_data, page, items_per_page=10)
    
    return render_template('borrowed_books.html', 
                         borrowed_books=books, 
                         current_date=current_date,
                         current_page=current_page,
                         total_pages=total_pages,
                         total_items=total_items)


@app.route('/due_books')
def due_books():
    """Show overdue books with pagination"""
    page = request.args.get('page', 1, type=int)
    
    pipeline = [
        {
            "$match": {
                "status": "borrowed",
                "due_date": {"$lt": datetime.now()}
            }
        },
        {
            "$lookup": {
                "from": "borrowers",
                "localField": "borrower_id",
                "foreignField": "_id",
                "as": "borrower"
            }
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book"
            }
        },
        {
            "$lookup": {
                "from": "authors",
                "localField": "book.author_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$unwind": "$borrower"
        },
        {
            "$unwind": "$book"
        },
        {
            "$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}
        },
        {
            "$project": {
                "_id": 1,
                "serial_number": "$book.serial_number",
                "title": "$book.title",
                "isbn": "$book.isbn",
                "category": "$book.category",
                "author": "$author.name",
                "borrower": 1,
                "issue_date": 1,
                "due_date": 1
            }
        }
    ]
    
    due_books_data = list(mongo.db.borrow_transactions.aggregate(pipeline))
    
    # Calculate fine for overdue books (2 rupees per day)
    current_date = datetime.now()
    for book in due_books_data:
        if book.get('due_date'):
            days_overdue = (current_date.date() - book['due_date'].date()).days
            book['days_overdue'] = days_overdue
            book['fine'] = days_overdue * 2  # 2 rupees per day
    
    # Apply pagination
    books, total_pages, current_page, total_items = get_paginated_results(due_books_data, page, items_per_page=10)
    
    return render_template('due_books.html', 
                         due_books=books,
                         current_page=current_page,
                         total_pages=total_pages,
                         total_items=total_items)


# ====== BORROWER MANAGEMENT ======

@app.route('/borrowers')
def borrowers():
    """Borrower management page - Add new borrower"""
    return render_template('borrowers.html')


@app.route('/view_all_borrowers')
def view_all_borrowers():
    """View all registered borrowers"""
    borrowers_list = list(mongo.db.borrowers.find())
    
    # Add book count for each borrower
    for borrower in borrowers_list:
        count = mongo.db.borrow_transactions.count_documents({
            "borrower_id": borrower["_id"],
            "status": "borrowed"
        })
        borrower['borrowed_count'] = count
    
    return render_template('view_borrowers.html', borrowers=borrowers_list)


@app.route('/add_borrower', methods=['POST'])
def add_borrower():
    """Add a new borrower"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    student_id = request.form.get('student_id', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    
    # Validate inputs
    if not name or len(name) < 2:
        flash("Error: Name must be at least 2 characters long.", "error")
        return redirect(url_for('borrowers'))
    
    if not email or not validate_email(email):
        flash("Error: Invalid email format.", "error")
        return redirect(url_for('borrowers'))
    
    if not student_id or len(student_id) < 3:
        flash("Error: Student ID must be at least 3 characters long.", "error")
        return redirect(url_for('borrowers'))
    
    # Validate phone number format if provided
    if phone and not re.match(r'^[0-9\-\+\(\)\s]{7,}$', phone):
        flash("Error: Invalid phone number format.", "error")
        return redirect(url_for('borrowers'))
    
    # Check for duplicate email
    existing_email = mongo.db.borrowers.find_one({"email": email})
    if existing_email:
        flash(f"Error: Email '{email}' already registered.", "error")
        return redirect(url_for('borrowers'))
    
    # Check for duplicate student ID
    existing_student_id = mongo.db.borrowers.find_one({"student_id": student_id})
    if existing_student_id:
        flash(f"Error: Student ID '{student_id}' already registered.", "error")
        return redirect(url_for('borrowers'))
    
    try:
        # Generate a unique member ID (format: MEM-XXXXXXXXXXX)
        member_id = f"MEM-{student_id.upper()}-{datetime.now().strftime('%s')}"
        
        mongo.db.borrowers.insert_one({
            "member_id": member_id,
            "name": name,
            "email": email,
            "student_id": student_id,
            "phone": phone if phone else None,
            "address": address if address else None,
            "created_at": datetime.now()
        })
        flash(f"✅ Borrower added successfully! Member ID: {member_id}", "success")
        return redirect(url_for('borrowers'))
    except Exception as e:
        flash(f"Error: Failed to add borrower: {str(e)}", "error")
        return redirect(url_for('borrowers'))


@app.route('/remove_borrower/<borrower_id>', methods=['POST'])
def remove_borrower(borrower_id):
    """Remove a borrower and return their books"""
    try:
        borrower_id_obj = ObjectId(borrower_id)
    except:
        flash("Error: Invalid borrower ID.", "error")
        return redirect(url_for('borrowers'))
    
    # Check if borrower has active loans
    active_loans = mongo.db.borrow_transactions.count_documents({
        "borrower_id": borrower_id_obj,
        "status": "borrowed"
    })
    
    if active_loans > 0:
        flash(f"Error: Borrower has {active_loans} active loan(s). Return books first.", "error")
        return redirect(url_for('borrowers'))
    
    try:
        mongo.db.borrowers.delete_one({"_id": borrower_id_obj})
        flash("✅ Borrower removed successfully!", "success")
    except Exception as e:
        flash(f"Error: Failed to remove borrower: {str(e)}", "error")
    
    return redirect(url_for('borrowers'))


# ====== BOOK BORROWING ======

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    """Borrow a book"""
    if request.method == 'POST':
        serial_number = request.form.get('serial_number', '').strip()
        borrower_id = request.form.get('borrower_id', '').strip()
        issue_date_str = request.form.get('issue_date', '').strip()
        
        # Validation
        if not all([serial_number, borrower_id, issue_date_str]):
            flash("Error: All fields are required.", "error")
            return redirect(url_for('borrow_book'))
        
        try:
            borrower_id_obj = ObjectId(borrower_id)
        except:
            flash("Error: Invalid borrower selected.", "error")
            return redirect(url_for('borrow_book'))
        
        try:
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d')
        except ValueError:
            flash("Error: Invalid date format. Use YYYY-MM-DD.", "error")
            return redirect(url_for('borrow_book'))
        
        if issue_date > datetime.now():
            flash("Error: Issue date cannot be in the future.", "error")
            return redirect(url_for('borrow_book'))
        
        # Check if book exists and is available
        book = mongo.db.books.find_one({"serial_number": serial_number})
        
        if not book:
            flash("Error: Book not found.", "error")
            return redirect(url_for('borrow_book'))
        
        if book.get("quantity_available", 0) < 1:
            flash("Error: Book has no available copies.", "error")
            return redirect(url_for('borrow_book'))
        
        # Check if borrower exists
        borrower = mongo.db.borrowers.find_one({"_id": borrower_id_obj})
        if not borrower:
            flash("Error: Borrower not found.", "error")
            return redirect(url_for('borrow_book'))
        
        # Check for duplicate active borrow
        existing_borrow = mongo.db.borrow_transactions.find_one({
            "book_id": book["_id"],
            "borrower_id": borrower_id_obj,
            "status": "borrowed"
        })
        
        if existing_borrow:
            flash("Error: Borrower already has this book checked out.", "error")
            return redirect(url_for('borrow_book'))
        
        # Check if borrower can issue more books (max 2 books)
        active_borrows = mongo.db.borrow_transactions.count_documents({
            "borrower_id": borrower_id_obj,
            "status": "borrowed"
        })
        
        if active_borrows >= 2:
            flash(f"Error: Borrower has reached the maximum limit of 2 books. Please return a book first.", "error")
            return redirect(url_for('borrow_book'))
        
        try:
            # Calculate due date (14 days from issue date)
            due_date = issue_date + timedelta(days=14)
            
            # Create borrow transaction
            mongo.db.borrow_transactions.insert_one({
                "borrower_id": borrower_id_obj,
                "book_id": book["_id"],
                "serial_number": serial_number,
                "issue_date": issue_date,
                "due_date": due_date,
                "return_date": None,
                "status": "borrowed",
                "created_at": datetime.now()
            })
            
            # Decrease quantity_available
            mongo.db.books.update_one(
                {"_id": book["_id"]},
                {"$inc": {"quantity_available": -1}}
            )
            
            flash("✅ Book borrowed successfully!", "success")
            return redirect(url_for('borrowed_books'))
            
        except Exception as e:
            flash(f"Error: Failed to borrow book: {str(e)}", "error")
            return redirect(url_for('borrow_book'))
    
    else:  # GET request
        available_books = get_books_with_details({"quantity_available": {"$gt": 0}})
        borrowers = list(mongo.db.borrowers.find())
        
        # Add active borrow count for each borrower
        for borrower in borrowers:
            active_count = mongo.db.borrow_transactions.count_documents({
                "borrower_id": borrower["_id"],
                "status": "borrowed"
            })
            borrower['active_books'] = active_count
            borrower['can_borrow'] = active_count < 2
        
        return render_template('borrow_book.html', available_books=available_books, borrowers=borrowers)


@app.route('/return_book/<transaction_id>', methods=['POST'])
def return_book(transaction_id):
    """Return a borrowed book - Check if payment needed"""
    try:
        transaction_id_obj = ObjectId(transaction_id)
    except:
        flash("Error: Invalid transaction ID.", "error")
        return redirect(url_for('borrowed_books'))
    
    try:
        transaction = mongo.db.borrow_transactions.find_one({"_id": transaction_id_obj})
        
        if not transaction:
            flash("Error: Transaction not found.", "error")
            return redirect(url_for('borrowed_books'))
        
        # Calculate if there's a fine (overdue)
        current_date = datetime.now()
        fine = 0
        
        if transaction.get('due_date') and transaction['due_date'] < current_date:
            days_overdue = (current_date.date() - transaction['due_date'].date()).days
            fine = days_overdue * 2  # 2 rupees per day
        
        # If there's a fine, redirect to payment page
        if fine > 0:
            return redirect(url_for('payment_page', transaction_id=str(transaction_id_obj)))
        
        # If no fine, return book immediately
        return_book_directly(transaction_id_obj, transaction)
        flash("✅ Book returned successfully!", "success")
        
    except Exception as e:
        flash(f"Error: Failed to return book: {str(e)}", "error")
    
    return redirect(url_for('borrowed_books'))


def return_book_directly(transaction_id_obj, transaction):
    """Directly return book and update inventory"""
    mongo.db.borrow_transactions.update_one(
        {"_id": transaction_id_obj},
        {
            "$set": {
                "return_date": datetime.now(),
                "status": "returned"
            }
        }
    )
    
    # Increase quantity_available
    mongo.db.books.update_one(
        {"_id": transaction["book_id"]},
        {"$inc": {"quantity_available": 1}}
    )


@app.route('/payment/<transaction_id>')
def payment_page(transaction_id):
    """Display payment page for collecting fine"""
    try:
        transaction_id_obj = ObjectId(transaction_id)
    except:
        flash("Error: Invalid transaction ID.", "error")
        return redirect(url_for('borrowed_books'))
    
    try:
        # Get transaction with full details
        pipeline = [
            {"$match": {"_id": transaction_id_obj}},
            {
                "$lookup": {
                    "from": "borrowers",
                    "localField": "borrower_id",
                    "foreignField": "_id",
                    "as": "borrower"
                }
            },
            {
                "$lookup": {
                    "from": "books",
                    "localField": "book_id",
                    "foreignField": "_id",
                    "as": "book"
                }
            },
            {"$unwind": "$borrower"},
            {"$unwind": "$book"},
            {"$project": {"borrower_details": 0, "book_details": 0}}
        ]
        
        results = list(mongo.db.borrow_transactions.aggregate(pipeline))
        if not results:
            flash("Error: Transaction not found.", "error")
            return redirect(url_for('borrowed_books'))
        
        transaction = results[0]
        current_date = datetime.now()
        
        # Calculate fine
        days_overdue = 0
        if transaction.get('due_date'):
            days_overdue = (current_date.date() - transaction['due_date'].date()).days
        
        fine = days_overdue * 2
        
        # Prepare transaction data for payment template
        transaction_data = {
            'transaction_id': str(transaction_id_obj),
            'serial_number': transaction['book'].get('serial_number', 'N/A'),
            'title': transaction['book'].get('title', 'N/A'),
            'category': transaction['book'].get('category', 'N/A'),
            'author': transaction['book'].get('author', 'Unknown'),
            'borrower_name': transaction['borrower'].get('name', 'N/A'),
            'member_id': transaction['borrower'].get('member_id', 'N/A'),
            'email': transaction['borrower'].get('email', 'N/A'),
            'issue_date': transaction.get('issue_date').strftime('%d-%m-%Y') if transaction.get('issue_date') else 'N/A',
            'due_date': transaction.get('due_date').strftime('%d-%m-%Y') if transaction.get('due_date') else 'N/A',
            'days_overdue': days_overdue,
            'fine': fine
        }
        
        return render_template('payment.html', transaction=transaction_data, transaction_id=str(transaction_id_obj))
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('borrowed_books'))


@app.route('/process_payment', methods=['POST'])
def process_payment():
    """Process payment and return book"""
    transaction_id = request.form.get('transaction_id', '').strip()
    payment_method = request.form.get('payment_method', '').strip()
    amount = request.form.get('amount', 0, type=int)
    
    if not all([transaction_id, payment_method, amount]):
        flash("Error: Invalid payment details.", "error")
        return redirect(url_for('borrowed_books'))
    
    try:
        transaction_id_obj = ObjectId(transaction_id)
    except:
        flash("Error: Invalid transaction ID.", "error")
        return redirect(url_for('borrowed_books'))
    
    try:
        transaction = mongo.db.borrow_transactions.find_one({"_id": transaction_id_obj})
        
        if not transaction:
            flash("Error: Transaction not found.", "error")
            return redirect(url_for('borrowed_books'))
        
        # Get borrower and book details
        borrower = mongo.db.borrowers.find_one({"_id": transaction['borrower_id']})
        book = mongo.db.books.find_one({"_id": transaction['book_id']})
        
        # Return the book
        return_book_directly(transaction_id_obj, transaction)
        
        # Get updated transaction for receipt
        pipeline = [
            {"$match": {"_id": transaction_id_obj}},
            {
                "$lookup": {
                    "from": "borrowers",
                    "localField": "borrower_id",
                    "foreignField": "_id",
                    "as": "borrower"
                }
            },
            {
                "$lookup": {
                    "from": "books",
                    "localField": "book_id",
                    "foreignField": "_id",
                    "as": "book"
                }
            },
            {"$unwind": "$borrower"},
            {"$unwind": "$book"},
        ]
        
        results = list(mongo.db.borrow_transactions.aggregate(pipeline))
        updated_transaction = results[0] if results else transaction
        
        current_date = datetime.now()
        days_overdue = (current_date.date() - transaction['due_date'].date()).days if transaction.get('due_date') else 0
        
        # Create unique transaction ID
        unique_txn_id = f"TXN-{current_date.strftime('%Y%m%d')}-{int(datetime.now().timestamp())}"
        
        # Store payment record in payment_history collection
        mongo.db.payment_history.insert_one({
            'transaction_id': unique_txn_id,
            'borrow_transaction_id': transaction_id_obj,
            'borrower_id': transaction['borrower_id'],
            'book_id': transaction['book_id'],
            'title': book.get('title', 'N/A') if book else 'N/A',
            'serial_number': book.get('serial_number', 'N/A') if book else 'N/A',
            'borrower_name': borrower.get('name', 'N/A') if borrower else 'N/A',
            'member_id': borrower.get('member_id', 'N/A') if borrower else 'N/A',
            'amount': amount,
            'payment_method': payment_method.upper(),
            'payment_date': current_date,
            'status': 'PAID',
            'created_at': current_date
        })
        
        # Prepare receipt data
        receipt_data = {
            'receipt_number': f"REC-{int(datetime.now().timestamp())}",
            'title': book.get('title', 'N/A') if book else 'N/A',
            'serial_number': book.get('serial_number', 'N/A') if book else 'N/A',
            'category': book.get('category', 'N/A') if book else 'N/A',
            'borrower_name': borrower.get('name', 'N/A') if borrower else 'N/A',
            'member_id': borrower.get('member_id', 'N/A') if borrower else 'N/A',
            'email': borrower.get('email', 'N/A') if borrower else 'N/A',
            'issue_date': transaction.get('issue_date').strftime('%d-%m-%Y') if transaction.get('issue_date') else 'N/A',
            'due_date': transaction.get('due_date').strftime('%d-%m-%Y') if transaction.get('due_date') else 'N/A',
            'return_date': current_date.strftime('%d-%m-%Y'),
            'days_overdue': days_overdue,
            'fine': amount,
            'payment_method': payment_method.upper(),
            'payment_date': current_date.strftime('%d-%m-%Y %H:%M:%S'),
            'timestamp': current_date.strftime('%d %B %Y at %I:%M %p'),
            'transaction_id': unique_txn_id
        }
        
        flash("✅ Payment successful! Book returned.", "success")
        return render_template('payment_receipt.html', receipt=receipt_data)
        
    except Exception as e:
        flash(f"Error: Payment processing failed: {str(e)}", "error")
        return redirect(url_for('borrowed_books'))


# ====== TRANSACTION HISTORY & MANAGEMENT ======

@app.route('/transaction_history')
def transaction_history():
    """View all payment transactions with filtering and search"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '').strip()
    payment_method = request.args.get('payment_method', '').strip()
    date_range = request.args.get('date_range', '').strip()
    
    # Build query
    query = {}
    
    # Search filter
    if search_query:
        query['$or'] = [
            {'transaction_id': {'$regex': search_query, '$options': 'i'}},
            {'title': {'$regex': search_query, '$options': 'i'}},
            {'borrower_name': {'$regex': search_query, '$options': 'i'}},
            {'member_id': {'$regex': search_query, '$options': 'i'}}
        ]
    
    # Payment method filter
    if payment_method:
        query['payment_method'] = payment_method.upper()
    
    # Date range filter
    if date_range:
        today = datetime.now()
        if date_range == 'today':
            query['payment_date'] = {
                '$gte': datetime(today.year, today.month, today.day),
                '$lt': datetime(today.year, today.month, today.day) + timedelta(days=1)
            }
        elif date_range == 'week':
            query['payment_date'] = {'$gte': today - timedelta(days=7)}
        elif date_range == 'month':
            query['payment_date'] = {'$gte': today - timedelta(days=30)}
        elif date_range == 'year':
            query['payment_date'] = {'$gte': today - timedelta(days=365)}
    
    # Get all transactions
    all_transactions = list(mongo.db.payment_history.find(query).sort('payment_date', -1))
    
    # Calculate statistics
    total_transactions = len(all_transactions)
    total_collected = sum(txn.get('amount', 0) for txn in all_transactions)
    avg_fine = round(total_collected / total_transactions, 2) if total_transactions > 0 else 0
    total_books_returned = total_transactions
    
    stats = {
        'total_transactions': total_transactions,
        'total_collected': total_collected,
        'avg_fine': avg_fine,
        'total_books_returned': total_books_returned
    }
    
    # Apply pagination
    items_per_page = 10
    total_pages = (total_transactions + items_per_page - 1) // items_per_page
    
    if page < 1:
        page = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_transactions = all_transactions[start_idx:end_idx]
    
    # Format transactions for display
    formatted_transactions = []
    for txn in paginated_transactions:
        formatted_transactions.append({
            'transaction_id': txn.get('transaction_id', 'N/A'),
            'title': txn.get('title', 'N/A'),
            'borrower_name': txn.get('borrower_name', 'N/A'),
            'amount': txn.get('amount', 0),
            'payment_method': txn.get('payment_method', 'N/A'),
            'payment_date': txn['payment_date'].strftime('%d-%m-%Y') if txn.get('payment_date') else 'N/A',
            'payment_time': txn['payment_date'].strftime('%H:%M:%S') if txn.get('payment_date') else 'N/A',
            'status': txn.get('status', 'PAID'),
            'member_id': txn.get('member_id', 'N/A')
        })
    
    return render_template('transaction_history.html',
                         transactions=formatted_transactions,
                         stats=stats,
                         current_page=page,
                         total_pages=total_pages,
                         total_transactions=total_transactions,
                         search_query=search_query,
                         payment_method=payment_method,
                         date_range=date_range)


@app.route('/transaction_details/<transaction_id>')
def transaction_details(transaction_id):
    """View detailed information for a specific transaction"""
    try:
        txn = mongo.db.payment_history.find_one({'transaction_id': transaction_id})
        
        if not txn:
            flash("Error: Transaction not found.", "error")
            return redirect(url_for('transaction_history'))
        
        # Format transaction data
        transaction_data = {
            'transaction_id': txn.get('transaction_id'),
            'title': txn.get('title'),
            'serial_number': txn.get('serial_number'),
            'borrower_name': txn.get('borrower_name'),
            'member_id': txn.get('member_id'),
            'amount': txn.get('amount'),
            'payment_method': txn.get('payment_method'),
            'payment_date': txn['payment_date'].strftime('%d-%m-%Y %H:%M:%S') if txn.get('payment_date') else 'N/A',
            'status': txn.get('status'),
            'created_at': txn['created_at'].strftime('%d %B %Y at %I:%M %p') if txn.get('created_at') else 'N/A'
        }
        
        return render_template('transaction_details.html', transaction=transaction_data)
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('transaction_history'))


# ====== CLEANUP ======

@app.route('/clean_returned_books', methods=['POST'])
def clean_returned_books():
    """Remove returned book records"""
    try:
        result = mongo.db.borrow_transactions.delete_many({"status": "returned"})
        flash(f"✅ Removed {result.deleted_count} returned book records.", "success")
    except Exception as e:
        flash(f"Error: Failed to clean records: {str(e)}", "error")
    
    return redirect(url_for('borrowed_books'))


if __name__ == '__main__':
    app.run(debug=True)
