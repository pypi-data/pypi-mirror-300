# mini_db.py

class Database:
    def __init__(self):
        self.tables = {}
        self.current_table = None

    def create_table(self, name):
        self.tables[name] = []
        # print(f"Tabela '{name}' criada.")  # Comente ou remova essa linha

    def navigate(self, table_name):
        self.current_table = table_name
        # print(f"Navegando para a tabela '{table_name}'.")  # Comente ou remova essa linha

    def insert(self, record):
        self.tables[self.current_table].append(record)
        # print(f"Registro inserido na tabela '{self.current_table}': {record}")  # Comente ou remova essa linha

    def select(self):
        return self.tables[self.current_table]