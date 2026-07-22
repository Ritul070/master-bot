import sqlite3 

conn = sqlite3.connect('company.db') 
cursor = conn.cursor() 

create_table_sql=''' create table employees(id int, name varchar, department varchar, salary int);''' 

cursor.execute(create_table_sql) 

cursor.execute("insert into employees values(25124, 'Ritul', 'Ai', 50)") 
cursor.execute("insert into employees values(25125, 'Dhruvi', 'Ai', 60);") 
cursor.execute("insert into employees values(25126, 'Roshni', 'Cse', 5);") 
cursor.execute("insert into employees values(25127, 'Tansu', 'Cse', 2);") 

conn.commit() 
conn.close() 

print("Database setup complete!")