<?php

class DepartamentosRepositorio
{
    private PDO $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    public function getDepartamentos(): array
    {
        $stmt = $this->db->prepare('SELECT * FROM departamentos');
        $stmt->execute();
        $departamentos = $stmt->fetchAll(PDO::FETCH_ASSOC);

        return array_map(function ($departamento) {
            return new Product(
                $departamento['idDepartamentos'],
                $departamento['nome'],
                $departamento['descricao'],
                $departamento['imagem'],
                $departamento['link'],
                $departamento['idFiles'],
                $departamento['title'] ?? '',
                $departamento['linkDashboard'] ?? '',
                $departamento['img'] ?? ''
            );
        }, $departamentos);
    }
}

?>
