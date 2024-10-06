First of all , you must connect to your mysql database with this function :

```
from mysqlSaver.mysqlSaver import *

your_connection = Connection("your_host" , "your_port" , "your_username" , "your_password" , "your_databasename").check_connection()
```

When you make connection to your owen database , you can use "your_connection" variable to use other function like this , for example :

```
from mysqlSaver.mysqlSaver import *
import pandas as pd

your_connection = Connection(host="localhost" , port=3306 , username="root" , password="test_password" , database="students").check_connection()

df = pd.DataFrame({"name" : ['john'] , "lastname" : ["doe"] , 'age' : [19]})
Saver(df , "your_table" , your_connection).sql_saver()
```


In this function, at first, according to the create_table function, the table is created based on the type of each column in the dataframe .
You can use other functions such as partition and primarykey and etc. in the same way.
Good Luck .