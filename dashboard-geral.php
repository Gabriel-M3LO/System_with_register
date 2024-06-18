<?php

    require "src/config.php";
    require "src/Model/Product.php";
    require "src/repository/DepartamentosRepositorio.php";

    $DepartamentosRepositorio = new DepartamentosRepositorio($pdo);
    $dadosEmpresa = $DepartamentosRepositorio-> opcoesDepartamentos();

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
        <a class="navbar-brand" style="margin-left: 150px; font-weight: bold; font-size: 20px" href="#">Gestao Remota</a>
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
<div class="container">
    <div class="row">
        <?php foreach ($dadosEmpresa as $Empresa): ?>
            <div class="card" style="width: 18rem; margin-left: 35px; margin-top: 35px">
                <img src="<?=$Empresa->getImagens()?>" class="card-img-top" alt="..." style="width: 270px; height: 170px">
                <div class="card-body">
                    <h5 class="card-title"><?= $Empresa->getNome() ?></h5>
                    <p class="card-text"><?= $Empresa->getDescricao() ?></p>
                    <a href="#" class="btn btn-primary">clique aqui</a>
                </div>
            </div>
        <?php endforeach; ?>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
</body>
</html>
