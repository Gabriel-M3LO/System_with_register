<?php
class Arquivo {
    private $title;
    private $link;
    private $img;
    private $departamento;
    private $empresa;

    public function __construct($title, $link, $img, $departamento, $empresa) {
        $this->title = $title;
        $this->link = $link;
        $this->img = $img;
        $this->departamento = $departamento;
        $this->empresa = $empresa;
    }

    public function getTitle() {
        return $this->title;
    }

    public function getLink() {
        return $this->link;
    }

    public function getImg() {
        return $this->img;
    }

    public function getDepartamento() {
        return $this->departamento;
    }

    public function getEmpresa() {
        return $this->empresa;
    }
}
?>
