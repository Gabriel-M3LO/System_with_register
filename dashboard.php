<?php
session_start();
include('config.php');
if (!isset($_SESSION['email'])) {
    // Redireciona para a página de login se o usuário não estiver logado
    echo "<script> location.href='login.php'; </script>";
    exit();
}

// Caso contrário, continue carregando a página normalmente
$email = $_SESSION['email'];

// Conexão com o banco de dados
$conn = new mysqli("localhost", "root", "", "login");

// Verificar conexão
if ($conn->connect_error) {
    die("Conexão falhou: " . $conn->connect_error);
}

// Extrair o domínio e o departamento do email
$email_parts = explode('@', $email);
$domain = $email_parts[1];
$department = explode('.', $email_parts[0])[1];

// Buscar arquivos relacionados ao domínio e departamento
if ($department === 'geral') {
    // Usuário geral, busca arquivos da empresa sem filtrar por departamento
    $file_stmt = $conn->prepare("SELECT file, title FROM files WHERE empresa = ?");
    $file_stmt->bind_param("s", $domain);
    echo "<script> location.href='dashboard-geral.php'; </script>";
} else {
    // Usuário de um departamento específico, busca arquivos do departamento
    $file_stmt = $conn->prepare("SELECT file, title FROM files WHERE empresa = ? AND departamento = ?");
    $file_stmt->bind_param("ss", $domain, $department);
}

$file_stmt->execute();
$file_stmt->store_result();

// Verificar se há arquivos para o domínio e departamento
$files = [];
if ($file_stmt->num_rows > 0) {
    $file_stmt->bind_result($file_path, $title);
    while ($file_stmt->fetch()) {
        $files[] = ['path' => $file_path, 'title' => $title];
    }
} else {
    $message = "Nenhum arquivo disponível para este domínio e departamento.";
}

$file_stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arquivos Disponíveis</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" style="margin-left: 15%; font-weight: bold; font-size: 20px" href="#">Gestão Remota</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="form-inline my-2 my-lg-0" id="navbarSupportedContent" style="margin-right: 15%">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item" style="float: right">
                    <a class="nav-link active" href="logout.php" tabindex="-1" aria-disabled="true">Sair</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container mt-5">
    <h3>Relatórios Disponíveis</h3>
    <?php if (!empty($files)): ?>
        <ul class="list-group">
            <?php foreach ($files as $file): ?>
                <li class="list-group-item"><a href="<?php echo $file['path']; ?>"><i class="bi bi-box-arrow-up-right       "></i><?php echo $file['title']; ?></a></li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p><?php echo $message; ?></p>
    <?php endif; ?>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
</body>
</html>
