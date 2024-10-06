from tqdm import tqdm
import pymysql
import pandas as pd



class Connection:
    def __init__(self , host , port , username , password , database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def Connect(self):
        try:
            return pymysql.connect(host=self.host, port=int(self.port), user=self.username , password=self.password , database=self.database)
        except:
            print('This connection does not exist')



class CheckerAndReceiver:
    def __init__(self , connection  , database_name=0 , table_name=0):
        self.connection = connection
        self.database_name = database_name
        self.table_name = table_name


    def read_table(self):
        sql_query = f"SELECT * FROM {self.table_name}"
        df = pd.read_sql_query(sql_query, self.connection)
        return df
    


    def table_exist(self):
        
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{self.table_name}'")
        exist = cursor.fetchone()
        if exist == None:
            return False
        else:
            return True
        

    def database_exist(self):
        
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
        exist = cursor.fetchone()
        if exist == None:
            return False
        else:
            return True





class Creator:
    def __init__(self , df , table_name , connection):
        self.df =df
        self.table_name =table_name
        self.connection =connection


    def create_table(self):
        cursor = self.connection.cursor()
        
        column_data_types = {"int32": 'INT', 'int64': 'INT', 'float64': 'FLOAT', 'datetime64': 'DATETIME', 'bool': 'BOOL', 'object': 'LONGTEXT'}
        columns = []

        for column, data_type in self.df.dtypes.items():
            if data_type == 'object':
                max_length = self.df[column].str.len().max()
                if max_length >= 70:
                    columns.append(f"`{column}` LONGTEXT")
                else:
                    columns.append(f"`{column}` VARCHAR(70)")
            else:
                columns.append(f"`{column}` {column_data_types[str(data_type)]}")

        columns_str = ', '.join(columns)
        
        query = f"CREATE TABLE {self.table_name} ({columns_str})"
        cursor.execute(query)
        self.connection.commit()


    def database_creator(self):
        
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
        exist = cursor.fetchone()
        if not exist:
            cursor.execute(f"CREATE DATABASE {self.database_name}")
        else:
            print('Database is exist')





class Saver:
    def __init__(self , df , table_name , connection , primary_key_list=0):
        self.df = df
        self.table_name = table_name
        self.connection = connection
        self.primary_key_list = primary_key_list



    def sql_saver(self):

        if not CheckerAndReceiver(self.table_name , self.connection).table_exist():
            Creator(self.df , self.table_name , self.connection).create_table()

        cursor = self.connection.cursor()
        columns = ', '.join([f'`{column}`' for column in self.df.columns])
        values_str = ','.join(['%s'] * len(self.df.columns))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values_str})"
        for row in tqdm(self.df.values):
            data = tuple(row)
            cursor.execute(query, data)
        self.connection.commit()



    def sql_saver_with_primarykey(self):

        if not CheckerAndReceiver(self.table_name , self.connection).table_exist():
            Creator(self.df , self.table_name , self.connection).create_table()

        cursor = self.connection.cursor()
        columns = ', '.join([f'`{column}`' for column in self.df.columns])
        values_str = ','.join(['%s'] * len(self.df.columns))
        query = f"INSERT IGNORE INTO {self.table_name} ({columns}) VALUES ({values_str});"
        self.connection.commit()
        query3 = f"ALTER TABLE {self.table_name} DROP PRIMARY KEY;"
        query_check_key = f"SHOW KEYS FROM {self.table_name} WHERE Key_name = 'PRIMARY';"
        cursor.execute(query_check_key)
        if cursor.fetchone() is not None:
            cursor.execute(query3)
            self.connection.commit()
        else:
            pass
        query2 = f"ALTER TABLE {self.table_name} ADD PRIMARY KEY ({' , '.join(self.primary_key_list)})"
        cursor.execute(query2)
        self.connection.commit()
        
        for row in tqdm(self.df.values):
            data = tuple(row)
            cursor.execute(query, data)
        self.connection.commit()



    def sql_saver_with_primarykey_and_update(self):

        
        if not CheckerAndReceiver(self.table_name , self.connection).table_exist():
            Creator(self.df , self.table_name , self.connection).create_table()

        cursor = self.connection.cursor()
        columns = ', '.join([f'`{column}`' for column in self.df.columns])
        values_str = ','.join(['%s'] * len(self.df.columns))
        query = f"INSERT IGNORE INTO {self.table_name} ({columns}) VALUES ({values_str});"
        self.connection.commit()
        update_str = ', '.join([f'`{column}` = VALUES(`{column}`)' for column in self.df.columns])
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values_str}) ON DUPLICATE KEY UPDATE {update_str};"
        self.connection.commit()
        query3 = f"ALTER TABLE {self.table_name} DROP PRIMARY KEY;"
        query_check_key = f"SHOW KEYS FROM {self.table_name} WHERE Key_name = 'PRIMARY';"
        cursor.execute(query_check_key)
        if cursor.fetchone() is not None:
            cursor.execute(query3)
            self.connection.commit()
        else:
            pass
        query2 = f"ALTER TABLE {self.table_name} ADD PRIMARY KEY ({' , '.join(self.primary_key_list)})"
        cursor.execute(query2)
        self.connection.commit()
        
        for row in tqdm(self.df.values):
            data = tuple(row)
            cursor.execute(query, data)
        self.connection.commit()



    def sql_saver_with_unique_key(self):
        if not CheckerAndReceiver(self.table_name , self.connection).table_exist():
            Creator(self.df , self.table_name , self.connection).create_table()

        cursor = self.connection.cursor()
        columns = ', '.join([f'`{column}`' for column in self.df.columns])
        values_str = ', '.join(['%s'] * len(self.df.columns))

        query = f"INSERT IGNORE INTO {self.table_name} ({columns}) VALUES ({values_str});"

        for row in tqdm(self.df.values):
            data = tuple(row)
            cursor.execute(query, data)
        self.connection.commit()



    def sql_updater_with_primarykey(self):
        cursor = self.connection.cursor()

        for row in tqdm(self.df.values):
            primary_key_values = tuple(row[self.df.columns.get_loc(pk)] for pk in self.primary_key_list)
            set_statements = ', '.join([f'`{column}` = %s' for column in self.df.columns if column not in self.primary_key_list])
            query = f"UPDATE {self.table_name} SET {set_statements} WHERE {' AND '.join([f'`{pk}` = %s' for pk in self.primary_key_list])};"
            data = tuple(row[self.df.columns.get_loc(column)] for column in self.df.columns if column not in self.primary_key_list) + primary_key_values
            cursor.execute(query, data)

        self.connection.commit()






class Partition:
    def __init__(self , df , table_name , connection , range_key , primary_key_list , start_year_partition , end_year_partition):
        self.df = df
        self.table_name = table_name
        self.connection = connection
        self.range_key = range_key
        self.primary_key_list = primary_key_list
        self.start_year_partition = start_year_partition
        self.end_year_partition = end_year_partition



    def create_partition_table(self):


        if not CheckerAndReceiver(self.table_name , self.connection).table_exist():
            start_year = self.start_year_partition
            start_month = 1
            end_year = self.end_year_partition
            end_month = 12
            year = start_year
            month = start_month
            partition_query = ''
            first_iteration = True

            while year <= end_year:
                while (year < end_year and month <= 12) or (year == end_year and month <= end_month):
                    partition_name = f"p{year}m{month:02}"
                    partition_value = int(f"{year}{month:02}32")
                    partition_clause = f"PARTITION `{partition_name}` VALUES LESS THAN ({partition_value}) ENGINE = InnoDB"
                    
                    if first_iteration:
                        partition_query += partition_clause
                        first_iteration = False
                    else:
                        partition_query += f", {partition_clause}"
                    
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                        
                break

            cursor = self.connection.cursor()
            column_data_types = {"int32":'INT' , 'int64': 'INT', 'float64': 'FLOAT', 'datetime64': 'DATETIME', 'bool': 'BOOL', 'object': 'VARCHAR(70)'}
            columns = ', '.join([f'`{column}` {column_data_types[str(data_type)]}' for column, data_type in self.df.dtypes.items()])
            query_set_partition = f'''CREATE TABLE {self.table_name} ({columns}, KEY `{self.table_name}_index` ({' , '.join(self.primary_key_list)})) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci PARTITION BY RANGE (`{self.range_key}`) ({partition_query})'''
            cursor.execute(query_set_partition)
            self.connection.commit()
        else:
            pass