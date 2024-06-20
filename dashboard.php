<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}

require 'src/db_config.php';
require 'src/model/Arquivo.php';

// Exemplo de exibição de dados específicos do usuário logado
$dadosArquivos = [];

if ($_SESSION['role'] === 'general') {
    $sql = "SELECT Title, link, Img, Departamento, Empresa FROM files";
    $stmt = $conn->prepare($sql);
} else {
    $sql = "SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = ? AND Empresa = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $_SESSION['departamento'], $_SESSION['empresa']);
}

$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $arquivo = new Arquivo($row['Title'], $row['link'], $row['Img'], $row['Departamento'], $row['Empresa']);
        $dadosArquivos[] = $arquivo;
    }
} else {
    echo "0 resultados";
}

$stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Gestão Remota</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="dashboard.php">Dashboard</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="logout.php">Sair</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container">
    <h2>Bem-vindo, <?php echo $_SESSION['email']; ?></h2>
    <p>Departamento: <?php echo $_SESSION['departamento']; ?></p>
    <p>Empresa: <?php echo $_SESSION['empresa']; ?></p>

    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#cadastrarModal">
        Cadastrar
    </button>

    <div class="row">
        <?php foreach ($dadosArquivos as $arquivo): ?>
            <div class="card" style="width: 18rem; margin: 15px;">
                <img src="<?= "img/" . $arquivo->getImg() ?>" class="card-img-top" alt="..." style="width: 270px; height: 170px">
                <div class="card-body">
                    <h5 class="card-title"><?= $arquivo->getTitle() ?></h5>
                    <p class="card-text">Departamento: <?= $arquivo->getDepartamento() ?></p>
                    <p class="card-text">Empresa: <?= $arquivo->getEmpresa() ?></p>
                    <a href="<?= $arquivo->getLink() ?>" class="btn btn-primary">Clique aqui</a>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>

<!-- Modal -->
<div class="modal fade" id="cadastrarModal" tabindex="-1" aria-labelledby="cadastrarModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <form action="cadastrar_arquivo.php" method="post" enctype="multipart/form-data">
                <div class="modal-header">
                    <h5 class="modal-title" id="cadastrarModalLabel">Cadastrar Novo Arquivo</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label for="title" class="form-label">Título</label>
                        <input type="text" class="form-control" id="title" name="title" required>
                    </div>
                    <div class="mb-3">
                        <label for="link" class="form-label">Link</label>
                        <input type="text" class="form-control" id="link" name="link" required>
                    </div>
                    <div class="mb-3">
                        <label for="img" class="form-label">Imagem</label>
                        <input type="file" class="form-control" id="img" name="img" required>
                    </div>
                    <div class="mb-3">
                        <label for="departamento" class="form-label">Departamento</label>
                        <input type="text" class="form-control" id="departamento" name="departamento" required>
                    </div>
                    <div class="mb-3">
                        <label for="empresa" class="form-label">Empresa</label>
                        <input type="text" class="form-control" id="empresa" name="empresa" required>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <button type="submit" class="btn btn-primary">Cadastrar</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"
        integrity="sha384-eMN6wGhxxKoVPKaI5t2eK2eA6dP/8Kti1VvRQl6UGVg6nsWv8F+V/Ly9Ll7B6p0v" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js"
        integrity="sha384-cVKIPhG0X1if5iDqJ7GSwkWkD1yIAqzplPBkM/3peOuO/oT7VQ5lPQvZ6zdWH/J+" crossorigin="anonymous"></script>
</body>
</html>
