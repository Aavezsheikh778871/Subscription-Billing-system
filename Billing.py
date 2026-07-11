import datetime
import json
import os
import sqlite3
# Main Class User with all methods needed
class User:
    
    def __init__(self, name, email, balance):
        self.name = name
        self.email = email        
        self.__balance = balance
#Shows the current time and date
    def subscription_start_date(self):
        date = datetime.datetime.now() 
        print(date)
#Saving amount to deposit 
    def deposit(self, amount):
        if amount > 0 :
            self.__balance += amount
            print("Transaction is Successfully Done!!")
            self.save_to_ledger(amount, "deposit")

        else:
            print("No Transaction is done yet")
#Saving amount to charge fee
    def charge_fee(self, amount):
        
        if  0 < amount <= self.__balance:
            self.__balance -= amount
            print("Withdrawed Successfully!!")
            self.save_to_ledger(amount, "charge")

        else:
            print("Insufficient balance!")
#Save the transaction details to ledger.json file
    def save_to_ledger(self, amount, transaction_type):
        
        conn = sqlite3.connect("billing.db")
        cursor = conn.cursor()
        
        cursor.execute ("""     
                        INSERT INTO transactions (name, amount, type, date)
                        VALUES (?, ?, ?, ?)
                        """, (self.name, amount, transaction_type, str(datetime.datetime.now())))
        
        conn.commit()
        conn.close()

#Free_user type in User    
class Free_user(User):
    
    def __init__(self, name, email):
        super().__init__(name, email, 0)
        
    def calculate_bill(self):
        return 1500
#Premium_user type in User
class Premium_user(User):
    
    def __init__(self, name, email):
        super().__init__(name, email, 0)
    
    def calculate_bill(self):
        return 2000
#Corporate_user type in User
class Corporate_user(User):
    
    def __init__(self, name, email, employees):
        super().__init__(name, email, 0)
        self.employees = employees
        
    def calculate_bill(self):
        
        if self.employees >= 10:
            return 1300 * self.employees
        else:
            print("Minimum 10 employees required for Corporate plan!")
            return 0 
#Show the name and amount of deposits of All User from the transaction and if the file not exist it throughs the error
def show_deposits():
  
    conn = sqlite3.connect("billing.db") 
    cursor = conn.cursor()
    
    cursor.execute ("SELECT name, amount FROM transactions WHERE type = 'deposit'")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row[0], row[1])
        
    conn.close()

if __name__ == "__main__":
    
    free1 = Free_user("Aavuu", "aavuu@email.com")
    corporate1 = Corporate_user("TechCorp", "contact@techcorp.com", 15)
    premium1 = Premium_user("Sufiyan", "sufiyan123@gmail.com")
    
    free1.deposit(2000)
    bill1 = free1.calculate_bill()
    free1.charge_fee(bill1)
    
    corporate1.deposit(25000)
    bill2 = corporate1.calculate_bill()
    corporate1.charge_fee(bill2)
    
    premium1.deposit(3000)
    bill3 = premium1.calculate_bill()
    premium1.charge_fee(bill3)
    
    show_deposits()