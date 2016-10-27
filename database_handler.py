__author__ = 'ASUS-PC'
class databaseHandler(object):

    def sql_handler(self,database,query):
        import mysql.connector as cnn
        config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'database': database,
            'raise_on_warnings': True,
        }
        cnx =cnn.Connect(**config)
        cursor = cnx.cursor()
        cursor.execute(query)
        results=list(cursor.fetchall())
        cursor.close()
        cnx.close()
        return results
test=databaseHandler()
print(test.sql_handler("cdcol","select * from cds"))