import mysql.connector
import re


class DatabaseManager:
    def __init__(self, connection_string, tabela = None):
        # Extrai os parâmetros da string de conexão usando regex
        self.tabela = tabela
        self.params = self.parse_connection_string(connection_string)
        
        # Conectando ao banco de dados usando os parâmetros extraídos
        self.conexao = mysql.connector.connect(
            host=self.params['host'],
            user=self.params['user'],
            password=self.params['password'],
            port=self.params['port'],
            database=self.params['database']
        )
        self.cursor = self.conexao.cursor()

    def parse_connection_string(self, connection_string):
        # Regex para extrair host, user, password, port e database da string de conexão
        pattern = r'-h(?P<host>[\w\.]+) -u(?P<user>\w+) -p(?P<password>[\w]+) --port (?P<port>\d+) .+ (?P<database>\w+)'
        match = re.search(pattern, connection_string)
        if not match:
            raise ValueError("A string de conexão não está no formato correto.")
        
        return match.groupdict()

    def criar_tabela(self, tabela, colunas):
        """
        Cria uma tabela com um ID automático e colunas definidas pelo usuário.

        :param tabela: Nome da tabela.
        :param colunas: Um dicionário contendo os nomes das colunas e seus tipos, ex: {"nome_produto": "VARCHAR(255)", "valor": "DECIMAL(10, 2)"}.
        """
        self.tabela = tabela
        colunas_str = ", ".join([f"{nome} {tipo}" for nome, tipo in colunas.items()])
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.tabela} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {colunas_str}
        )
        """
        self.cursor.execute(query)
        self.conexao.commit()
        print(f"Tabela '{self.tabela}' criada com sucesso!")

    def inserir_valor(self, colunas, valores):
        """
        Insere valores na tabela criada.

        :param colunas: Uma lista com os nomes das colunas onde os dados serão inseridos.
        :param valores: Uma lista ou tupla com os valores a serem inseridos.
        """
        colunas_str = ", ".join(colunas)
        placeholders = ", ".join(["%s"] * len(valores))
        query = f"INSERT INTO {self.tabela} ({colunas_str}) VALUES ({placeholders})"
        self.cursor.execute(query, valores)
        self.conexao.commit()
        print(f"Valores inseridos na tabela '{self.tabela}' com sucesso!")

    def ler_valores(self):
        """
        Lê todos os valores da tabela criada.
        """
        query = f"SELECT * FROM {self.tabela}"
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        # for linha in resultados:
        #     print(linha)
        
        return resultados

    def editar_valor(self, coluna, novo_valor, condicao_coluna, condicao_valor):
        """
        Edita valores na tabela criada com base em uma condição.

        :param coluna: Coluna a ser editada.
        :param novo_valor: Novo valor para a coluna.
        :param condicao_coluna: Coluna usada como condição.
        :param condicao_valor: Valor da condição.
        """
        query = f"UPDATE {self.tabela} SET {coluna} = %s WHERE {condicao_coluna} = %s"
        self.cursor.execute(query, (novo_valor, condicao_valor))
        self.conexao.commit()
        print(f"Valor da coluna '{coluna}' atualizado para {novo_valor} na tabela '{self.tabela}'.")

    def deletar_valor(self, condicao_coluna, condicao_valor):
        """
        Deleta um valor da tabela criada com base em uma condição.

        :param condicao_coluna: Coluna usada como condição.
        :param condicao_valor: Valor da condição.
        """
        query = f"DELETE FROM {self.tabela} WHERE {condicao_coluna} = %s"
        self.cursor.execute(query, (condicao_valor,))
        self.conexao.commit()
        print(f"Valor deletado da tabela '{self.tabela}' onde {condicao_coluna} = {condicao_valor}.")

    def exibir_colunas(self):
        """
        Exibe as colunas da tabela criada.
        """
        query = f"SHOW COLUMNS FROM {self.tabela}"
        self.cursor.execute(query)
        colunas = self.cursor.fetchall()
        print(f"Colunas da tabela '{self.tabela}':")
        print(colunas)
        self.colunas = []
        for coluna in colunas:
            self.colunas.append(coluna[0])
            print(coluna[0])

    def carregar_colunas(self):
        """
        Exibe as colunas da tabela criada.
        """
        query = f"SHOW COLUMNS FROM {self.tabela}"
        self.cursor.execute(query)
        colunas = self.cursor.fetchall()
        # print(f"Colunas da tabela '{self.tabela}':")
        # print(colunas)
        self.colunas = []
        for coluna in colunas:
            self.colunas.append(coluna[0])
            # print(coluna[0])            

    def fechar_conexao(self,e=1):
        """
        Fecha a conexão com o banco de dados.
        """
        self.cursor.close()
        self.conexao.close()
        print("Conexão com o banco de dados fechada.")
