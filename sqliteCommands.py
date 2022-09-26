from sqlitedict import SqliteDict
import sqlite3

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

class sqlite3Commands:

    @staticmethod
    def add(player_id, entry:tuple, database = 'matchingengine'):

        connection = sqlite3.connect(database + '.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO {} (PlayerID, Item, Action, Price, Quantity) VALUES ({},?,?,?,?)".format(database, player_id), entry)
        lastid = int(cursor.lastrowid)
        connection.commit()
        str_tuple = '-'.join([str(x) for x in entry])
        order_id = '-'.join([str(lastid), player_id, str_tuple])
        order_list = sqldictCommands.load(player_id, database='playerorder')
        order_list.append(order_id)
        sqldictCommands.save(player_id, order_list, database='playerorder')
        return lastid

    @staticmethod
    def remove(player_id, orderid:str, database = 'matchingengine'):
        connection = sqlite3.connect(database + '.db')
        cursor = connection.cursor()
        split_orderid = orderid.split('-')
        entry = [x for x in split_orderid]
        cursor.execute("DELETE FROM {} WHERE ID = ? and PlayerID = ? and Item = ? and Action = ? and Price = ? and Quantity = ?".format(database), entry)
        connection.commit()
        order_list = sqldictCommands.load(player_id, database='playerorder')
        order_list.remove(orderid)
        sqldictCommands.save(player_id, order_list, database='playerorder')

