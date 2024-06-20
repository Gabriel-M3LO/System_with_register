<?php
require 'src/db_config.php';
require 'src/Model/Arquivo.php';

$dadosArquivos = [];

$sql = "SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = 'Financeiro'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $arquivo = new Arquivo($row['Title'], $row['link'], $row['Img'], $row['Departamento'], $row['Empresa']);
        $dadosArquivos[] = $arquivo;
    }
} else {
    echo "0 resultados";
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arquivos Financeiros</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
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
                    <a class="nav-link active" aria-current="page" href="logout.php">Sair</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div class="container">
    <div class="row">
        <?php foreach ($dadosArquivos as $arquivo): ?>
            <div class="card" style="width: 18rem; margin-left: 35px; margin-top: 35px">
                <img src="<?="img/".$arquivo->getImg()?>" class="card-img-top" alt="..." style="width: 270px; height: 170px">
                <div class="card-body">
                    <h5 class="card-title"><?= $arquivo->getTitle() ?></h5>
                    <p class="card-text">Departamento: <?= $arquivo->getDepartamento() ?></p>
                    <p class="card-text">Empresa: <?= $arquivo->getEmpresa() ?></p>
                    <a href="<?= $arquivo->getLink()?>" class="btn btn-primary">Clique aqui</a>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
</body>
</html>
