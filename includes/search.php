<?php
include 'db.php';

$searchTerm = strtolower($_GET['query']);

// Search query
$query = "SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(genre) LIKE ?";
$stmt = $conn->prepare($query);
$searchTerm = "%$searchTerm%";
$stmt->bind_param("sss", $searchTerm, $searchTerm, $searchTerm);
$stmt->execute();
$result = $stmt->get_result();

$books = [];
while ($row = $result->fetch_assoc()) {
    $books[] = $row;
}

echo json_encode($books);
?>
