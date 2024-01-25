# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class GrowwPipeline:
    def __init__(self):
        self.create_connection()
        #self.create_table()
    def create_connection(self):
        self.conn=sqlite3.connect("groww.db")
        self.curr=self.conn.cursor()
    def create_table(self):
       
        self.curr.execute("""CREATE TABLE IF NOT EXISTS MutualFunds(FundName varchar(45),Returns1Y varchar(5), Returns3Y varchar(5),Returns5Y varchar(5), Date date, Category text,Type text)""")
        
        self.curr.execute("""CREATE TABLE IF NOT EXISTS Stocks(StockName varchar(45),MarketValue varchar(5), Low varchar(5),High varchar(5), Date date, Category text,Type text)""")
        
        self.curr.execute("""CREATE TABLE IF NOT EXISTS AllStocks(StockName varchar(45),MarketValue varchar(5), ClosePrice varchar(5),MarketCap varchar(5), Date date, Category text,Type text)""")
    def process_item(self,item,spider):
        if 'FundName' in item:
            self.store_mutual_funds(item)
        if 'Market Cap' in item:
            self.store_all_stocks(item)
        if '52W Low' in item:
            self.store_stocks(item)
        return item
    def store_mutual_funds(self,item):
        self.curr.execute("""Insert into MutualFunds values(?,?,?,?,?,?,?)""",
		(
		item['FundName'],
		item['1Y'],
		item['3Y'],
        item['5Y'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()
    def store_all_stocks(self,item):
        print("All")
        self.curr.execute("""Insert into AllStocks values(?,?,?,?,?,?,?)""",
		(
		item['StockName'],
		item['Market Value'],
		item['Close Price'],
        item['Market Cap'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()
    def store_stocks(self,item):
        print("Stocks")
        self.curr.execute("""Insert into Stocks values(?,?,?,?,?,?,?)""",
		(
		item['StockName'],
		item['Market Value'],
		item['52W Low'],
        item['52W High'],
        item['Date'],
        item['Category'],
        item['Type']))
        self.conn.commit()
