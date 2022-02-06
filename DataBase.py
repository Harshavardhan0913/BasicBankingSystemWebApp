import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customers(customerId NUMBER,customerName TEXT, balance REAL)");
        self.conn.commit()
    def get_data(self):
        self.cursor.execute(f"Select * from customers");
        data = self.cursor.fetchall()
        return data
    def get_customer(self, customerid):
        self.cursor.execute(f"Select * from customers where customerId = '{customerid}'");
        data = self.cursor.fetchall()
        return data
    def set_balance(self, customerid, balance):
        self.cursor.execute(f"Select * from customers where customerId = '{customerid}'")
        data = self.cursor.fetchall()
        if data:
            self.cursor.execute(f"Update customers set balance='{balance}' where customerName = '{customerid}'")
            self.conn.commit()
            return "Success"
        else:
            return "Fail"

    def get_other_customers(self,customerId):
        self.cursor.execute(f"Select * from customers where customerId != '{customerId}'");
        data = self.cursor.fetchall()
        #print(data.rowcount)
        if data:
            return data
        else:
            return None

    def transfer(self,fromCustomerId,toCustomerId,amount):
        try:
            self.cursor.execute(f"Select balance from customers where customerId = '{fromCustomerId}'")
            data = self.cursor.fetchall()
            #print(data[0]['balance'])
            #print(amount)
            if float(data[0]['balance']) >= float(amount):
                #print("10000000")
                self.cursor.execute(f"Update customers set balance={float(data[0]['balance'])-amount} where customerId = '{fromCustomerId}' ")
            else:
                return 1
            self.cursor.execute(f"Select balance from customers where customerId = '{toCustomerId}'")
            data1 = self.cursor.fetchall()
            self.cursor.execute(f"Update customers set balance={float(data1[0]['balance']) + amount} where customerId = '{toCustomerId}' ")
            self.conn.commit()
            return 0
        except:
            return -1
