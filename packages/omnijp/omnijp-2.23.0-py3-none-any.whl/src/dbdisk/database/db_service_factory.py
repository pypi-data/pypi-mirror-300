from src.common.database import DbOracleService
from src.common.database import DbPgService
from src.common.database import DbService
from src.common.database import DbSybaseService
from src.dbdisk.types import DbType


class DbServiceFactory:
    @staticmethod
    def create_db_service(db_type: DbType, connection_string: str) -> DbService:
        if db_type == DbType.POSTGRESQL:
            return DbPgService(connection_string)
        elif db_type == DbType.SYBASE:
            return DbSybaseService(connection_string)
        elif db_type == DbType.ORACLE:
            return DbOracleService(connection_string)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")