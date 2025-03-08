import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
try:
    with mydb.cursor() as db_cursor:
        db_cursor.execute("CREATE DATABASE munchmate")
except Exception as e:
    print("Error running sql connection/command: ", e)

# FAQ for setup
# location of db files -> SHOW VARIABLES LIKE "datadir";
# port of the sql server -> SHOW VARIABLES LIKE "port";
# on windows: type "C:\ProgramData\MySQL\MySQL Server 8.0\my.ini" | findstr "port"
# on linux: cat /etc/mysql/my.cnf | grep port


# test mysql -> mysql -u root -p or mysql -u root
# change root with the different user and set password if exist for the local sql server

# python createsuperuser --> python manage.py createsuperuser --username=mishra --email=anuraagmishra.214@gmail.com

# mysql --> use munchmate --> select * from auth_users


