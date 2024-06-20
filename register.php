<?php
session_start();

include('db_config.php');

// Protegendo as entradas contra SQL Injection
$usuario = $conn->real_escape_string($_POST['usuario']);
$senha = $conn->real_escape_string($_POST['senha']);
$email = $conn->real_escape_string($_POST['Email']);

// Verificando se o usuário já existe
$sql = "SELECT * FROM usuarios WHERE email = '$email'";
$res = $conn->query($sql);

if ($res->num_rows > 0) {
    echo "<script>alert('Usuário ou Email já existe');</script>";
    echo "<script>location.href='register.html';</script>";
    exit();
}

// Inserindo o novo usuário no banco de dados
$sql = "INSERT INTO usuarios (usuario, senha, email) VALUES ('$usuario', '$senha', '$email')";
if ($conn->query($sql) === TRUE) {
    echo "<script>alert('Usuário registrado com sucesso');</script>";
    echo "<script>location.href='index.php';</script>";
} else {
    echo "Erro: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>