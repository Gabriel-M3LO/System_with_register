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

// Buscar todos os arquivos, independentemente do departamento
$file_stmt = $conn->prepare("SELECT id, file, title, empresa, departamento FROM files");
$file_stmt->execute();
$file_stmt->store_result();

// Verificar se há arquivos disponíveis
$files = [];
if ($file_stmt->num_rows > 0) {
    $file_stmt->bind_result($id, $file_path, $title, $empresa, $departamento);
    while ($file_stmt->fetch()) {
        $files[] = ['id' => $id, 'path' => $file_path, 'title' => $title, 'empresa' => $empresa, 'departamento' => $departamento];
    }
} else {
    $message = "Nenhum arquivo disponível.";
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
        <table class="table">
            <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Titulo</th>
                <th scope="col">Empresa</th>
                <th scope="col">Departamento</th>
            </tr>
            </thead>
            <tbody>
            <?php foreach ($files as $file): ?>
                <tr>
                    <th scope="row"><?php echo $file['id']; ?></th>
                    <td><?php echo $file['title']; ?></td>
                    <td><?php echo $file['empresa']; ?></td>
                    <td><?php echo $file['departamento']; ?></td>
                </tr>
            <?php endforeach; ?>
            </tbody>
        </table>
    <?php else: ?>
        <p><?php echo $message; ?></p>
    <?php endif; ?>


    <form>
        <div class="form-group">
            <label for="inputTitulo">Título da Dashboard</label>
            <input style="width: 400px" type="Dashboard" class="form-control" id="exampleInputEmail1"
                   aria-describedby="emailHelp" placeholder="Título">
        </div>
        <div class="full-height-div d-flex justify-content-start align-items-start" style="margin-top: 10px">
            <div class="form-group">
                <label for="inputDepartamento">Departamento</label>
                <input style="width: 200px" type="Departamento" class="form-control" id="exampleInputDepartamento"
                       placeholder="Departamento">
            </div>
            <div class="form-group">
                <label style="margin-left: 10px"; for="inputSetor">Setor</label>
                <input style="width: 190px; margin-left: 10px" type="Setor" class="form-control" id="exampleInputSetor"
                       placeholder="Setor">
            </div>
        </div>
        <button style="margin-top: 8px" type="submit" class="btn btn-primary">Enviar</button>
    </form>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
</body>
</html>
