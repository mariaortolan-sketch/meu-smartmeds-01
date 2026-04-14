from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Produto(CrudBase):
    table = "produto"
    fields = [
        "nome",
        "descricao",
        "categoria",
        "unidade_medida",
        "quantidade",
        "estoque_minimo",
        "preco_custo",
        "preco_venda"
    ]

    def __init__(self, nome, descricao, categoria, unidade_medida,
                 quantidade, estoque_minimo, preco_custo, preco_venda):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.unidade_medida = unidade_medida
        self.quantidade = quantidade
        self.estoque_minimo = estoque_minimo
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda

    def validate(self):
        erros = [
            Validator.required(self.nome, "nome"),
            Validator.non_negative(self.quantidade, "quantidade"),
            Validator.non_negative(self.estoque_minimo, "estoque mínimo"),
            Validator.non_negative(self.preco_custo, "preço de custo"),
            Validator.non_negative(self.preco_venda, "preço de venda")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def low_stock(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM produto WHERE quantidade <= estoque_minimo ORDER BY nome"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def update_quantity(cls, id, nova_quantidade, connection=None):
        conexao = connection or Database.connect()
        cursor = conexao.cursor()
        try:
            sql = "UPDATE produto SET quantidade = %s WHERE id = %s"
            cursor.execute(sql, (nova_quantidade, id))
            if connection is None:
                conexao.commit()
            return cursor.rowcount
        except Exception:
            if connection is None:
                conexao.rollback()
            raise
        finally:
            cursor.close()
            if connection is None:
                conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            queries = [
                "SELECT COUNT(*) FROM movimentacao WHERE produto_id = %s",
                "SELECT COUNT(*) FROM pedido_movimentacao WHERE produto_id = %s"
            ]
            total = 0
            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        produto = cls.find_by_id(id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o produto porque ele possui pedidos ou movimentações vinculadas.")
        cls.delete(id)
