<?php

class Product
{
    private int $idDepartamentos;
    private string $nome;
    private string $descricao;
    private string $imagem;

    /**
     * @param int $idDepartamentos
     * @param string $nome
     * @param string $descricao
     * @param string $imagem
     */
    public function __construct(int $idDepartamentos, string $nome, string $descricao, string $imagem)
    {
        $this->idDepartamentos = $idDepartamentos;
        $this->nome = $nome;
        $this->descricao = $descricao;
        $this->imagem = $imagem;
    }

    public function getIdDepartamentos(): int
    {
        return $this->idDepartamentos;
    }

    public function getNome(): string
    {
        return $this->nome;
    }

    public function getDescricao(): string
    {
        return $this->descricao;
    }

    public function getImagem(): string
    {
        return $this->imagem;
    }

    public function getImagens(): string
    {
        return  "img/" . $this->imagem;
    }


}