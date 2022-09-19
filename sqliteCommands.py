from sqlitedict import SqliteDict
import sqlite3

class sqldictCommands:

    @staticmethod
    def save(key, value, database):
        if database == 'player':
            cache_file = 'player.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value
                mydict.commit()
        except Exception as ex:
            print("Error during storing data: ", ex) 

    @staticmethod
    def load(key, database):
        if database == 'player':
            cache_file = 'player.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                value = mydict[key]
            mydict.close()
            return value
        except Exception as ex:
            mydict.close()
            print("Error during loading data: ", ex) 
            return False
            
    @staticmethod
    def delete(key, database):
        if database == 'player':
            cache_file = 'player.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                mydict.pop(key)
                mydict.commit()
        except Exception as ex:
            print("Error during deletion: ", ex)

class sqliteCommands:
    #create sqlite3 database to store 
    @staticmethod
    def add(entry, database):
        connection = sqlite3.connect(database + '.db')
        cursor = connection.cursor()
        print("INSERT INTO {} VALUES ({},{},{},{})".format(database, *entry))
        cursor.execute("INSERT INTO {} VALUES ({},{},{},{})".format(database, *entry))
        pass

sqliteCommands.add(['Gold','6404',100,100], 'buyorder')