<?php
class Empresa {
    private $nome;
    private $descricao;
    private $link;
    private $imagem;

    public function __construct($nome, $descricao, $link, $imagem) {
        $this->nome = $nome;
        $this->descricao = $descricao;
        $this->link = $link;
        $this->imagem = $imagem;
    }

    public function getNome() {
        return $this->nome;
    }

    public function getDescricao() {
        return $this->descricao;
    }

    public function getLink() {
        return $this->link;
    }

    public function getImagem() {
        return $this->imagem;
    }
}
?>
