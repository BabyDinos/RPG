from sqlitedict import SqliteDict


class sqlCommands:

    def save(key, value, unit):
        if unit == 'player':
            cache_file = 'player.sqlite'
        else:
            cache_file = 'enemy.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                mydict[key] = value
                mydict.commit()
        except Exception as ex:
            print("Error during storing data: ", ex) 

    def load(key, unit):
        if unit == 'player':
            cache_file = 'player.sqlite'
        else:
            cache_file = 'enemy.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                value = mydict[key]
            mydict.close()
            return value
        except Exception as ex:
            mydict.close()
            print("Error during loading data: ", ex) 
            return False

    def delete(key, unit):
        if unit == 'player':
            cache_file = 'player.sqlite'
        else:
            cache_file = 'enemy.sqlite'
        try:
            with SqliteDict(cache_file) as mydict:
                mydict.pop(key)
                mydict.commit()
        except Exception as ex:
            print("Error during deletion: ", ex)