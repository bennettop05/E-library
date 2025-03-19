<?php
session_start();
include 'db.php';

if (!isset($_SESSION['user_id'])) {
    echo "You need to login first.";
    exit();
}

$userId = $_SESSION['user_id'];
$borrowId = $_POST['borrow_id'];

// Get book ID
$query = "SELECT book_id FROM borrowed_books WHERE id = ? AND user_id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("ii", $borrowId, $userId);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 0) {
    echo "Book not found or already returned.";
    exit();
}

$book = $result->fetch_assoc();
$bookId = $book['book_id'];

// Delete record from borrowed_books
$query = "DELETE FROM borrowed_books WHERE id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("i", $borrowId);

if ($stmt->execute()) {
    // Update book availability
    $updateQuery = "UPDATE books SET available = available + 1 WHERE id = ?";
    $stmt = $conn->prepare($updateQuery);
    $stmt->bind_param("i", $bookId);
    $stmt->execute();

    echo "Book returned successfully!";
} else {
    echo "Error returning the book.";
}
?>
