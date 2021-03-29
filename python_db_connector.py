'''  DO:  more $HOME/.my.cnf to see your MySQL username and  password
#  CHANGE:  MYUSERNAME and MYMYSQLPASSWORD in the test section of
#  this program to your username and mysql password
#  RUN: Python3 python_db_connector.py '''

import mysql.connector
from tabulate import tabulate
           
def open_database (hostname,user_name,mysql_pw,database_name):
      global conn
      conn= mysql.connector.connect(host= hostname, 
      user= user_name,  
      password= mysql_pw, 
      database= database_name 
    ) 
      global cursor
      cursor = conn.cursor() 

def printFormat(result):
    header=[]
    for cd in cursor.description:# get headers
        header.append(cd[0])
    print('')
    print('Query Result:')
    print('')
    print(tabulate(result, headers=header))# print results in table format

# select and display query
def executeSelect (query):
    cursor.execute(query)
    printFormat(cursor.fetchall())

def  insert(table,values):
     query ="INSERT into " + table + " values (" + values + ")" +';'
     cursor.execute(query)
     conn.commit()


def executeUpdate(query): # use this function for delete and update
    cursor.execute(query)
    conn.commit()


def close_db ():  # use this function to close db
    cursor.close()
    conn.close()

##### Test #######
mysql_username = 'MYUSERNAME' # please change to your username
mysql_password ='MYMYSQLPASSWORD'  # please change to your MySQL password

open_database('localhost',mysql_username,mysql_password,mysql_username) # open database   

print(' ')
print('Testing select: ')
print('=======================================')
executeSelect('SELECT * FROM ITEM'); 

print(' ')
print('Testing insert item 22: ')
print('=======================================')
insert('ITEM',"22,'test',23.5,'M'")
executeSelect('SELECT * FROM ITEM where id = 22;')

print(' ')
print('Testing delete item 22: ')
print('=======================================')
executeUpdate('delete from ITEM where id = 22;')
executeSelect('SELECT * FROM ITEM where id = 22;')

print(' ')
print('Testing update of address to Jordan for supplier 3: ');
print('=======================================')
executeSelect("SELECT * FROM SUPPLIER where id = 3;")
executeUpdate("Update SUPPLIER set address = 'JORDAN' where id = 3;")
executeSelect("SELECT * FROM SUPPLIER where id = 3;")
executeUpdate("Update SUPPLIER set address = 'YEMEN' where id = 3;")

close_db()# close database







