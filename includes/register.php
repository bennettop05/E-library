<?php
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);

    // Check if username already exists
    $checkQuery = "SELECT * FROM users WHERE username = ?";
    $stmt = $conn->prepare($checkQuery);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        echo "Username already exists. Please choose another one.";
    } else {
        // Insert new user
        $insertQuery = "INSERT INTO users (username, password) VALUES (?, ?)";
        $stmt = $conn->prepare($insertQuery);
        $stmt->bind_param("ss", $username, $password);

        if ($stmt->execute()) {
            echo "Registration successful! You can now login.";
        } else {
            echo "Error during registration.";
        }
    }
}
?>
