from sqlitedict import SqliteDict

class sqldictCommands:

    @staticmethod
    def save(key, value, database):
        cache_file = ''.join([database, '.sqlite'])
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value
                mydict.commit()
        except Exception as ex:
            print("Error during storing data: ", ex) 

    @staticmethod
    def load(key, database):
        cache_file = ''.join([database, '.sqlite'])
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
        cache_file = ''.join([database, '.sqlite'])
        try:
            with SqliteDict(cache_file) as mydict:
                mydict.pop(key)
                mydict.commit()
        except Exception as ex:
            print("Error during deletion: ", ex)


