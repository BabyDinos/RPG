#This will format the matchingengine.db into more person-friendly interface (aka. more readable)
import nextcord
import pandas as pd
import sqlite3
from sqliteCommands import sqlite3Commands

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
        return [(name, group[group['Action'] == 'Buy'].tail(1), group[group['Action'] == 'Sell'].head(1)) for name, group in grouped_data_frame]

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

    @classmethod
    def match(cls, item):
        grouped_data_frame = cls.marketdataframe[cls.marketdataframe['Item'] == item].copy()
        
        buy_group_data_frame = grouped_data_frame.loc[grouped_data_frame['Action'] == 'Buy'].copy()
        sell_group_data_frame = grouped_data_frame.loc[grouped_data_frame['Action'] == 'Sell'].copy()
        if buy_group_data_frame.empty or sell_group_data_frame.empty:
            return [], []

        buy_group_data_frame.sort_values(by = ['Price','ID'], ascending = [False, True],inplace=True)
        buy_group_data_frame.reset_index(drop = True, inplace = True)

        sell_group_data_frame.sort_values(by = ['Price','ID'], ascending = [True, True],inplace=True)
        sell_group_data_frame.reset_index(drop = True, inplace = True)

        buy_price = buy_group_data_frame.head(1)['Price'].tolist()[0]
        sell_price = sell_group_data_frame.head(1)['Price'].tolist()[0]
        buy_quantity = buy_group_data_frame.head(1)['Quantity'].tolist()[0]
        sell_quantity = sell_group_data_frame.head(1)['Quantity'].tolist()[0]
        cancel_order_list = []

        while not sell_group_data_frame.empty and not buy_group_data_frame.empty and sell_price <= buy_price:
            minimum_quantity = min(buy_quantity, sell_quantity)
            buy_quantity -= minimum_quantity
            sell_quantity -= minimum_quantity
            buy_quantity_changed = True
            sell_quantity_changed = True

            if buy_quantity == 0:
                entry = buy_group_data_frame.head(1).iloc[0].tolist()
                cancel_order_list.append(entry)
                index = cls.marketdataframe.index[cls.marketdataframe['ID'] == entry[0]][0]
                cls.marketdataframe.drop(index = index, axis = 0, inplace = True)
                buy_group_data_frame.drop(index = buy_group_data_frame.index[0], axis = 0, inplace = True)
                buy_group_data_frame.reset_index(drop = True, inplace = True)
                buy_quantity_changed = False
                if not buy_group_data_frame.empty:
                    buy_price = buy_group_data_frame.head(1)['Price'].tolist()[0]
                    buy_quantity = buy_group_data_frame.head(1)['Quantity'].tolist()[0]
            if sell_quantity == 0:
                entry = sell_group_data_frame.head(1).iloc[0].tolist()
                cancel_order_list.append(entry)
                index = cls.marketdataframe.index[cls.marketdataframe['ID'] == entry[0]][0]
                cls.marketdataframe.drop(index = index, axis = 0, inplace = True)
                sell_group_data_frame.drop(index = sell_group_data_frame.index[0], axis = 0, inplace = True)
                sell_group_data_frame.reset_index(drop=True, inplace = True)
                sell_quantity_changed = False
                if not sell_group_data_frame.empty:
                    sell_price = sell_group_data_frame.head(1)['Price'].tolist()[0]
                    sell_quantity = sell_group_data_frame.head(1)['Quantity'].tolist()[0]

        # To edit the order when its partially filled
        edit_order_list = []
        if buy_quantity_changed == True:
            buy_group_data_frame.loc[0,'Quantity'] = buy_quantity
            edit_order_list.append(buy_group_data_frame.head(1).iloc[0].tolist())
        if sell_quantity_changed == True:
            sell_group_data_frame.loc[0, 'Quantity'] = sell_quantity
            edit_order_list.append(sell_group_data_frame.head(1).iloc[0].tolist())

        return cancel_order_list, edit_order_list
