import Connectivity_MySQL as sql
import Connectivity_MongoDB as md
import DataTransfer_To_MongoDB as data_md

#Creating Table "Youtube_Channels" in MySQL Database
sql.mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS Youtube_Channels (
    Channel_Id VARCHAR(255) PRIMARY KEY,
    Channel_Name VARCHAR(255),
    Subscription_Count INT,
    Channel_Views INT,
    Channel_Description VARCHAR(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Playlist_Id VARCHAR(255),
    Video_Count INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""")
# Retrieve data from MongoDB collection and insert into MySQL

for document in data_md.channel_collection.find(): # Extract data from MongoDB document
    Channel_Id = str(document['Channel_Id'])
    Channel_Name = document['Channel_Name']
    Subscription_Count = document['Subscription_Count']
    Channel_Views = document['Channel_Views']
    Channel_Description = document['Channel_Description']
    Playlist_Id = document['Playlist_Id']
    Video_Count = document['Video_Count']

    # Encode strings to UTF-8
    Channel_Description_utf8 = Channel_Description.encode('utf-8')

    # Insert data into MySQL table
    sql.mysql_cursor.execute("""
        INSERT INTO Youtube_Channels (Channel_Id, Channel_Name, Subscription_Count, Channel_Views, Channel_Description, Playlist_Id, Video_Count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (Channel_Id, Channel_Name, Subscription_Count, Channel_Views, Channel_Description_utf8, Playlist_Id, Video_Count))

sql.mysql_connection.commit()
sql.mysql_connection.close()
md.client.close()


# Creating Table "Channels_Playlist" in MySQL Database¶
sql.mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS Channels_Playlist (
    Playlist_Id VARCHAR(255) PRIMARY KEY,
    Channel_Id VARCHAR(255) ,
    Playlist_Name TEXT,
    Number_of_uploads INT
    )
""")

# Retrieve data from MongoDB collection and insert into MySQL
for document in data_md.playlist_collection.find():
    Playlist_Id = str(document['Playlist_Id'])
    Channel_Id = str(document['Channel_Id'])
    Playlist_Name = document['Playlist_Name']
    Number_of_uploads = document['Number_of_uploads']

    # Insert data into MySQL table
    sql.mysql_cursor.execute("""
        INSERT INTO Channels_Playlist (Playlist_Id, Channel_Id, Playlist_Name, Number_of_uploads)
        VALUES (%s, %s, %s, %s)
    """, (Playlist_Id, Channel_Id, Playlist_Name, Number_of_uploads))

# Commit changes and close connections
sql.mysql_connection.commit()
sql.mysql_connection.close()
md.client.close()

# Creating Table "VideoId_Wise_Details" in MySQL Database
sql.mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS VideoId_Wise_Details(
    Video_Id VARCHAR(255) PRIMARY KEY,
    Video_Name VARCHAR(255) ,
    Playlist_Id VARCHAR(255),
    Tags VARCHAR(2000),
    PublishedAt VARCHAR(255),
    View_Count INT,
    Like_Count INT,
    Dislike_Count INT,
    Favorite_Count INT,
    Comment_Count INT,
    Duration VARCHAR(255),
    Thumbnail VARCHAR(255),
    Caption_Status TEXT
      )
""")
# Retrieve data from MongoDB collection and insert into MySQL
for document in data_md.videoid_wise_collection.find():
    Video_Id = document['Video_Id']
    Video_Name = document['Video_Name']
    Playlist_Id = document['Playlist_Id']
    if 'Tags' in document and isinstance(document['Tags'], list):
        tags_str = ', '.join(document['Tags'])
    else:
        tags_str = ''
    PublishedAt = document['PublishedAt']
    View_Count = document['View_Count']
    Like_Count = document['Like_Count']
    Dislike_Count = document['Dislike_Count']
    Favorite_Count = document['Favorite_Count']
    Comment_Count = document['Comment_Count']
    Duration = document['Duration']
    Thumbnail = document['Thumbnail']
    Caption_Status = str(document['Caption_Status'])

    # Insert data into MySQL table
    sql.mysql_cursor.execute("""
        INSERT INTO VideoId_Wise_Details (Video_Id, Video_Name, Playlist_Id, Tags, PublishedAt, View_Count, Like_Count, Dislike_Count, Favorite_Count, 
        Comment_Count,  Duration, Thumbnail,  Caption_Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
    """, (Video_Id, Video_Name, Playlist_Id, tags_str, PublishedAt, View_Count, Like_Count, Dislike_Count, Favorite_Count,
        Comment_Count,  Duration, Thumbnail,  Caption_Status))

# Commit changes and close connections
sql.mysql_connection.commit()
sql.mysql_connection.close()
md.client.close()

# Creating Table "CommentId_Wise_Details" in MySQL Database
sql.mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS CommentId_Wise_Details_final(
    Comment_Id VARCHAR(255) PRIMARY KEY,
    Comment_Text VARCHAR(5000) ,
    Comment_Author VARCHAR(255),
    Comment_PublishedAt VARCHAR(250),
    Video_Id VARCHAR(255)
        )
""")

# Retrieve data from MongoDB collection and insert into MySQL
for document in data_md.commentids_collection.find():
    # Extract data from MongoDB document

    Comment_Id = document['Comment_Id']
    Comment_Text = document['Comment_Text'][:5000]
    Comment_Author = document['Comment_Author']
    Comment_PublishedAt = document['Comment_PublishedAt']
    Video_Id = document['Video_Id']

    sql.mysql_cursor.execute("""
        INSERT INTO CommentId_Wise_Details_final (Comment_Id, Comment_Text, Comment_Author, Comment_PublishedAt, Video_Id)
        VALUES (%s, %s, %s, %s, %s)
    """, (Comment_Id, Comment_Text, Comment_Author, Comment_PublishedAt, Video_Id))

# Commit changes and close connections
sql.mysql_connection.commit()
sql.mysql_connection.close()
md.client.close()


