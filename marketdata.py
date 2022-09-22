#This will format the matchingengine.db into more person-friendly interface (aka. more readable)
import nextcord
import pandas as pd
import sqlite3

class MarketData:

    marketdataframe = pd.DataFrame()

    @classmethod
    def startup(cls):
        conn = sqlite3.connect('matchingengine.db')
        sql_query = pd.read_sql_query('SELECT * FROM matchingengine', conn)
        cls.marketdataframe = pd.DataFrame(sql_query, dtype=str)

    @staticmethod
    def display():
        grouped_data_frame = MarketData.marketdataframe.sort_values(['ID','Price','Quantity'], ascending = [True, False, False]).groupby(['Item','Action'])
        for name, group in grouped_data_frame:
            print(name)
            print(group)

    @classmethod
    def add(cls, player_id, entry):
        entry = list(entry)
        new_id = str(int(cls.marketdataframe.loc[len(cls.marketdataframe)-1,'ID'])+1)
        entry = [new_id, player_id] + entry
        cls.marketdataframe.loc[len(cls.marketdataframe)] = entry

    @classmethod
    def remove(cls, orderid):
        split_orderid = orderid.split('-')
        remove_index = cls.marketdataframe.index[(cls.marketdataframe['ID'] == split_orderid[0]) & (cls.marketdataframe['PlayerID'] == split_orderid[1])].tolist()[0]
        cls.marketdataframe = cls.marketdataframe.drop(labels = remove_index, axis = 0).reset_index(drop= True)


