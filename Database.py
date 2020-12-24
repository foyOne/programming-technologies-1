from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select
# from sqlalchemy.pool import SingletonThreadPool

def Convert2SqlType(colType):
    py2sql = {float: Float, str: String}
    return py2sql.get(colType)


class Database:

    def __init__(self, conn):
        self.Engien = create_engine(conn)
        self.MetaData = MetaData()
        self.Base = self.Engien.connect()

    
    def CreateDatabase(self):
        self.MetaData.create_all(self.Engien)
        self.Base = self.Engien.connect()

    def AddTable(self, Name, **colDict):
        Table(Name, self.MetaData)
        for colName, colType in colDict:
            self.MetaData.tables[Name].append_column(Column(colName, Convert2SqlType(colType)))

    # Методы

    def Select(self, TableName):
        QueryResult = None
        try:
            QueryResult = self.Base.execute(select([self.MetaData.tables[TableName]]))
        except:
            return None
        else:
            return QueryResult