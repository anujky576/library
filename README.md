# 📚 Library Management System

A comprehensive Flask-based web application for managing library operations, including book inventory management, borrower records, book lending/returning, and financial transaction tracking. Built with MongoDB for flexible document storage and designed following database normalization principles (3NF).

---

## 🎯 Project Overview

The Library Management System is designed to streamline library operations by providing:
- **Complete Book Management**: Track books with detailed metadata (serial number, ISBN, title, author, publication, category)
- **Borrower Management**: Register, store, and manage borrower information
- **Lending Operations**: Handle book borrowing/returning with automatic due dates and penalty calculations
- **Financial Tracking**: Process fine payments for overdue books with transaction history
- **Advanced Search & Filtering**: Find books by multiple criteria with pagination support

---

## ✨ Features

### 📖 Book Management
- ✅ View all books in the library with detailed information
- ✅ Search books by serial number, title, author, ISBN, publication, or category
- ✅ Category-based filtering for organized browsing
- ✅ Real-time availability tracking (available vs. borrowed)
- ✅ Pagination support for large book collections

### 👥 Borrower Management
- ✅ Add new borrowers with email validation
- ✅ View all registered borrowers with their borrowing history
- ✅ Unique email enforcement per borrower
- ✅ Remove borrowers with automatic return of all their books
- ✅ Cascade deletion to maintain referential integrity

### 🔄 Lending & Returning
- ✅ Borrow books with automatic 14-day due date calculation
- ✅ Validation to prevent duplicate simultaneous borrowing
- ✅ Availability checking before lending
- ✅ Return books and automatically calculate overdue fines
- ✅ Fine calculation: ₹2 per day for overdue books

### 📊 Transaction Management
- ✅ Complete transaction history with status tracking (borrowed, returned, paid)
- ✅ Overdue books dashboard with fine calculation
- ✅ Payment processing for outstanding fines
- ✅ Payment receipts generation
- ✅ Detailed transaction information with date tracking

### 🔍 Reporting & Tracking
- ✅ View all currently borrowed books
- ✅ Track overdue books with calculated penalties
- ✅ Transaction history with filtering and pagination
- ✅ Borrower-specific transaction records
- ✅ Daily operation summaries

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask 3.1.0 (Python) |
| **Database** | MongoDB with PyMongo |
| **Template Engine** | Jinja2 with HTML5 |
| **Package Manager** | pip |
| **Environment Management** | python-dotenv |
| **Python Version** | 3.8+ |

### Key Dependencies
```
Flask==3.1.0
flask-pymongo==3.0.1
pymongo==4.6.0
python-dotenv==1.0.1
Werkzeug==3.1.3
Jinja2==3.1.6
```

---

## 📋 Requirements

- **Python**: 3.8 or higher
- **MongoDB**: 4.0+ (local or cloud instance)
- **pip**: Python package manager (comes with Python)
- **RAM**: Minimum 512MB
- **Disk Space**: 500MB for installation and database

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd library-management
```

### Step 2: Create and Activate Virtual Environment
```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=library_management

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
DEBUG=True
```

### Step 5: Initialize Database
```bash
# For setting up constraints and indexes
python setup_constraints.py

# For seeding sample data (optional)
python seed_mongodb.py
```

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
library-management/
├── app.py                              # Main Flask application with all routes
├── config.py                           # Configuration settings
├── setup_constraints.py                # Database constraint and index setup
├── seed_mongodb.py                     # Sample data seeding script
├── requirements.txt                    # Python dependencies
├── CONSTRAINTS_DOCUMENTATION.md        # Detailed constraint documentation
├── .env                               # Environment variables (not in repo)
├── .venv/                             # Virtual environment directory
│
├── static/                            # Static assets
│   ├── css/                          # Stylesheets
│   └── js/                           # JavaScript files
│
└── templates/                         # HTML templates
    ├── home.html                     # Homepage with all books
    ├── navbar.html                   # Navigation bar
    ├── available_books.html          # Available books listing
    ├── borrowed_books.html           # Borrowed books display
    ├── due_books.html                # Overdue books tracking
    ├── borrowers.html                # Borrowers management
    ├── view_borrowers.html           # View all borrowers
    ├── borrow_book.html              # Book borrowing form
    ├── payment.html                  # Payment processing
    ├── payment_receipt.html          # Payment receipt
    ├── transaction_details.html      # Individual transaction details
    ├── transaction_history.html      # Complete transaction history
    └── due_books.html                # Due books view
```

---

## 🗄️ Database Schema & Normalization

### Database Structure

The Library Management System uses MongoDB with a **normalized 3NF schema** comprising the following collections:

#### 1. **Books Collection**
```json
{
  "_id": ObjectId,
  "serial_number": String (unique),
  "title": String,
  "isbn": String,
  "author_id": ObjectId (Foreign Key → authors),
  "publication_id": ObjectId (Foreign Key → publications),
  "category": String,
  "quantity_total": Integer,
  "quantity_available": Integer,
  "created_date": Date,
  "last_updated": Date
}
```

#### 2. **Authors Collection**
```json
{
  "_id": ObjectId,
  "name": String,
  "bio": String,
  "country": String,
  "created_date": Date
}
```

#### 3. **Publications Collection**
```json
{
  "_id": ObjectId,
  "name": String,
  "address": String,
  "contact": String,
  "created_date": Date
}
```

#### 4. **Borrowers Collection**
```json
{
  "_id": ObjectId,
  "name": String,
  "email": String (unique),
  "phone": String,
  "address": String,
  "registration_date": Date,
  "last_activity": Date
}
```

#### 5. **Borrow Transactions Collection**
```json
{
  "_id": ObjectId,
  "book_id": ObjectId (Foreign Key → books),
  "borrower_id": ObjectId (Foreign Key → borrowers),
  "issue_date": Date,
  "due_date": Date,
  "return_date": Date,
  "status": String (borrowed/returned/overdue),
  "fine_amount": Decimal,
  "paid_fine": Decimal,
  "created_date": Date
}
```

---

### 📐 Database Normalization (1NF, 2NF, 3NF)

#### **First Normal Form (1NF)**
✅ **Achieved** - All attributes contain atomic (indivisible) values
- Each field contains only single values, no repeating groups
- Example: Books don't store multiple authors in a single field; they reference `author_id`
- Borrowers have single email, name fields (not arrays)
- Transactions store individual book-borrower pairs

**Implementation:**
```python
# ❌ Violates 1NF (repeating group)
book = {
    "title": "Python Guide",
    "authors": ["John", "Jane"]  # Multiple authors in one field
}

# ✅ Follows 1NF (normalized reference)
book = {
    "title": "Python Guide",
    "author_id": ObjectId("...")  # Reference to authors collection
}
```

---

#### **Second Normal Form (2NF)**
✅ **Achieved** - All non-key attributes fully depend on the entire primary key
- All non-key attributes depend on the primary key
- No partial dependency on composite keys
- Author metadata (bio, country) stored separately, not duplicated in books
- Publication details separated from book records

**Advantages:**
- Eliminates redundant author/publication data
- Single update point for author information
- Prevents data anomalies

**Example:**
```python
# ❌ Violates 2NF (partial dependency)
books = {
    "serial_number": "B001",
    "author_name": "John Doe",
    "author_country": "USA",  # Depends only on author, not on book
    "title": "Python 101"
}

# ✅ Follows 2NF (separated concerns)
books = {
    "_id": ObjectId("..."),
    "serial_number": "B001",
    "author_id": ObjectId("..."),
    "title": "Python 101"
}

authors = {
    "_id": ObjectId("..."),
    "name": "John Doe",
    "country": "USA"
}
```

---

#### **Third Normal Form (3NF)**
✅ **Achieved** - All non-key attributes depend only on the primary key (no transitive dependencies)
- No transitive dependencies between non-key attributes
- Book's category doesn't depend on publication; it's a direct attribute
- Borrower's email/phone/address depend only on borrower ID, not on other attributes

**Normalization Process:**
```python
# ❌ Violates 3NF (transitive dependency)
books = {
    "title": "Python 101",
    "author_id": ObjectId("..."),
    "author_name": "John",              # Transitively depends on author_id
    "author_country": "USA",            # Transitively depends on author_id
    "publication_id": ObjectId("..."),
    "publication_name": "Pearson",      # Transitively depends on publication_id
}

# ✅ Follows 3NF (transitive dependencies removed)
books = {
    "_id": ObjectId("..."),
    "title": "Python 101",
    "author_id": ObjectId("..."),      # Only direct FK
    "publication_id": ObjectId("..."),  # Only direct FK
    "category": "Programming"           # Direct attribute
}

authors = {
    "_id": ObjectId("..."),
    "name": "John",
    "country": "USA"
}

publications = {
    "_id": ObjectId("..."),
    "name": "Pearson",
    "address": "..."
}
```

**Benefits of 3NF:**
- ✅ **Data Consistency**: Single source of truth for author/publication data
- ✅ **Reduced Redundancy**: No duplicate author/publication information
- ✅ **Easier Updates**: Change author info in one place
- ✅ **Query Optimization**: MongoDB aggregation pipelines with $lookup
- ✅ **Scalability**: Easy to add new collections without data duplication

---

## 🔐 Integrity Constraints

### 1. **UNIQUE Constraints**
- **Serial Number**: Each book must have a unique serial number
  - Enforced at: MongoDB unique index
  - Error Code: E11000
  
- **Email**: Each borrower must have a unique email
  - Enforced at: MongoDB unique index + application validation
  - Error Code: E11000 or validation message

### 2. **PRIMARY KEY Constraints**
- All collections use MongoDB's `_id` (ObjectId) as primary key
- Automatically generated and enforced
- Ensures every document is uniquely identifiable

### 3. **FOREIGN KEY Constraints** (Application Level)
- **Books → Authors**: `book.author_id` references `authors._id`
- **Books → Publications**: `book.publication_id` references `publications._id`
- **Borrow Transactions → Borrowers**: `transaction.borrower_id` references `borrowers._id`
- **Borrow Transactions → Books**: `transaction.book_id` references `books._id`

**Referential Integrity Implementation:**
```python
# Validate borrower exists before lending
borrower = mongo.db.borrowers.find_one({"_id": borrower_id_obj})
if not borrower:
    return "Error: Borrower not found.", 404

# Cascade delete: Return all books when removing a borrower
mongo.db.borrow_transactions.update_many(
    {"borrower_id": borrower_id_obj, "status": "borrowed"},
    {"$set": {"status": "returned", "return_date": datetime.now()}}
)
```

### 4. **NOT NULL Constraints**
**Books Collection:**
- `serial_number` - Required
- `title` - Required
- `author_id` - Required
- `publication_id` - Required
- `category` - Required

**Borrowers Collection:**
- `name` - Required, minimum 2 characters
- `email` - Required, unique

**Borrow Transactions:**
- `book_id` - Required
- `borrower_id` - Required
- `issue_date` - Required
- `due_date` - Required (auto-calculated)

### 5. **CHECK Constraints** (Application Level)

**Quantity Validation:**
```python
# Books must have quantity ≥ 1 to be available
if quantity_available < 1:
    return "Error: No available copies.", 400
```

**Date Validation:**
```python
# Issue date cannot be in future
if issue_date > datetime.now():
    return "Error: Issue date cannot be in future.", 400

# Due date auto-calculated as issue_date + 14 days
due_date = issue_date + timedelta(days=14)
```

**Email Format Validation:**
```python
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(pattern, email):
    return "Error: Invalid email format.", 400
```

### 6. **DUPLICATE Prevention Constraints**
- Prevent borrowing the same book twice simultaneously
  ```python
  duplicate = mongo.db.borrow_transactions.find_one({
      "book_id": book_id,
      "borrower_id": borrower_id,
      "status": "borrowed"
  })
  if duplicate:
      return "Error: Already borrowed this book.", 409
  ```

### 7. **Domain Constraints**
- **Fine Amount**: Always non-negative (₹ 0 or more)
- **Quantity**: Always positive integer
- **Status**: Only allows: `borrowed`, `returned`, `overdue`, `paid`
- **Days Overdue**: Auto-calculated from due_date

### 8. **Performance Indexes**
```python
# Unique indexes
db.books.create_index([("serial_number", 1)], unique=True)
db.borrowers.create_index([("email", 1)], unique=True)

# Regular indexes for fast queries
db.books.create_index([("category", 1)])
db.borrow_transactions.create_index([("borrower_id", 1)])
db.borrow_transactions.create_index([("status", 1)])
db.borrow_transactions.create_index([("due_date", 1)])

# Compound indexes
db.borrow_transactions.create_index([("borrower_id", 1), ("status", 1)])
db.books.create_index([("author_id", 1), ("publication_id", 1)])
```

---

## 🔗 API Routes

### **Home & Navigation**
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage displaying all books |
| `/available_books` | GET | List available books with filtering & search |
| `/borrowed_books` | GET | Show currently borrowed books |
| `/due_books` | GET | Show overdue books with fines |

### **Book Operations**
| Route | Method | Description |
|--------|--------|-------------|
| `/borrow_book` | GET, POST | Borrow a book form and processing |
| `/return_book/<transaction_id>` | POST | Return a borrowed book |

### **Borrower Management**
| Route | Method | Description |
|-------|--------|-------------|
| `/borrowers` | GET | Borrower management page |
| `/view_all_borrowers` | GET | List all borrowers |
| `/add_borrower` | POST | Register a new borrower |
| `/remove_borrower/<borrower_id>` | POST | Remove a borrower |

### **Transaction & Payment**
| Route | Method | Description |
|-------|--------|-------------|
| `/transaction_history` | GET | View all transactions |
| `/transaction_details/<transaction_id>` | GET | Detailed transaction information |
| `/payment/<transaction_id>` | GET | Payment form page |
| `/process_payment` | POST | Process fine payment |
| `/payment_receipt` | GET | Generate payment receipt |
| `/clean_returned_books` | POST | Archive returned books |

---

## 💡 Key Usage Examples

### Adding a Borrower
1. Navigate to **Borrowers** section
2. Click **Add New Borrower**
3. Fill in name and valid email
4. Click **Save**

### Borrowing a Book
1. Go to **Available Books**
2. Select desired book
3. Click **Borrow**
4. Choose borrower from dropdown
5. Confirm - Due date auto-set to 14 days

### Returning a Book
1. Go to **Borrowed Books**
2. Find the book to return
3. Click **Return Book**  
4. Fine auto-calculated if overdue
5. Proceed to payment (if fine exists)

### Paying Fines
1. Check **Overdue Books** section
2. Click **Pay Fine** on book with pending payment
3. Review fine amount and details
4. Click **Process Payment**
5. Receive digital receipt

---

## ⚙️ Configuration

Update `.env` file for custom configuration:

```env
# MongoDB Settings
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=library_management

# Flask Settings
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DEBUG=True

# Optional: Cloud MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## 🧪 Testing

### Quick Test Scenario
1. Start app: `python app.py`
2. Add a borrower via interface
3. Add some books (through MongoDB or seed script)
4. Try borrowing a book
5. Check transaction history
6. Test returning and fine calculation

### Constraint Testing
- Try duplicate serial number → Should error
- Try duplicate email → Should error
- Try borrowing with invalid borrower → Should error
- Try future issue date → Should error
- Try invalid email format → Should error

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution**: Ensure MongoDB is running
```bash
# macOS with Homebrew
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows - Run MongoDB service
```

### ModuleNotFoundError
```
Error: No module named 'flask'
```
**Solution**: Install dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port or kill existing process
```python
# In app.py, change port
app.run(debug=True, port=5001)
```

---

## 📝 License

This project is provided as-is for educational purposes.

---

## 👨‍💻 Developer Notes

- **Code Style**: PEP 8 compliant Python
- **Architecture**: MVC pattern with Flask
- **Database**: 3NF normalized MongoDB schema
- **Validation**: Multi-layer (MongoDB + Application)
- **Error Handling**: Comprehensive with user-friendly messages
- **Scalability**: Ready for production with proper indexing and constraints

---

## 🤝 Support

For issues or questions:
1. Check existing constraints documentation
2. Review MongoDB logs
3. Verify `.env` configuration
4. Check application console output

---

**Last Updated**: April 2026
**Version**: 3.0.0
**Status**: Production Ready ✅

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DB=library_db
   ```

5. **Create the database and tables**
   
   Create a MySQL database and tables with the following schema:
   
   ```sql
   CREATE DATABASE library_db;
   USE library_db;
   
   CREATE TABLE borrowers (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL
   );
   
   CREATE TABLE books (
       id INT AUTO_INCREMENT PRIMARY KEY,
       serial_number VARCHAR(50) UNIQUE NOT NULL,
       title VARCHAR(200) NOT NULL,
       author VARCHAR(100) NOT NULL,
       publication VARCHAR(100),
       borrower_id INT,
       issue_date DATE,
       due_date DATE,
       FOREIGN KEY (borrower_id) REFERENCES borrowers(id)
   );
   ```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5001`

2. **Navigate the application**
   - **Home**: View all books in the library
   - **Available Books**: See only books that are not currently borrowed
   - **Borrowed Books**: View all books currently borrowed with borrower names and due dates
   - **Borrowers**: Manage borrower records and add new borrowers
   - **Borrow Book**: Issue a book to a borrower
   - **Search**: Find specific books by title, author, or serial number

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page - view all books |
| `/available_books` | GET | View available books |
| `/borrowed_books` | GET | View currently borrowed books |
| `/borrowers` | GET | View all borrowers |
| `/add_borrower` | POST | Add a new borrower |
| `/borrow_book` | GET, POST | Borrow a book for a borrower |
| `/return_book` | POST | Return a book (on time) |
| `/return_with_penalty` | POST | Return a book (overdue) |
| `/remove_borrower` | POST | Remove a borrower |
| `/search` | GET | Search for books |

## Key Features Explained

### Automatic Due Date Calculation
When a book is borrowed, the system automatically calculates a due date 14 days from the issue date.

### Borrower Tracking
Each borrowed book is linked to a borrower. The system tracks:
- Borrower's name and email
- Issue date
- Due date
- Overdue status

### Book Status
Books can be in one of two states:
- **Available**: No borrower assigned
- **Borrowed**: Assigned to a specific borrower

## File Structure

```
library-management/
├── app.py                 # Main Flask application
├── config.py              # Configuration (commented template)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── templates/             # HTML templates
│   ├── home.html
│   ├── available_books.html
│   ├── borrowed_books.html
│   ├── borrowers.html
│   ├── borrow_book.html
│   └── navbar.html
└── static/                # Static files (CSS, JS, images)
```

## Error Handling

The application includes error handling for:
- Book not available for borrowing
- Invalid date formats
- Database connection issues
- Borrower removal with active loans

## Future Enhancements

- Implement penalty/fine calculation for overdue books
- Add user authentication and roles (admin, librarian)
- Email notifications for overdue books
- Book reservation system
- Generate reports and statistics
- Barcode/QR code scanning

## License

[Add your license information here]

## Support

For issues or questions, please contact the development team or create an issue in the repository.

## Notes

- The application runs on port 5001 by default
- Debug mode is disabled in production (`debug=False`)
- Database backups should be regularly created using `library_db_backup.sql`
