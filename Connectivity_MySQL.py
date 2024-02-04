import mysql.connector
mysql_connection = mysql.connector.connect(
                                host = "localhost",
                                user = "preeti",
                                passwd = "Pasw0rd@sql",
                                database = "Youtube_Data_Scrapping",
                                charset="utf8mb4"
)
mysql_cursor = mysql_connection.cursor()
# mysql_cursor.execute("CREATE DATABASE Youtube_Data_Scrapping")

