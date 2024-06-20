<?php
session_start();
require 'src/db_config.php';

$email = $_POST['email'];
$password = $_POST['password'];

// Prepare a consulta SQL para evitar SQL Injection
$stmt = $conn->prepare("SELECT idusers, password, departamento, empresa, role FROM users WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    $stmt->bind_result($id, $hashed_password, $departamento, $empresa, $role);
    $stmt->fetch();

    // Verifica se a senha está correta
    if ($password === $hashed_password) {  // Comparação direta de senha em texto plano
        // Armazena informações na sessão
        $_SESSION['user_id'] = $id;
        $_SESSION['email'] = $email;
        $_SESSION['departamento'] = $departamento;
        $_SESSION['empresa'] = $empresa;
        $_SESSION['role'] = $role;
        header("Location: dashboard.php");
    } else {
        header("Location: index.php?error=Senha incorreta.");
    }
} else {
    header("Location: index.php?error=Usuário não encontrado.");
}

$stmt->close();
$conn->close();
?>
