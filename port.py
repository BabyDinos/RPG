# This is the place where players will directly interact with 
import matchingengine

class Port:

    serial_number = 1

    @classmethod
    def serial_number_increase(cls):
        cls.serial_number += 1

    #create sqlite3 database to store 
    @staticmethod
    def order(player_id, serial_number, entry:tuple):
        try:
            feedback = matchingengine.MatchingEngine.send_order(player_id, serial_number, entry)
            if feedback == serial_number:
                Port.serial_number_increase()
                return feedback
        except:
            return False

    @staticmethod
    def cancelorder(player_id, serial_number, orderid):
        try:
            feedback = matchingengine.MatchingEngine.cancel_order(player_id, serial_number, orderid)
            if feedback == serial_number:
                Port.serial_number_increase()
                return feedback
        except:
            return False

