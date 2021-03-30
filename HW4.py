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

# Function to execute query, but NOT display. Use for logic checking
def executeOnly(query):
    cursor.execute(query)
    cursor.fetchall()

def insert(table, values):
    query = "INSERT into " + table + " values (" + values + ")" + ';'
    cursor.execute(query)
    conn.commit()

# Function creates the display for the menu
def menu():
    print("Press [1] for Supplier By Country")
    print("Press [2] for Add Supplier")
    print("Press [3] for Employee Performance")
    print("Press [4] for Update Item")
    print("Press [5] for Cancel Sales")
    print("Press [6] for Quit")

def supplierCountry():
    # Get user input for country
    countryName = input("Enter the name of country to check: ").upper()

    print(f"Current availability for {countryName} shown below.")
    executeSelect(f"SELECT S.SUPPLIER_ID AS 'Supplier ID', S.NAME AS 'Supplier Name', S.PHONE_NUMBER as 'Phone Number', I.NAME AS 'Coffee Name', I.ROASTING_TYPE FROM Inventory_MGMT IM Left JOIN Item I ON I.ID = IM.ITEM_ID LEFT JOIN Supplier S ON S.SUPPLIER_ID = IM.SUPPLIER_ID WHERE S.COUNTRY =  '{countryName}';")
    print("\n")


def addSupplier():
    # Get the new suppler name, phone number, and country
    newSupplier = input("Enter the name of the new supplier: ")
    newSuppNum = input("Enter the phone number of the new supplier: ")
    newSuppCountry = input("Enter the country where the new supplier is located: ")

    # itemFlag to control while loop for item nameinput; makes sure that the item is a valid item.
    itemFlag = False
    while itemFlag == False:
        coffeeItem = input("Please enter the name of the coffee this supplier sells: ")
        coffeeItem = coffeeItem.upper()
        try:
            #Test input against Item database
            executeOnly(f"SELECT NAME FROM Item WHERE NAME = '{coffeeItem}';")
            
            #If the rowcount is 0, the item is not in the table
            if cursor.rowcount == 0:
                print("Invalid coffee. Please select a valid coffee.")

            #Else, item does exist in the table
            else:
                itemFlag = True
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
    executeSelect(f"SELECT s.NAME AS 'Supplier', i.NAME AS 'Coffee' FROM Supplier s LEFT JOIN Inventory_MGMT im ON s.SUPPLIER_ID = im.SUPPLIER_ID LEFT JOIN Item i ON i.ID = im.ITEM_ID WHERE i.NAME = '{coffeeItem}';")


def employeePerformance():
    # Get user input for employee
    employeeName = input("Enter the name employee or performance check: ").upper()

    # Display the employee sales
    print(f"Total sales for {employeeName} shown below.")
    executeOnly(f"SELECT I.NAME as 'Name', I.ROASTING_TYPE as 'Roasting Type', COUNT(I.NAME) as 'Sales Count' FROM Sales M LEFT JOIN Item I ON I.ID = M.ITEM_ID LEFT JOIN Employee E ON E.ID = M.EMPLOYEE_ID WHERE E.NAME = '{employeeName}' GROUP BY I.NAME, I.ROASTING_TYPE;")


    #Check if employee has no sales
    if cursor.rowcount == 0:
        print(f"{employeeName} has sold no items\n")
    else:
        executeSelect(f"SELECT I.NAME as 'Name', I.ROASTING_TYPE as 'Roasting Type', COUNT(I.NAME) as 'Sales Count' FROM Sales M LEFT JOIN Item I ON I.ID = M.ITEM_ID LEFT JOIN Employee E ON E.ID = M.EMPLOYEE_ID WHERE E.NAME = '{employeeName}' GROUP BY I.NAME, I.ROASTING_TYPE;")


def updateItem():
    #Get the item name to update
    itemFlag = False
    while itemFlag == False:
        coffeeItem = input("Please enter the name of the item to update: ")
        coffeeItem = coffeeItem.upper()
        try:
            #Test input against Item database
            executeOnly(f"SELECT NAME FROM Item WHERE NAME = '{coffeeItem}';")
            
            #If the rowcount is 0, the item is not in the table
            if cursor.rowcount == 0:
                print("Item is not in the table. Please select a valid item.")

            #Else, item does exist in the table
            else:
                itemFlag = True
        except ValueError:
            print("Invalid input. Please try again.")

    supplierFlag = False
    while supplierFlag == False:
        supplierID = int(input("Please enter the ID this supplier: "))
        try:
            #Test input against Supplier database
            executeOnly(f"SELECT SUPPLIER_ID FROM Supplier WHERE SUPPLIER_ID = {supplierID};")
            
            #If the rowcount is 0, the Supplier ID is not in the table
            if cursor.rowcount == 0:
                print("Supplier with this ID does not exist.")

            #Else, Supplier_ID does exist in the table
            else:
                supplierFlag = True
        except ValueError:
            print("Invalid input. Please try again using a numeric ID.")

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
    executeOnly(f"SELECT i.Name, im.Total_Available FROM Item i LEFT JOIN Inventory_MGMT im ON i.ID = im.Item_ID WHERE i.Name = '{coffeeItem}' AND im.Supplier_ID = '{supplierID}';")
    if cursor.rowcount == 0:
        print(f"Supplier #{supplierID} does not sell {coffeeItem}. Returning to main menu.")
        return
    else:
        print(f"Current availability for {coffeeItem} sold by Supplier #{supplierID} shown below.")
        executeSelect(f"SELECT i.Name, im.Total_Available FROM Item i LEFT JOIN Inventory_MGMT im ON i.ID = im.Item_ID WHERE i.Name = '{coffeeItem}' AND im.Supplier_ID = '{supplierID}';")

    #Update the item
    print(f"\nUpdating {coffeeItem}")
    executeUpdate(f"UPDATE Inventory_MGMT im, Item i SET Total_Available = {newAvailNum} WHERE i.ID = im.Item_ID AND i.Name = '{coffeeItem}' AND im.Supplier_ID = '{supplierID}';")

    #Display the updated values
    print(f"{coffeeItem}'s total availability, sold by Supplier #{supplierID}, updated successfully. {coffeeItem}'s new availability shown below.")
    executeSelect(f"SELECT i.Name, im.Total_Available FROM Item i LEFT JOIN Inventory_MGMT im ON i.ID = im.Item_ID WHERE i.Name = '{coffeeItem}' AND im.Supplier_ID = '{supplierID}';")


def cancelSales():
    #Get user input for transaction to cancel
    cancelID = input("Enter transaction ID to cancel: ")

    #Display Updated Table
    print("\nPrinting transaction.")
    executeSelect(f"SELECT * FROM Sales M WHERE TRANS_ID = {cancelID};")

    cursor.execute(f"SELECT * FROM Sales M WHERE TRANS_ID = {cancelID};")
    res = (cursor.fetchone())

    #If nothing has been returned, return to the main menu
    if res is None:
        print(f"Transaction #{cancelID} does not exist. Returning to main menu.")
        return
    elif "Reversed" not in res:
        #Update Transaction
        print("\nCanceling transaction.")
        executeUpdate(f"UPDATE Sales SET STATUS = 'Reversed' WHERE TRANS_ID = {cancelID};")

        #Update Stock
        cursor.execute(f"SELECT * FROM Sales M WHERE TRANS_ID = {cancelID};")
        res = (cursor.fetchone())
        if "Reversed" in res:
            print("\nUpdating Inventory.")
            executeUpdate(f"UPDATE Inventory_MGMT im LEFT JOIN Sales s ON s.Item_ID = im.Item_ID SET im.Total_Available = (im.Total_Available + 1) WHERE s.TRANS_ID = {cancelID} AND s.STATUS = 'Reversed';")
        else:
            print(f"\nTransaction #{cancelID} has already been returned. Returning to main menu.")
            return
    elif "Reversed" in res:
        print(f"\nTransaction #{cancelID} has already been returned. Returning to main menu.")
        return

    #Show updated transaction
    print("\nUpdated transaction shown below.")
    executeSelect(f"SELECT * FROM Sales WHERE TRANS_ID = {cancelID};")

    #Show the current stock
    print("\nCurrent stock of item shown below.")
    executeSelect(f"SELECT im.ITEM_ID, im.SUPPLIER_ID, im.TOTAL_ITEM_SALES_3_MONTHS, im.TOTAL_AVAILABLE FROM Sales s LEFT JOIN Inventory_MGMT im ON im.ITEM_ID = s.ITEM_ID WHERE s.TRANS_ID = {cancelID} AND im.TOTAL_ITEM_SALES_3_MONTHS != 0")


def executeUpdate(query):  # use this function for delete and update
    cursor.execute(query)
    conn.commit()


def close_db():  # use this function to close db
    cursor.close()
    conn.close()

def main():

    #Check if int input is on the list
    loop = True
    while loop is True:
        menu()
        #Check if input is a valid int
        numInt = False
        while numInt == False:
            select = input("Enter Option: ")
            try:
                select = int(select)
                numInt = True
            except ValueError:
                print("String detected. Please use numbers 1-6 to select an option.\n")
                menu()

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
        elif select == 6:
            print("Exiting. Goodbye!")
            loop = False
            quit()
        else:
            print(f"{select} is not an option. Please select a valid option from the menu.\n")

    # Close database
    close_db()


##### Test #######
mysql_username = 'dmiao'  # MYSQL Username
mysql_password = 'bieYuj0b'  # MYSQL Password
mysql_host = 'turing.uark.edu'

open_database(mysql_host, mysql_username, mysql_password, mysql_username)  # open database

main()