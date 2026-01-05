import sqlite3

## connect to sqlite
connection=sqlite3.connect("student.db")

# Create a cursor to insert record, create table
cursor=connection.cursor()

# Create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

# Insert some more records
cursor.execute('''INSERT INTO STUDENT VALUES('Kashyap','Data Science','A',100)''')
cursor.execute('''INSERT INTO STUDENT VALUES('John','Data Science','B',90)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Mukesh','Data Science','A',86)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Jacob','DEVOPS','A',50)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Dipesh','DEVOPS','A',35)''')

## Display all the records
print("The inserted records are")
data=cursor.execute('''SELECT * from STUDENT''')
for row in data:
    print(row)

# Commit changes in the database
connection.commit() 
connection.close()