<?php
session_start();
require 'Repository/db_config.php';

$title = $_POST['title'];
$link = $_POST['link'];
$departamento = $_POST['departamento'];
$empresa = $_POST['empresa'];
$img = $_FILES['img']['name'];

// Diretório de destino para o upload da imagem
$target_dir = "img/";
$target_file = $target_dir . basename($img);
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

// Verifica se o arquivo é uma imagem real
$check = getimagesize($_FILES['img']['tmp_name']);
if ($check !== false) {
    // Faz o upload da imagem
    if (move_uploaded_file($_FILES['img']['tmp_name'], $target_file)) {
        // Insere os dados no banco de dados
        $stmt = $conn->prepare("INSERT INTO files (Title, link, Img, Departamento, Empresa) VALUES (?, ?, ?, ?, ?)");
        $stmt->bind_param("sssss", $title, $link, $img, $departamento, $empresa);

        if ($stmt->execute()) {
            header("Location: dashboard.php");
        } else {
            echo "Erro ao cadastrar arquivo.";
        }

        $stmt->close();
    } else {
        echo "Erro ao fazer upload da imagem.";
    }
} else {
    echo "O arquivo não é uma imagem.";
}

$conn->close();
?>
