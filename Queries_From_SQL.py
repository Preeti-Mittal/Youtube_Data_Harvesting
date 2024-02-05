import mysql.connector
import streamlit as st

# Function to establish connection with MySQL database
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="preeti",
            passwd="Pasw0rd@sql",
            database="Youtube_Data_Scrapping",
            charset="utf8mb4"
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

# Function to execute SQL query and fetch results
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

# What are the names of all the videos and their corresponding channels?
def get_video_channel_names(connection):
    query = """
    SELECT v.Video_Name, c.Channel_Name
    FROM videoid_wise_details v
    INNER JOIN youtube_channels c ON v.Playlist_Id = c.Playlist_Id COLLATE utf8mb4_unicode_ci
    """
    return execute_query(connection, query)

# Which channels have the most number of videos, and how many videos do they have?
def get_channels_with_most_videos(connection):
    query = """
    SELECT c.Channel_Name, c.Channel_Id, COUNT(v.Video_Id) AS Video_Count
    FROM youtube_channels c
    LEFT JOIN videoid_wise_details v ON c.Playlist_Id COLLATE utf8mb4_unicode_ci = v.Playlist_Id COLLATE utf8mb4_unicode_ci
    GROUP BY c.Channel_Name, c.Channel_Id
    ORDER BY Video_Count DESC
    LIMIT 1
    """
    return execute_query(connection, query)

# What are the top 10 most viewed videos and their respective channels?
def get_top_10_viewed_videos(connection):
    query = """
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM videoid_wise_details v
    INNER JOIN youtube_channels c ON v.Playlist_Id COLLATE utf8mb4_unicode_ci = c.Playlist_Id COLLATE utf8mb4_unicode_ci
    ORDER BY v.View_Count DESC
    LIMIT 10
    """
    return execute_query(connection, query)

# How many comments were made on each video, and what are their corresponding video names?
def get_comments_per_video(connection):
    query = """
    SELECT v.Video_Name, COUNT(cm.Comment_Id) AS Comment_Count
    FROM videoid_wise_details v
    LEFT JOIN commentid_wise_details cm ON v.Video_Id = cm.Video_Id
    GROUP BY v.Video_Name
    """
    return execute_query(connection, query)

# Which videos have the highest number of likes, and what are their corresponding channel names?
def get_videos_with_highest_likes(connection):
    query = """
    SELECT v.Video_Name, c.Channel_Name, v.Like_Count
    FROM videoid_wise_details v
    INNER JOIN youtube_channels c ON v.Playlist_Id COLLATE utf8mb4_unicode_ci = c.Playlist_Id COLLATE utf8mb4_unicode_ci
    ORDER BY v.Like_Count DESC
    LIMIT 1
    """
    return execute_query(connection, query)

# What is the total number of likes and dislikes for each video, and what are their corresponding video names?
def get_likes_dislikes_per_video(connection):
    query = """
    SELECT v.Video_Name, SUM(v.Like_Count) AS Total_Likes, SUM(v.Dislike_Count) AS Total_Dislikes
    FROM videoid_wise_details v
    GROUP BY v.Video_Name
    """
    return execute_query(connection, query)

# What is the total number of views for each channel, and what are their corresponding channel names?
def get_views_per_channel(connection):
    query = """
    SELECT c.Channel_Name, SUM(v.View_Count) AS Total_Views
    FROM youtube_channels c
    INNER JOIN videoid_wise_details v ON c.Playlist_Id COLLATE utf8mb4_unicode_ci = v.Playlist_Id COLLATE utf8mb4_unicode_ci
    GROUP BY c.Channel_Name
    """
    return execute_query(connection, query)

# What are the names of all the channels that have published videos in the year 2022?
def get_channels_published_in_2022(connection):
    query = """
    SELECT DISTINCT c.Channel_Name
    FROM youtube_channels c
    INNER JOIN videoid_wise_details v ON c.Playlist_Id COLLATE utf8mb4_unicode_ci = v.Playlist_Id COLLATE utf8mb4_unicode_ci
    WHERE v.PublishedAt COLLATE utf8mb4_unicode_ci LIKE '2022%'
    """
    return execute_query(connection, query)

# What is the average duration of all videos in each channel, and what are their corresponding channel names?
def get_average_duration_per_channel(connection):
    query = """
    SELECT c.Channel_Name, AVG(v.Duration) AS Average_Duration
    FROM youtube_channels c
    INNER JOIN videoid_wise_details v ON c.Playlist_Id COLLATE utf8mb4_unicode_ci = v.Playlist_Id COLLATE utf8mb4_unicode_ci
    GROUP BY c.Channel_Name
    """
    return execute_query(connection, query)

# Which videos have the highest number of comments, and what are their corresponding channel names?
def get_videos_with_highest_comments(connection):
    query = """
    SELECT v.Video_Name, c.Channel_Name, COUNT(cm.Comment_Id) AS Comment_Count
    FROM videoid_wise_details v
    INNER JOIN youtube_channels c ON v.Playlist_Id COLLATE utf8mb4_unicode_ci = c.Playlist_Id COLLATE utf8mb4_unicode_ci
    LEFT JOIN commentid_wise_details cm ON v.Video_Id COLLATE utf8mb4_unicode_ci = cm.Video_Id COLLATE utf8mb4_unicode_ci
    GROUP BY v.Video_Name, c.Channel_Name
    ORDER BY Comment_Count DESC
    LIMIT 1
    """
    return execute_query(connection, query)
