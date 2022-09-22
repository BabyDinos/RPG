# Will have all the logic, display the trades, and communicate with the ports
# It will multitask out orders from the ports, back to the ports where every player can see what is currently being ordered. 
# Player -> Port Class will communicate with the matching engine 
# Save orders in market data dataframe
import sqlite3
import sqliteCommands


class MatchingEngine:

    port_serial_number = 1


    @classmethod
    def serial_number_increase(cls):
        cls.port_serial_number += 1  

    @staticmethod
    def send_order(player_id, serial_number, entry:tuple):
        if serial_number == MatchingEngine.port_serial_number:
            try:
                sqliteCommands.sqlite3Commands.add(player_id, entry)
                MatchingEngine.serial_number_increase()
                return serial_number
            except:
                print('Error in Saving order')

    @staticmethod
    def cancel_order(player_id, serial_number, orderid):
        if serial_number == MatchingEngine.port_serial_number:
            try:
                sqliteCommands.sqlite3Commands.remove(player_id, orderid)
                MatchingEngine.serial_number_increase()
                return serial_number
            except:
                print('Error in Cancelling Order')

