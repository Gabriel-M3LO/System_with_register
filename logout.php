<?php
session_start();
unset($_SESSION['email']);
unset($_SESSION['senha']);
session_destroy();
header("location:http://localhost/Controle_Gestao_Correta/index.php");
?>