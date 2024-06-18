<?php

class DepartamentosRepositorio
{
    private PDO $pdo;

    /**
     * @param PDO $pdo
     */
    public function __construct(PDO $pdo)
    {
        $this->pdo = $pdo;
    }

    public function opcoesDepartamentos() :array
    {
        $sql1 = "SELECT * FROM departamentos";
        $statement = $this->pdo->query($sql1);
        $depEmpresa = $statement->fetchAll(pdo::FETCH_ASSOC);

        $dadosEmpresa = array_map(function ($Empresa) {
            return new Product($Empresa['idDepartamentos'],
                $Empresa['Nome'],
                $Empresa['Descricao'],
                $Empresa['Imagem']
            );
        }, $depEmpresa);
        return $dadosEmpresa;
    }
}