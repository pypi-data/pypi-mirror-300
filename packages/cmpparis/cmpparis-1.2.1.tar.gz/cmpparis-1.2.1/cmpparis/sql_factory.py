from .odbc import Odbc

class SqlFactory:
    @staticmethod
    def create_sql_connector(connector_type, server, database, username, password):
        if connector_type == "odbc":
            return Odbc(server, database, username, password)
        else:
            raise ValueError("Invalid connector type")