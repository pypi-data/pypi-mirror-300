from enum import Enum
import hashlib as sh

class EncryptValue:
    def __init__(
        self,
        value
    ):
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        self.value_hashed = hash.hexdigest()


class Types(Enum):
    integer = 'INTEGER'
    text = 'TEXT'
    real = 'REAL'
    null = 'NULL'
    blob = 'BLOB'

class Column:
    def __init__(
        self,
        name: str,
        column_type: Types,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        not_null: bool = False
    ):
        self.name = name
        self.type = column_type

        if not isinstance(column_type, Types):
            raise ValueError(f'O tipo da coluna deve ser um valor de `column_types`, e não {type(column_type)}.')
        
        self.column_parameters = f'{name} {column_type.value}'
        
        if primary_key == True:
            self.column_parameters += f' PRIMARY KEY'
        
        if auto_increment == True:
            self.column_parameters += f' AUTOINCREMENT'
        
        if unique == True:
            self.column_parameters += f' UNIQUE'
        
        if not_null == True:
            self.column_parameters += f' NOT NULL'
    
    def to_dict(self):
        """Converte a coluna para um dicionário."""
        return {
            'name': self.name,
            'type': self.type.value,
            'parameters': self.column_parameters
        }

class Table:
    def __init__(
        self,
        name: str
    ):
        self.columns: list[Column] = []
        self.name = name
    
    def to_dict(self):
        """Converte a tabela e suas colunas para um dicionário."""
        return {
            'table_name': self.name,
            'columns': [column.to_dict() for column in self.columns]
        }

class Filter:
    def __init__(
        self,
        column: str
    ):
        self.column_name = column
        self.__condition: str = f"WHERE {column} "
        self.__params: list = []
    
    def filterby(self, column):
        self.__condition += f'{column} '
        return self

    @property
    def OR(self):
        self.__condition += "OR "
        return self
    
    @property
    def AND(self):
        self.__condition += "AND "
        return self
    
    def EQUAL(self, value):
        self.__add_filter(condition='=', value=value)
        return self
    
    def GATHER_THAN(self, value):
        self.__add_filter(condition='>', value=value)
        return self
    
    def GATHER_OR_EQUAL(self, value):
        self.__add_filter(condition='>=', value=value)
        return self
    
    def LESS_THAN(self, value):
        self.__add_filter(condition='<', value=value)
        return self
    
    def LESS_OR_EQUAL(self, value):
        self.__add_filter(condition='<=', value=value)
        return self
    
    def CONTAIN(self, value):
        self.__add_filter(condition='LIKE', value=f'%{value}%')
        return self
    
    def __add_filter(self, condition: str, value):
        self.__params.append(value)
        self.__condition += f'{condition} ? '

class ColumnData:
    def __init__(
        self,
        column: str,
        value: str | int | float | bool | None
    ):
        self.column = column
        self.value = value