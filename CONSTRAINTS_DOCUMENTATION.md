# MongoDB Integrity Constraints Implementation

## Summary
This document outlines all the integrity constraints implemented for the Library Management System using MongoDB and Flask.

---

## 1. ✅ UNIQUE INDEXES (MongoDB Level)

### Serial Number Uniqueness
- **Collection:** `books`
- **Field:** `serial_number`
- **Type:** Unique Index
- **Impact:** Prevents duplicate book serial numbers in the system
- **Error Code:** E11000 (Duplicate Key Error)

### Email Uniqueness
- **Collection:** `borrowers`
- **Field:** `email`
- **Type:** Unique Index
- **Impact:** Ensures each borrower has a unique email address
- **Error Code:** E11000 (Duplicate Key Error)

---

## 2. ✅ SCHEMA VALIDATION (MongoDB Level)

### Books Collection Validation
```javascript
Required Fields:
- serial_number (string)
- title (string)
- author (string)
- publication (string)

Optional Fields with Type Constraints:
- quantity (integer, minimum: 1)
- borrower_id (ObjectId or null)
- issue_date (date or null)
- due_date (date or null)
```

### Borrowers Collection Validation
```javascript
Required Fields:
- name (string)
- email (string, email format regex)

Optional Fields:
- None currently
```

---

## 3. ✅ REFERENTIAL INTEGRITY (Application Level)

### Foreign Key Relationship
- **Parent:** `borrowers._id`
- **Child:** `books.borrower_id`
- **Implementation:**
  - Validate borrower exists before borrowing a book
  - Cascade delete: When removing a borrower, return all their books
  - Reference integrity check in `borrow_book()` route

**Code Example:**
```python
borrower = mongo.db.borrowers.find_one({"_id": borrower_id_obj})
if not borrower:
    return "Error: Borrower not found.", 404
```

---

## 4. ✅ QUANTITY VALIDATION (Application Level)

### Quantity > 0 Constraint
- **Collection:** `books`
- **Field:** `quantity`
- **Rule:** Must be >= 1 to borrow
- **Validation Location:** `borrow_book()` route
- **Check:**
```python
if book.get("quantity", 1) < 1:
    return "Error: Book has no available copies.", 400
```

---

## 5. ✅ DUPLICATE BORROWING PREVENTION (Application Level)

### One User-Book Combination Only
- **Rule:** A borrower cannot borrow the same book twice simultaneously
- **Validation Location:** `borrow_book()` route
- **Check:**
```python
duplicate = mongo.db.books.find_one({
    "serial_number": serial_number,
    "borrower_id": borrower_id_obj
})
if duplicate:
    return f"Error: Borrower already has '{book.get('title')}'. Duplicate borrowing not allowed.", 409
```

---

## 6. ✅ EMAIL VALIDATION (Application Level)

### Email Format Validation
- **Pattern:** RFC 5322 compliant email regex
- **Validation Function:** `validate_email(email)`
- **Validation Location:** `add_borrower()` route
- **Check:**
```python
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not validate_email(email):
    return "Error: Invalid email format.", 400
```

---

## 7. ✅ DATE CONSTRAINTS

### Issue Date Validation
- **Rule:** Cannot be in the future
- **Validation Location:** `borrow_book()` route
- **Check:**
```python
if issue_date > datetime.now():
    return "Error: Issue date cannot be in the future.", 400
```

### Due Date Calculation
- **Rule:** Automatically calculated as `issue_date + 14 days`
- **Immutable:** Cannot be manually set by user

---

## 8. ✅ REQUIRED FIELD CONSTRAINTS

### Books Collection
- `serial_number` - Required, must be string
- `title` - Required, must be string
- `author` - Required, must be string
- `publication` - Required, must be string

### Borrowers Collection
- `name` - Required, minimum 2 characters
- `email` - Required, must be unique and valid format

---

## 9. ✅ PERFORMANCE INDEXES

### Created Indexes
1. **serial_number_1** - Unique index for fast book lookup
2. **email_1** - Unique index for borrower email lookup
3. **borrower_id_1** - Index for finding books by borrower
4. **borrower_id_1_serial_number_1** - Compound index for availability checks
5. **due_date_1** - Index for overdue book queries

---

## 10. ✅ APPLICATION-LEVEL VALIDATIONS

### Input Validation
- ✅ Non-empty field validation
- ✅ Type checking for ObjectId conversions
- ✅ Date format validation (YYYY-MM-DD)
- ✅ Email format validation

### Business Logic Validation
- ✅ Book availability check (borrower_id IS NULL)
- ✅ Borrower existence check
- ✅ Duplicate borrowing prevention
- ✅ Cascade deletion (when removing borrower)

### Error Handling
- ✅ Proper HTTP status codes (400, 404, 409, 500)
- ✅ User-friendly error messages
- ✅ MongoDB error code handling (E11000)

---

## Testing Scenarios

### ✅ Test Constraint 1: Duplicate Serial Number
```
1. Try to add a book with serial number "B001" (already exists)
2. MongoDB returns E11000 error
3. Application catches and displays user-friendly error
```

### ✅ Test Constraint 2: Duplicate Email
```
1. Try to add borrower with existing email
2. Application validates and rejects
3. User sees: "Email already registered"
```

### ✅ Test Constraint 3: Invalid Email Format
```
1. Try to add borrower with invalid email
2. Regex validation fails
3. User sees: "Invalid email format"
```

### ✅ Test Constraint 4: Duplicate Borrowing
```
1. Borrower "Alice" borrows "Python Programming"
2. Try to borrow same book again for Alice
3. Application checks and rejects
4. User sees: "Borrower already has 'Python Programming'"
```

### ✅ Test Constraint 5: Quantity Check
```
1. Book with quantity 0 attempts to be borrowed
2. Application validation fails
3. User sees: "Book has no available copies"
```

### ✅ Test Constraint 6: Future Issue Date
```
1. Try to borrow book with tomorrow's date as issue_date
2. Application validation fails
3. User sees: "Issue date cannot be in the future"
```

### ✅ Test Constraint 7: Referential Integrity
```
1. Try to borrow book with non-existent borrower_id
2. Application checks borrower existence
3. User sees: "Borrower not found"
```

### ✅ Test Constraint 8: Cascade Delete
```
1. Remove a borrower who has borrowed 3 books
2. All 3 books are automatically returned (borrower_id set to NULL)
3. Books appear in "Available Books" again
4. Borrower is deleted from database
```

---

## 11. ✅ STUDENT ID & MEMBER ID CONSTRAINTS

### Student ID Uniqueness
- **Collection:** `borrowers`
- **Field:** `student_id`
- **Type:** Unique Index
- **Minimum Length:** 3 characters
- **Impact:** Ensures each borrower has a unique student ID (e.g., STU001, ADM123)
- **Error Code:** E11000 (Duplicate Key Error)
- **Validation:**
```python
if not student_id or len(student_id) < 3:
    flash("Error: Student ID must be at least 3 characters long.", "error")

existing_student_id = mongo.db.borrowers.find_one({"student_id": student_id})
if existing_student_id:
    flash(f"Error: Student ID '{student_id}' already registered.", "error")
```

### Member ID System
- **Format:** `MEM-{STUDENT_ID}-{TIMESTAMP}`
- **Example:** `MEM-STU001-1234567890`
- **Uniqueness:** Auto-generated during borrower creation
- **Purpose:** Primary identifier for member tracking and records
- **Generation Code:**
```python
member_id = f"MEM-{student_id.upper()}-{datetime.now().strftime('%s')}"
```

### Member ID Use Cases:
1. **Membership Card:** Display on physical/digital library card
2. **Borrow Transactions:** Track all borrowing history by member_id
3. **Fine Payments:** Payment records linked to member_id
4. **Statistics:** Generate member-wise borrowing reports
5. **Access Control:** Verify membership validity
6. **Audit Trail:** Track all member activities

### Borrower Record Structure:
```javascript
{
  _id: ObjectId,
  member_id: "MEM-STU001-1234567890",     // Unique member identifier
  name: "John Doe",                        // Required
  email: "john@example.com",               // Unique, required
  student_id: "STU001",                    // Unique, required
  phone: "+91-98765-43210",                // Optional, formatted
  address: "123 Main St, City",            // Optional
  created_at: ISODate("2026-04-15T10:30:00Z")
}
```

### Phone Number Validation
- **Format:** Supports multiple formats
  - International: `+91-98765-43210`
  - Parentheses: `(123) 456-7890`
  - Simple: `9876543210`
- **Regex Pattern:** `^[0-9\-\+\(\)\s]{7,}$`
- **Minimum Length:** 7 characters
- **Optional Field:** Not required
- **Validation Code:**
```python
if phone and not re.match(r'^[0-9\-\+\(\)\s]{7,}$', phone):
    flash("Error: Invalid phone number format.", "error")
```

---

## Files Modified

1. **setup_constraints.py** - New file
   - Creates MongoDB indexes
   - Applies schema validation rules
   
2. **app.py** - Updated file
   - Added validation helper functions
   - Updated all routes with constraint checks
   - Added proper error handling
   - Added email regex validation
   - Added duplicate borrowing prevention

---

## 12. ✅ MAXIMUM BOOKS PER BORROWER CONSTRAINT

### Borrowing Limit
- **Rule:** Each borrower can issue a maximum of **2 books** at any time
- **Collection:** `borrow_transactions`
- **Validation Location:** `borrow_book()` route
- **Check:**
```python
active_borrows = mongo.db.borrow_transactions.count_documents({
    "borrower_id": borrower_id_obj,
    "status": "borrowed"
})

if active_borrows >= 2:
    flash("Error: Borrower has reached the maximum limit of 2 books. Please return a book first.", "error")
```

### Rules
1. **Check Before Borrowing:** Count all active borrowed books for the borrower
2. **Reject if at Limit:** Prevent new borrow operation if borrower already has 2 active books
3. **Allow Return:** Borrowers can return books anytime
4. **Recalculate Immediately:** After returning a book, borrower can immediately borrow another

### UI Feedback
- **0 books borrowed:** ✓ Can borrow 2 books
- **1 book borrowed:** ⚠️ Can borrow 1 more book
- **2 books borrowed:** 🚫 At limit - must return a book first

### Business Rationale
- **Fair Resource Distribution:** Ensures all borrowers get equal access to library books
- **Inventory Management:** Prevents hoarding of books
- **Quality of Service:** Encourages regular returns and participation
- **Demand Balancing:** Maintains available book count for other borrowers

### Testing Scenario
```
Test: Maximum 2 Books Constraint
1. Borrower borrows Book A (Active: 1/2) ✓
2. Borrower borrows Book B (Active: 2/2) ✓
3. Try borrow Book C (Active: 2/2) ✗ REJECTED
   Error: "Borrower has reached the maximum limit of 2 books"
4. Borrower returns Book A (Active: 1/2)
5. Now can borrow Book C (Active: 2/2) ✓
```

---

## Summary Table

| Constraint | Type | Level | Status |
|-----------|------|-------|--------|
| Unique Serial Number | Uniqueness | MongoDB | ✅ Active |
| Unique Email | Uniqueness | MongoDB | ✅ Active |
| Unique Student ID | Uniqueness | MongoDB | ✅ Active |
| Unique Member ID | Uniqueness | Application | ✅ Active |
| Referential Integrity | FK | Application | ✅ Active |
| Quantity > 0 | Domain | Application | ✅ Active |
| No Duplicate Borrowing | Business Logic | Application | ✅ Active |
| Maximum 2 Books Per Borrower | Business Logic | Application | ✅ Active |
| Email Format | Format | Application | ✅ Active |
| Phone Format | Format | Application | ✅ Active |
| Student ID Min Length | Length | Application | ✅ Active |
| Issue Date Validation | Temporal | Application | ✅ Active |
| Required Fields | NOT NULL | MongoDB + App | ✅ Active |
| Performance Indexes | Performance | MongoDB | ✅ Active |

---

## Conclusion
All integrity constraints have been successfully implemented at both MongoDB and Application levels, ensuring data consistency, prevent duplicates, and enforce business rules.

All new borrowers now have:
- ✅ Unique Member ID for tracking
- ✅ Unique Student ID for identification
- ✅ Phone number with format validation
- ✅ Email uniqueness constraint
- ✅ Name with minimum length requirement
