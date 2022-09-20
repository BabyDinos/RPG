# This is the place where players will directly interact with 
import matchingengine

class Port:

    serial_number = 1

    @classmethod
    def serial_number_increase(cls):
        cls.serial_number += 1

    #create sqlite3 database to store 
    @staticmethod
    def order(player_id, serial_number, entry:tuple, database):
        try:
            feedback = matchingengine.MatchingEngine.send_order(player_id, serial_number, entry)
            if feedback == [player_id, serial_number, entry]:
                Port.serial_number_increase(Port)
                return True
        except:
            return False

    @staticmethod
    def remove(orderid, database):
        try:
            pass
        except:
            return False


# connection = sqlite3.connect(database + '.db')
# cursor = connection.cursor()
# cursor.execute("INSERT INTO {} (Item, Price, Quantity) VALUES (?,?,?)".format(database), entry)
# if database == 'buyorder':
#     order_id = '-'.join([player_id, 'B', str(cursor.lastrowid)])
#     dictionary = sqliteCommands.sqldictCommands.load(player_id, database='playerorder')
#     dictionary['Buy'].append(order_id)
# elif database == 'sellorder':
#     order_id = '-'.join([player_id, 'S', str(cursor.lastrowid)])
#     dictionary = sqliteCommands.sqldictCommands.load(player_id, database='playerorder')
#     dictionary['Sell'].append(order_id)
# sqliteCommands.sqldictCommands.save(player_id, dictionary, database='playerorder')
# connection.commit()

# sections = orderid.split('-')
# player_id = sections[0]
# ID = sections[2]

# connection = sqlite3.connect(database + '.db')
# cursor = connection.cursor()
# cursor.execute("DELETE FROM {} WHERE ID = ?".format(database), ID)
# connection.commit()


# dictionary = sqliteCommands.sqldictCommands.load(player_id, database = 'playerorder')
# if database == 'buyorder':
#     dictionary['Buy'].remove(orderid)
# elif database == 'sellorder':
#     dictionary['Sell'].remove(orderid)
# sqliteCommands.sqldictCommands.save(player_id, dictionary, database = 'playerorder')