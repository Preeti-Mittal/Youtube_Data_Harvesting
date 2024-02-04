import Connectivity_MySQL as sql
import json

def get_channel_data(channel_id):


    # Fetch channel data
    query_channel = "SELECT * FROM youtube_channels WHERE Channel_Id = %s"
    sql.mysql_cursor.execute(query_channel, (channel_id,))
    channel_data = sql.mysql_cursor.fetchone()

    if not channel_data:
        return None

    channel_result = {
        "Channel_Name": channel_data[0],
        "Channel_Id": channel_data[1],
        "Subscription_Count": channel_data[2],
        "Channel_Views": channel_data[3],
        "Channel_Description": channel_data[4],
        "Playlist_Id": channel_data[5],
        "Playlist_Details" : [],
        "Videos": []
    }

    # Fetch playlist data
    query_playlist = "SELECT * FROM channels_playlist WHERE Playlist_Id = %s"
    sql.mysql_cursor.execute(query_playlist, (channel_data[5],))
    playlist_data = sql.mysql_cursor.fetchone()

    if not playlist_data:
        return None

    playlist_result = {
        "Number_of_uploads": playlist_data[2],
        "Playlist_Name": playlist_data[1]
    }

    channel_result["Playlist_Details"] = playlist_result

    # Fetch video data
    query_videos = "SELECT * FROM videoid_wise_details WHERE Playlist_Id = %s"
    sql.mysql_cursor.execute(query_videos, (channel_data[5],))
    video_data = sql.mysql_cursor.fetchall()

    for video in video_data:
        video_entry = {
            "Video_Id": video[0],
            "Video_Name": video[1],
            "Tags": video[3].split(',') if video[3] else [],
            "PublishedAt": video[4],
            "View_Count": video[5],
            "Like_Count": video[6],
            "Dislike_Count": video[7],
            "Favorite_Count": video[8],
            "Comment_Count": video[9],
            "Duration": video[10],
            "Thumbnail": video[11],
            "Caption_Status": video[12],
            "Comments": []
        }

        # Fetch comments for each video
        query_comments = "SELECT * FROM commentid_wise_details WHERE Video_Id = %s"
        sql.mysql_cursor.execute(query_comments, (video[0],))
        comments_data = sql.mysql_cursor.fetchall()

        for comment in comments_data:
            video_entry["Comments"].append({
                "Comment_Id": comment[0],
                "Comment_Text": comment[1],
                "Comment_Author": comment[2],
                "Comment_PublishedAt": comment[3]
            })

        channel_result["Videos"].append(video_entry)

    sql.mysql_cursor.close()
    sql.mysql_connection.close()

    return channel_result


# Example usage
# channel_id = "UClVjg4ALRonkQsMbb4I3S0g"
# result = get_channel_data(channel_id)
# if result:
#     # Print the result with pretty formatting
#     print(json.dumps(result, indent=4))
# else:
#     print("Channel not found or no data available.")