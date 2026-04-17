from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to MongoDB
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'library_management')

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]
books_collection = db['books']

# Sample books data - Randomized order
books_data = [
    {"serial_number": "B012", "title": "Cracking the Coding Interview", "author": "Gayle McDowell", "publication": "CareerCup", "quantity_available": 5, "borrower_id": None, "isbn": "978-0-98496-816-4", "category": "Interview"},
    {"serial_number": "B048", "title": "AI Superpowers", "author": "Kai-Fu Lee", "publication": "Houghton Mifflin", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-358-10792-3", "category": "AI"},
    {"serial_number": "B003", "title": "Clean Code", "author": "Robert C. Martin", "publication": "Prentice Hall", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-13-235088-4", "category": "Software Engineering"},
    {"serial_number": "B068", "title": "You Don't Know JS", "author": "Kyle Simpson", "publication": "O'Reilly", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-491-92446-4", "category": "Programming"},
    {"serial_number": "B039", "title": "Sapiens", "author": "Yuval Noah Harari", "publication": "Harper", "quantity_available": 6, "borrower_id": None, "isbn": "978-0-06-231609-7", "category": "History"},
    {"serial_number": "B023", "title": "C++ Primer", "author": "Stanley Lippman", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-321-71411-4", "category": "Programming"},
    {"serial_number": "B086", "title": "Prompt Engineering Guide", "author": "Elvis Saravia", "publication": "Self", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-716-17848-7", "category": "AI"},
    {"serial_number": "B019", "title": "PostgreSQL Up and Running", "author": "Regina Obe", "publication": "O'Reilly", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-96271-4", "category": "Databases"},
    {"serial_number": "B091", "title": "Emotional Intelligence", "author": "Daniel Goleman", "publication": "Bantam", "quantity_available": 5, "borrower_id": None, "isbn": "978-0-553-37506-2", "category": "Psychology"},
    {"serial_number": "B057", "title": "Building Microservices", "author": "Sam Newman", "publication": "O'Reilly", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-491-95035-7", "category": "Software Engineering"},
    {"serial_number": "B042", "title": "A Brief History of Time", "author": "Stephen Hawking", "publication": "Bantam", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-553-38016-3", "category": "History"},
    {"serial_number": "B014", "title": "Learning React", "author": "Alex Banks", "publication": "O'Reilly Media", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-491-95476-0", "category": "Web Development"},
    {"serial_number": "B077", "title": "Hands-On ML", "author": "Aurélien Géron", "publication": "O'Reilly", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-491-96245-2", "category": "Machine Learning"},
    {"serial_number": "B002", "title": "JavaScript: The Good Parts", "author": "Douglas Crockford", "publication": "O'Reilly Media", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-596-51774-8", "category": "Programming"},
    {"serial_number": "B033", "title": "The Lean Startup", "author": "Eric Ries", "publication": "Crown Business", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-307-88791-7", "category": "Business"},
    {"serial_number": "B082", "title": "GPT and Transformers", "author": "Ashish Vaswani", "publication": "ArXiv", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-234-56789-1", "category": "AI"},
    {"serial_number": "B061", "title": "Programming Pearls", "author": "Jon Bentley", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-201-63361-0", "category": "Programming"},
    {"serial_number": "B074", "title": "Feature Engineering", "author": "Alice Zheng", "publication": "O'Reilly", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-95325-9", "category": "Machine Learning"},
    {"serial_number": "B054", "title": "Kubernetes in Action", "author": "Marko Luksa", "publication": "Manning", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-617-29455-6", "category": "Web Development"},
    {"serial_number": "B095", "title": "Man's Search for Meaning", "author": "Viktor Frankl", "publication": "Random House", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-807-04127-8", "category": "Psychology"},
    {"serial_number": "B009", "title": "Introduction to Algorithms", "author": "Cormen & Leiserson", "publication": "MIT Press", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-262-03384-8", "category": "Algorithms"},
    {"serial_number": "B038", "title": "Zero to One", "author": "Peter Thiel", "publication": "Crown Business", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-553-41887-0", "category": "Business"},
    {"serial_number": "B071", "title": "TensorFlow in Practice", "author": "Aurélien Géron", "publication": "O'Reilly", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-97281-2", "category": "Machine Learning"},
    {"serial_number": "B045", "title": "The Selfish Gene", "author": "Richard Dawkins", "publication": "Oxford", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-19-288223-8", "category": "Science"},
    {"serial_number": "B056", "title": "Domain-Driven Design", "author": "Eric Evans", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-321-12521-7", "category": "Software Engineering"},
    {"serial_number": "B017", "title": "Node.js Design Patterns", "author": "Mario Casciaro", "publication": "Packt Publishing", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-785-88555-7", "category": "Web Development"},
    {"serial_number": "B040", "title": "Mindset", "author": "Carol S. Dweck", "publication": "Random House", "quantity_available": 5, "borrower_id": None, "isbn": "978-0-345-47232-8", "category": "Psychology"},
    {"serial_number": "B029", "title": "Deep Learning", "author": "Ian Goodfellow", "publication": "MIT Press", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-262-03561-3", "category": "Machine Learning"},
    {"serial_number": "B085", "title": "Hallucinations in LLMs", "author": "Rashmi Bansal", "publication": "ACM", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-234-56789-4", "category": "AI"},
    {"serial_number": "B010", "title": "Data Structures and Algorithms", "author": "Mark Allen Weiss", "publication": "Longman", "quantity_available": 3, "borrower_id": None, "isbn": "978-81-942847-8-0", "category": "Algorithms"},
    {"serial_number": "B052", "title": "Elasticsearch: The Definitive Guide", "author": "Clinton Gormley", "publication": "O'Reilly", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-92205-1", "category": "Databases"},
    {"serial_number": "B066", "title": "Ruby on Rails Tutorial", "author": "Michael Hartl", "publication": "Addison-Wesley", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-134-07957-0", "category": "Web Development"},
    {"serial_number": "B049", "title": "The Fourth Industrial Revolution", "author": "Klaus Schwab", "publication": "Crown Business", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-385-54258-3", "category": "Business"},
    {"serial_number": "B021", "title": "Java: The Complete Reference", "author": "Herbert Schildt", "publication": "McGraw-Hill", "quantity_available": 5, "borrower_id": None, "isbn": "978-1-260-44206-6", "category": "Programming"},
    {"serial_number": "B041", "title": "The Art of War", "author": "Sun Tzu", "publication": "Dover", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-486-42654-9", "category": "History"},
    {"serial_number": "B015", "title": "Angular Up and Running", "author": "Shyam Seshadri", "publication": "O'Reilly Media", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-92159-7", "category": "Web Development"},
    {"serial_number": "B090", "title": "AI Ethics in Practice", "author": "Luciano Floridi", "publication": "Oxford", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-198-05260-5", "category": "AI"},
    {"serial_number": "B073", "title": "Scikit-Learn Guide", "author": "Andreas Müller", "publication": "O'Reilly", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-96848-8", "category": "Machine Learning"},
    {"serial_number": "B001", "title": "Python Programming", "author": "Guido van Rossum", "publication": "O'Reilly Media", "quantity_available": 5, "borrower_id": None, "isbn": "978-0-13-110362-7", "category": "Programming"},
    {"serial_number": "B046", "title": "Cosmos", "author": "Carl Sagan", "publication": "Random House", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-394-50294-5", "category": "Science"},
    {"serial_number": "B060", "title": "Scrum: The Art of Doing Twice the Work", "author": "Jeff Sutherland", "publication": "Crown Business", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-553-41881-8", "category": "Project Management"},
    {"serial_number": "B007", "title": "Refactoring", "author": "Martin Fowler", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-13-468599-1", "category": "Software Engineering"},
    {"serial_number": "B072", "title": "PyTorch Tutorials", "author": "Soumith Chintala", "publication": "Self", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-616-77003-9", "category": "Machine Learning"},
    {"serial_number": "B026", "title": "Rust Programming Language", "author": "Steve Klabnik", "publication": "No Starch Press", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-491-92728-4", "category": "Programming"},
    {"serial_number": "B101", "title": "The Pragmatic Agile Developer", "author": "Dale Emery", "publication": "Addison-Wesley", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-321-61411-7", "category": "Project Management"},
    {"serial_number": "B092", "title": "Principles", "author": "Ray Dalio", "publication": "Simon Schuster", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-501-21339-6", "category": "Business"},
    {"serial_number": "B047", "title": "The Elegant Universe", "author": "Brian Greene", "publication": "Vintage", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-375-70811-4", "category": "Science"},
    {"serial_number": "B084", "title": "Attention is All You Need", "author": "Ashish Vaswani", "publication": "NeurIPS", "quantity_available": 1, "borrower_id": None, "isbn": "978-1-234-56789-3", "category": "AI"},
    {"serial_number": "B020", "title": "Redis in Action", "author": "Josiah Carlson", "publication": "Manning", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-617-29529-2", "category": "Databases"},
    {"serial_number": "B024", "title": "C# Player's Guide", "author": "RB Whitaker", "publication": "Independent", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-491-97278-2", "category": "Programming"},
    {"serial_number": "B037", "title": "The Innovator's Dilemma", "author": "Clayton Christensen", "publication": "Harvard Business", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-06-052199-8", "category": "Business"},
    {"serial_number": "B069", "title": "The JavaScript Way", "author": "Baptiste Pesquet", "publication": "Leanpub", "quantity_available": 2, "borrower_id": None, "isbn": "978-2-9570-8480-4", "category": "Programming"},
    {"serial_number": "B005", "title": "The Pragmatic Programmer", "author": "David Thomas", "publication": "Addison-Wesley", "quantity_available": 6, "borrower_id": None, "isbn": "978-0-13-595705-9", "category": "Software Engineering"},
    {"serial_number": "B078", "title": "Neural Networks from Scratch", "author": "Harrison Kinney", "publication": "Self", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-916-13381-4", "category": "Machine Learning"},
    {"serial_number": "B018", "title": "MongoDB: The Definitive Guide", "author": "Shannon Bradshaw", "publication": "O'Reilly Media", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-491-95424-1", "category": "Databases"},
    {"serial_number": "B011", "title": "The Art of Computer Programming", "author": "Donald Knuth", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-201-89683-1", "category": "Algorithms"},
    {"serial_number": "B093", "title": "Drive", "author": "Daniel Pink", "publication": "Riverhead", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-594-48760-8", "category": "Psychology"},
    {"serial_number": "B006", "title": "Code Complete", "author": "Steve McConnell", "publication": "Microsoft Press", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-7356-1967-8", "category": "Software Engineering"},
    {"serial_number": "B036", "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "publication": "Farrar Straus Giroux", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-374-27563-1", "category": "Psychology"},
    {"serial_number": "B097", "title": "The Innovators", "author": "Walter Isaacson", "publication": "Simon Schuster", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-476-70830-3", "category": "History"},
    {"serial_number": "B051", "title": "SQL Performance Explained", "author": "Markus Winand", "publication": "Self", "quantity_available": 2, "borrower_id": None, "isbn": "978-3-950307-12-0", "category": "Databases"},
    {"serial_number": "B087", "title": "LLM Agents and Tools", "author": "Harrison Chase", "publication": "LangChain", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-716-17849-4", "category": "AI"},
    {"serial_number": "B013", "title": "Web Development with Django", "author": "Adrian Holovaty", "publication": "Apress", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-617-29398-4", "category": "Web Development"},
    {"serial_number": "B079", "title": "Reinforcement Learning", "author": "Richard Sutton", "publication": "MIT Press", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-262-03924-6", "category": "Machine Learning"},
    {"serial_number": "B064", "title": "Advanced C Programming", "author": "Paul Wang", "publication": "Mitchell McGraw", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-028-64486-3", "category": "Programming"},
    {"serial_number": "B030", "title": "Natural Language Processing", "author": "Dan Jurafsky", "publication": "Stanford", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-492-05807-8", "category": "Machine Learning"},
    {"serial_number": "B008", "title": "The Mythical Man-Month", "author": "Fred Brooks", "publication": "Addison-Wesley", "quantity_available": 1, "borrower_id": None, "isbn": "978-0-201-63361-0", "category": "Project Management"},
    {"serial_number": "B058", "title": "Release It!", "author": "Michael T. Nygard", "publication": "Pragmatic", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-680-50239-8", "category": "Software Engineering"},
    {"serial_number": "B096", "title": "Thinking in Systems", "author": "Donella Meadows", "publication": "Chelsea Green", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-603-58009-7", "category": "Science"},
    {"serial_number": "B004", "title": "Design Patterns", "author": "Gang of Four", "publication": "Addison-Wesley", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-201-63361-0", "category": "Software Engineering"},
    {"serial_number": "B081", "title": "Protein Folding AI", "author": "John Jumper", "publication": "Science", "quantity_available": 1, "borrower_id": None, "isbn": "978-1-234-56789-0", "category": "AI"},
    {"serial_number": "B099", "title": "The Code Breaker", "author": "Walter Isaacson", "publication": "Simon Schuster", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-524-87365-7", "category": "History"},
    {"serial_number": "B065", "title": "Perl Programming", "author": "Randal Schwartz", "publication": "O'Reilly", "quantity_available": 1, "borrower_id": None, "isbn": "978-0-596-00027-8", "category": "Programming"},
    {"serial_number": "B075", "title": "Practical Statistics for Data Science", "author": "Andrew Bruce", "publication": "O'Reilly", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-491-95232-0", "category": "Machine Learning"},
    {"serial_number": "B022", "title": "Effective Java", "author": "Joshua Bloch", "publication": "Addison-Wesley", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-134-68599-1", "category": "Programming"},
    {"serial_number": "B050", "title": "Competing Against Luck", "author": "Clayton Christensen", "publication": "Harper Business", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-06-243713-1", "category": "Business"},
    {"serial_number": "B062", "title": "The C Programming Language", "author": "Brian Kernighan", "publication": "Prentice Hall", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-131-10362-7", "category": "Programming"},
    {"serial_number": "B032", "title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "publication": "Prentice Hall", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-136-04259-9", "category": "AI"},
    {"serial_number": "B044", "title": "Guns, Germs, and Steel", "author": "Jared Diamond", "publication": "Norton", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-393-31756-5", "category": "History"},
    {"serial_number": "B016", "title": "Vue.js in Action", "author": "Erik Hanchuk", "publication": "Manning", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-617-29494-3", "category": "Web Development"},
    {"serial_number": "B089", "title": "Responsible AI", "author": "Juan Carlos Niebles", "publication": "Stanford", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-234-56789-6", "category": "AI"},
    {"serial_number": "B076", "title": "Data Science from Scratch", "author": "Joel Grus", "publication": "O'Reilly", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-492-04113-9", "category": "Machine Learning"},
    {"serial_number": "B031", "title": "Computer Vision", "author": "Richard Szeliski", "publication": "Springer", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-96189-1", "category": "Machine Learning"},
    {"serial_number": "B063", "title": "UNIX Programming Environment", "author": "Brian Kernighan", "publication": "Prentice Hall", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-139-370307", "category": "Programming"},
    {"serial_number": "B088", "title": "Multimodal AI", "author": "Jiasen Lu", "publication": "Meta AI", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-234-56789-5", "category": "AI"},
    {"serial_number": "B028", "title": "Machine Learning Basics", "author": "Yoshua Bengio", "publication": "MIT Press", "quantity_available": 4, "borrower_id": None, "isbn": "978-1-491-93816-7", "category": "Machine Learning"},
    {"serial_number": "B035", "title": "Good to Great", "author": "Jim Collins", "publication": "HarperBusiness", "quantity_available": 5, "borrower_id": None, "isbn": "978-0-06-662099-2", "category": "Business"},
    {"serial_number": "B083", "title": "BERT Explained", "author": "Jacob Devlin", "publication": "Google", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-234-56789-2", "category": "AI"},
    {"serial_number": "B043", "title": "The Structure of Scientific Revolutions", "author": "Thomas Kuhn", "publication": "University Chicago", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-226-45808-3", "category": "History"},
    {"serial_number": "B055", "title": "Microservices Architecture", "author": "Sam Newman", "publication": "O'Reilly", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-491-94036-5", "category": "Web Development"},
    {"serial_number": "B027", "title": "Swift Programming Language", "author": "Apple Inc.", "publication": "Apple", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-491-95825-6", "category": "Programming"},
    {"serial_number": "B094", "title": "Atomic Habits", "author": "James Clear", "publication": "Avery", "quantity_available": 6, "borrower_id": None, "isbn": "978-0-735-21159-7", "category": "Psychology"},
    {"serial_number": "B070", "title": "Frontend Masters Guide", "author": "Kyle Simpson", "publication": "Self", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-716-18505-9", "category": "Web Development"},
    {"serial_number": "B053", "title": "Docker in Action", "author": "Jeff Nickoloff", "publication": "Manning", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-617-29429-7", "category": "Web Development"},
    {"serial_number": "B059", "title": "The Phoenix Project", "author": "Gene Kim", "publication": "IT Revolution", "quantity_available": 3, "borrower_id": None, "isbn": "978-0-988-26219-9", "category": "Project Management"},
    {"serial_number": "B034", "title": "Startup Way", "author": "Eric Ries", "publication": "Crown Business", "quantity_available": 2, "borrower_id": None, "isbn": "978-0-374-53981-8", "category": "Business"},
    {"serial_number": "B098", "title": "Steve Jobs Biography", "author": "Walter Isaacson", "publication": "Simon Schuster", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-451-65817-6", "category": "History"},
    {"serial_number": "B067", "title": "Eloquent JavaScript", "author": "Marijn Haverbeke", "publication": "No Starch Press", "quantity_available": 3, "borrower_id": None, "isbn": "978-1-593-27516-2", "category": "Programming"},
    {"serial_number": "B100", "title": "Cracking the Coding Interview Pro", "author": "Gayle McDowell", "publication": "CareerCup", "quantity_available": 4, "borrower_id": None, "isbn": "978-0-984-78170-9", "category": "Interview"},
    {"serial_number": "B080", "title": "Computer Vision Applications", "author": "Joseph Redmon", "publication": "Self", "quantity_available": 1, "borrower_id": None, "isbn": "978-1-719-03481-2", "category": "Machine Learning"},
    {"serial_number": "B025", "title": "Go in Action", "author": "William Kennedy", "publication": "Manning", "quantity_available": 2, "borrower_id": None, "isbn": "978-1-617-29393-9", "category": "Programming"},
]

# Insert books into the collection
try:
    # Clear existing books
    books_collection.delete_many({})
    
    result = books_collection.insert_many(books_data)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} books into MongoDB!")
    print(f"Database: {MONGODB_DB}")
    print(f"Collection: books")
    print(f"\nBooks inserted:")
    for i, book_id in enumerate(result.inserted_ids, 1):
        print(f"  {i}. {book_id}")
        
except Exception as e:
    print(f"❌ Error inserting books: {e}")

client.close()
