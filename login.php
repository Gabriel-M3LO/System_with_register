<?php
session_start();

if (empty($_POST) || empty($_POST["email"]) || empty($_POST["senha"])) {
    echo "<script>location.href='index.php';</script>";
    exit();
}

include ('config.php');

$email = $conn->real_escape_string($_POST['email']);
$senha = $conn->real_escape_string($_POST['senha']);

$sql = "SELECT * FROM usuarios WHERE email = '$email' AND senha = '$senha'";

$res = $conn->query($sql) or die($conn->error);

$row = $res->fetch_object();

$qtd = $res->num_rows;

if ($qtd > 0) {
    $_SESSION["email"] = $email;
    $_SESSION["senha"] = $row->senha;
    echo "<script>location.href='dashboard.php';</script>";
    exit();
} else {
    echo "<script>alert('Usuário e/ou senha incorreto(s)');</script>";
    echo "<script>location.href='index.php';</script>";
    exit();
}

?>