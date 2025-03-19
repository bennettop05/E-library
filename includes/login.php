<?php
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Check user credentials
    $checkQuery = "SELECT * FROM users WHERE username = ?";
    $stmt = $conn->prepare($checkQuery);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        $user = $result->fetch_assoc();
        // Verify password
        if (password_verify($password, $user['password'])) {
            session_start();
            $_SESSION['user_id'] = $user['id'];
            header("Location: ../dashboard.html");
        } else {
            echo "Invalid password. Please try again.";
        }
    } else {
        echo "User not found. Please register first.";
    }
}
?>
