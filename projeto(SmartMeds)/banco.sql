CREATE DATABASE IF NOT EXISTS produto_db;
USE produto_db;

CREATE TABLE IF NOT EXISTS produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    categoria VARCHAR(50),
    unidade_medida VARCHAR(20),
    quantidade INT NOT NULL DEFAULT 0,
    estoque_minimo INT NOT NULL DEFAULT 0,
    preco_custo DECIMAL(10,2) NOT NULL DEFAULT 0,
    preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pedido_movimentacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    quantidade INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE',
    observacao VARCHAR(255),
    data_pedido DATETIME NOT NULL,
    data_processamento DATETIME NULL,
    CONSTRAINT fk_pedido_produto FOREIGN KEY (produto_id) REFERENCES produto(id)
);

CREATE TABLE IF NOT EXISTS movimentacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    tipo_movimentacao VARCHAR(10) NOT NULL,
    quantidade INT NOT NULL,
    data_movimentacao DATETIME NOT NULL,
    CONSTRAINT fk_movimentacao_produto FOREIGN KEY (produto_id) REFERENCES produto(id)
);
