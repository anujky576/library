# Library Management System

A Flask-based web application for managing a library's book inventory and borrower records. This system allows librarians to track books, manage borrowers, and handle book lending operations efficiently.

## Features

- 📚 **Book Management**: View all books, search by title/author/serial number
- 🆓 **Availability Tracking**: See which books are available and which are currently borrowed
- 👥 **Borrower Management**: Add, view, and remove borrowers
- 🔄 **Lending Operations**:
  - Borrow books with automatic due date calculation (14 days)
  - Return books on time or with penalty
  - Track overdue books
- 🔍 **Search Functionality**: Find books quickly by title, author, or serial number
- 📋 **Borrowing History**: View all borrowed books and borrower details

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Frontend**: Jinja2 templates with HTML
- **Database Driver**: Flask-MySQLdb
- **Environment Management**: python-dotenv

## Requirements

- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd library-management
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

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
