from sqlitedict import SqliteDict


class sqlCommands():

    def save(key, value, cache_file = 'main.sqlite'):
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value
                mydict.commit()
        except Exception as ex:
            print("Error during storing data: ", ex) 

    def load(key, cache_file = 'main.sqlite'):
        try:
            with SqliteDict(cache_file) as mydict:
                value = mydict[key]
            return value
        except Exception as ex:
            print("Error during loading data: ", ex) 

    def exists(key, cache_file = 'main.sqlite'):
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key]
            return True
        except Exception:
            print('Does Not Exist')
            return False