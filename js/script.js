// Search Books Function
function searchBooks() {
    let searchInput = document.getElementById('searchBar').value.toLowerCase();
    let bookList = document.getElementById('bookList');
    bookList.innerHTML = '';

    // Dummy data for now (To be replaced with AJAX or PHP later)
    let books = [
        {id: 1, title: 'Book A', author: 'Author X', genre: 'Fiction'},
        {id: 2, title: 'Book B', author: 'Author Y', genre: 'Science'},
        {id: 3, title: 'Book C', author: 'Author Z', genre: 'History'}
    ];

    books.forEach(book => {
        if (book.title.toLowerCase().includes(searchInput) ||
            book.author.toLowerCase().includes(searchInput) ||
            book.genre.toLowerCase().includes(searchInput)) {
            
            let bookItem = `
                <div class="book-item">
                    <strong>${book.title}</strong> by ${book.author} (${book.genre})
                    <button onclick="borrowBook(${book.id})">Borrow</button>
                </div>
            `;
            bookList.innerHTML += bookItem;
        }
    });
}

// Borrow Book Function (Save to Local Storage)
function borrowBook(bookId) {
    let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];
    if (borrowedBooks.length >= 3) {
        alert('You can only borrow a maximum of 3 books at a time.');
        return;
    }

    let bookTitle = `Book ${String.fromCharCode(64 + bookId)}`;
    borrowedBooks.push({id: bookId, title: bookTitle, dueDate: getDueDate()});
    localStorage.setItem('borrowedBooks', JSON.stringify(borrowedBooks));
    alert('Book borrowed successfully!');
}

// Show Borrowed Books
function loadBorrowedBooks() {
    let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];
    let bookContainer = document.getElementById('borrowedBooks');
    bookContainer.innerHTML = '';
    
    borrowedBooks.forEach((book, index) => {
        let bookItem = `
            <div class="book-item">
                <strong>${book.title}</strong> - Due Date: ${book.dueDate}
                <button onclick="returnBook(${index})">Return</button>
            </div>
        `;
        bookContainer.innerHTML += bookItem;
    });
}

// Return Book Function
function returnBook(index) {
    let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];
    borrowedBooks.splice(index, 1);
    localStorage.setItem('borrowedBooks', JSON.stringify(borrowedBooks));
    alert('Book returned successfully!');
    loadBorrowedBooks();
}

// Get Due Date (14 Days Later)
function getDueDate() {
    let today = new Date();
    today.setDate(today.getDate() + 14);
    return today.toISOString().split('T')[0];
}

// Check Due Dates and Show Alerts
function checkDueDates() {
    let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];
    let today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format

    borrowedBooks.forEach(book => {
        let dueDate = new Date(book.dueDate);
        let currentDate = new Date(today);
        let timeDiff = dueDate - currentDate;
        let daysLeft = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

        if (daysLeft === 2) {
            alert(`Reminder: "${book.title}" is due in 2 days!`);
        } else if (daysLeft < 0) {
            alert(`Alert: "${book.title}" is overdue! Please return it immediately.`);
        }
    });
}

// Check due dates when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadBorrowedBooks();  // Load borrowed books
    checkDueDates();      // Check due dates
});
