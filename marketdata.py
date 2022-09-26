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
        cls.marketdataframe = pd.DataFrame(sql_query, dtype = 'object')
        cls.marketdataframe = cls.marketdataframe.astype({'ID':int,'PlayerID':pd.StringDtype(),'Item':pd.StringDtype(),'Action':pd.StringDtype(),'Price':int,'Quantity':int})
    @classmethod
    def display(cls):
        cls.marketdataframe.sort_values(by=['Price', 'ID','Quantity'], inplace=True)
        cls.marketdataframe.reset_index(drop = True, inplace = True)
        grouped_data_frame = cls.marketdataframe.groupby(['Item'])
        return [(name, group[group['Action'] == 'Buy'].head(1), group[group['Action'] == 'Sell'].tail(1)) for name, group in grouped_data_frame]

    @classmethod
    def add(cls, lastid, player_id, entry):
        entry = list(entry)
        new_id = lastid
        entry = [new_id, player_id] + entry
        cls.marketdataframe.loc[len(cls.marketdataframe)] = entry
        cls.marketdataframe = cls.marketdataframe.astype({'ID':int,'PlayerID':pd.StringDtype(),'Item':pd.StringDtype(),'Action':pd.StringDtype(),'Price':int,'Quantity':int})

    @classmethod
    def remove(cls, orderid):
        split_orderid = orderid.split('-')
        remove_index = cls.marketdataframe.index[(cls.marketdataframe['ID'] == int(split_orderid[0])) & (cls.marketdataframe['PlayerID'] == split_orderid[1])].tolist()[0]
        print(remove_index)
        cls.marketdataframe = cls.marketdataframe.drop(labels = remove_index, axis = 0).reset_index(drop= True)
