<?php

class DashboardsRepositorio
{
    private PDO $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    public function getArquivosFinanceiros(): array
    {
        $stmt = $this->db->prepare('SELECT * FROM files');
        $stmt->execute();
        $arquivos = $stmt->fetchAll(PDO::FETCH_ASSOC);

        return array_map(function ($arquivo) {
            return new Product(
                $arquivo['idDepartamentos'],
                $arquivo['nome'],
                $arquivo['descricao'],
                $arquivo['imagem'],
                $arquivo['link'],
                $arquivo['idFiles'],
                $arquivo['title'] ?? '',
                $arquivo['linkDashboard'] ?? '',
                $arquivo['img'] ?? ''
            );
        }, $arquivos);
    }
}

?>
