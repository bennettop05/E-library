<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user_id'])) {
    echo "You need to login first.";
    exit();
}

$userId = $_SESSION['user_id'];
$bookId = $_POST['book_id'];

// Check if the user has borrowed 3 books already
$query = "SELECT COUNT(*) as total FROM borrowed_books WHERE user_id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("i", $userId);
$stmt->execute();
$result = $stmt->get_result();
$data = $result->fetch_assoc();

if ($data['total'] >= 3) {
    echo "You can only borrow 3 books at a time.";
    exit();
}

// Check if the book is available
$query = "SELECT available FROM books WHERE id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("i", $bookId);
$stmt->execute();
$result = $stmt->get_result();
$book = $result->fetch_assoc();

if ($book['available'] <= 0) {
    echo "This book is not available.";
    exit();
}

// Borrow book
$dueDate = date('Y-m-d', strtotime("+14 days"));
$query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, due_date) VALUES (?, ?, NOW(), ?)";
$stmt = $conn->prepare($query);
$stmt->bind_param("iis", $userId, $bookId, $dueDate);

if ($stmt->execute()) {
    // Update book availability
    $updateQuery = "UPDATE books SET available = available - 1 WHERE id = ?";
    $stmt = $conn->prepare($updateQuery);
    $stmt->bind_param("i", $bookId);
    $stmt->execute();

    echo "Book borrowed successfully! Due date: $dueDate";
} else {
    echo "Error borrowing the book.";
}
?>
