'''  DO:  more $HOME/.my.cnf to see your MySQL username and  password
#  CHANGE:  MYUSERNAME and MYMYSQLPASSWORD in the test section of
#  this program to your username and mysql password
#  RUN: Python3 python_db_connector.py '''

import mysql.connector
from tabulate import tabulate


def open_database(hostname, user_name, mysql_pw, database_name):
    global conn
    conn = mysql.connector.connect(host=hostname,
                                   user=user_name,
                                   password=mysql_pw,
                                   database=database_name
                                   )
    global cursor
    cursor = conn.cursor()


def printFormat(result):
    header = []
    for cd in cursor.description:  # get headers
        header.append(cd[0])
    print('')
    print('Query Result:')
    print('')
    print(tabulate(result, headers=header))  # print results in table format


# select and display query
def executeSelect(query):
    cursor.execute(query)
    printFormat(cursor.fetchall())

def executeOnly(query):
    cursor.execute(query)
    cursor.fetchall()

def insert(table, values):
    query = "INSERT into " + table + " values (" + values + ")" + ';'
    cursor.execute(query)
    conn.commit()

def menu():
    print("Press [1] for Supplier By Country")
    print("Press [2] for Add Supplier")
    print("Press [3] for Employee Performance")
    print("Press [4] for Update Item")
    print("Press [5] for Cancel Sales")
    print("Press [6] for Quit")

def supplierCountry():
    # Get user input for country
    countryName = input("Enter the name of country to check: ")


    # Display the supplier for the given country
    print(f"Current availability for {countryName} shown below.")
    executeSelect(f"SELECT S.SUPPLIER_ID AS 'Supplier ID', S.NAME AS 'Supplier Name', S.PHONE_NUMBER as 'Phone Number', I.NAME AS 'Coffee Name', I.ROASTING_TYPE FROM Inventory_MGMT IM Left JOIN Item I ON I.ID = IM.ITEM_ID LEFT JOIN Supplier S ON S.SUPPLIER_ID = IM.SUPPLIER_ID WHERE S.COUNTRY =  '{countryName}';")



def addSupplier():
    # List of coffee names to use later on
    coffeeNames = ["ANTIGUA", "HAMBELA KIRITE", "KHAWLANI", "MOGIANA", "ALWADI", "VOLCANICA SUPREMO", "PNG",
                   "SUMATRA GAYO", "ARABICA", "GENERAL MERCHANDISE", "SIDAMO", "GHIMBI", "ALDURRAR"]
    # Get the new suppler name, phone number, and country
    newSupplier = input("Enter the name of the new supplier: ")
    newSuppNum = input("Enter the phone number of the new supplier: ")
    newSuppCountry = input("Enter the country where the new supplier is located: ")

    # itemFlag to control while loop for item ID input; makes sure that the ID is valid.
    itemFlag = False
    while itemFlag == False:
        coffeeItem = input("Please enter the name of the coffee this supplier sells: ")
        coffeeItem = coffeeItem.upper()
        try:
            if coffeeItem in coffeeNames:
                itemFlag = True
            else:
                print("Invalid coffee. Please select a valid coffee.")
        except ValueError:
            print("Invalid input. Please try again.")

    # availFlag to make sure the user inputs an availability > 0
    availFlag = False
    while availFlag == False:
        totalAvailable = input("Enter the supplier's current availability of their coffee: ")
        try:
            totalAvailable = int(totalAvailable)
            if (totalAvailable >= 0):
                availFlag = True
        except ValueError:
            print("Invalid amount. Please input an integer value.")

    # Insert new supplier into the Supplier table
    insert("Supplier",
           f"(SELECT (MAX(SUPPLIER_ID) + 1) FROM Supplier supp), '{newSupplier}', '{newSuppNum}', '{newSuppCountry}'")

    # Insert new supplier into Inventory_MGMT table
    insert("Inventory_MGMT",
           f"(SELECT ID FROM Item WHERE NAME = '{coffeeItem}'), (SELECT MAX(SUPPLIER_ID) FROM Supplier), 0, {totalAvailable}")

    # Show the record for the new supplier
    executeSelect(f"SELECT * FROM Supplier WHERE NAME = '{newSupplier}'")

    # Print out all suppliers who supply the same coffee
    print("\nHere are all of the suppliers of the selected coffee.")
    executeSelect(
        f"SELECT s.NAME AS 'Supplier', i.NAME AS 'Coffee' FROM Supplier s LEFT JOIN Inventory_MGMT im ON s.SUPPLIER_ID = im.SUPPLIER_ID LEFT JOIN Item i ON i.ID = im.ITEM_ID WHERE i.NAME = '{coffeeItem}';")


def employeePerformance():
    # Get user input for employee
    employeeName = input("Enter the name employee or performance check: ").upper()



    # Display the employee sales
    print(f"Total sales for {employeeName} shown below.")
    executeOnly(f"SELECT I.NAME as 'Name', I.ROASTING_TYPE as 'Roasting Type', COUNT(I.NAME) as 'Sales Count' FROM Sales M LEFT JOIN Item I ON I.ID = M.ITEM_ID LEFT JOIN Employee E ON E.ID = M.EMPLOYEE_ID WHERE E.NAME = '{employeeName}' GROUP BY I.NAME, I.ROASTING_TYPE;")


    #Check if employee has no sales
    if cursor.rowcount == 0:
        print(f"{employeeName} has sold no items")
    else:
        executeSelect(f"SELECT I.NAME as 'Name', I.ROASTING_TYPE as 'Roasting Type', COUNT(I.NAME) as 'Sales Count' FROM Sales M LEFT JOIN Item I ON I.ID = M.ITEM_ID LEFT JOIN Employee E ON E.ID = M.EMPLOYEE_ID WHERE E.NAME = '{employeeName}' GROUP BY I.NAME, I.ROASTING_TYPE;")


def updateItem():
    #Get the item name to update
    itemName = input("Enter the name of the item to update: ")
    supplierID = int(input("Enter the supplier ID of the item: "))

    #Flag for while loop; while the flag is false (or not an integer), loop for a valid input
    numFlag = False
    while numFlag == False:
        newAvailNum = input("Enter the item's new Total Availability: ")
        try:
            newAvailNum = int(newAvailNum)
            numFlag = True
        except ValueError:
            print("Invalid amount. Please input an integer value.")

    #Get the current availability for the item
    print(f"Current availability for {itemName} shown below.")
    executeSelect(f"SELECT i.Name, im.Total_Available FROM Item i LEFT JOIN Inventory_MGMT im ON i.ID = im.Item_ID WHERE i.Name = '{itemName}' AND im.Supplier_ID = '{supplierID}';")

    #Update the item
    print(f"\nUpdating {itemName}")
    executeUpdate(f"UPDATE Inventory_MGMT im, Item i SET Total_Available = {newAvailNum} WHERE i.ID = im.Item_ID AND i.Name = '{itemName}' AND im.Supplier_ID = '{supplierID}';")

    #Display the updated values
    print(f"{itemName}'s total availability updated. {itemName}'s new availability shown below.")
    executeSelect(f"SELECT i.Name, im.Total_Available FROM Item i LEFT JOIN Inventory_MGMT im ON i.ID = im.Item_ID WHERE i.Name = '{itemName}' AND im.Supplier_ID = '{supplierID}';")


def cancelSales():
    pass

def executeUpdate(query):  # use this function for delete and update
    cursor.execute(query)
    conn.commit()


def close_db():  # use this function to close db
    cursor.close()
    conn.close()


##### Test #######
mysql_username = 'dmiao'  # please change to your username
mysql_password = 'bieYuj0b'  # please change to your MySQL password
mysql_host = 'turing.uark.edu'

open_database(mysql_host, mysql_username, mysql_password, mysql_username)  # open database


#Menu creation
menu()
select = int(input("Enter Option: "))
while select != 6:
    if select == 1:
        supplierCountry()
    elif select == 2:
        addSupplier()
    elif select == 3:
        employeePerformance()
    elif select == 4:
        updateItem()
    elif select == 5:
        cancelSales()
    else:
        print("Invalid Option")

    #Reprint if invalid
    print()
    menu()
    select = int(input("Enter Option: "))

#print(' ')
#print('Testing select: ')
#print('=======================================')
#executeSelect('SELECT * FROM Item');

#print(' ')
#print('Testing insert item 22: ')
#print('=======================================')
#insert('Item', "22,'test',23.5,'M'")
#executeSelect('SELECT * FROM Item where id = 22;')

#print(' ')
#print('Testing delete item 22: ')
#print('=======================================')
#executeUpdate('delete from Item where id = 22;')
#executeSelect('SELECT * FROM Item where id = 22;')

#print(' ')
#print('Testing update of address to Jordan for supplier 3: ');
#print('=======================================')
#executeSelect("SELECT * FROM Supplier where SUPPLIER_ID = 3;")
#executeUpdate("Update Supplier set COUNTRY = 'JORDAN' where SUPPLIER_ID = 3;")
#executeSelect("SELECT * FROM Supplier where SUPPLIER_ID = 3;")

close_db()  # close database




