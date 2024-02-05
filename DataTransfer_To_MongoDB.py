import Connectivity_MongoDB as md
import Connectivity_Youtube as yt
import DataExtraction_From_Youtube as fn

db = md.client['Youtube_Data_Scrapping'] # Creating database in mongodb

#Collection For "Youtube Channels" Details in mongodb
channels_details = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    channels_details.append(channel_info)

channel_collection = db['youtube_channels'] # Creating collection in mongodb
channel_collection.insert_many(channels_details) # Inserting data into mongodb collection(youtube_channels)
print("Data inserted successfully.")

# Collection For Channel's Playlist in mongodb
playlist_details = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    playlist_id = channel_info['Playlist_Id']

    playlist_info = fn.get_playlist_details(yt.youtube, playlist_id)
    playlist_details.append(playlist_info)

playlist_collection = db['channels_playlist']
playlist_collection.insert_many(playlist_details) # Inserting data into mongodb collection(channels_playlist)
print("Data inserted successfully.")

# Collection For Videos in a playlist in mongodb
#Nested Collection
videos_details = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    playlist_id = channel_info['Playlist_Id']
    playlist_name = fn.get_playlist_details(yt.youtube, playlist_id)['Playlist_Name']
    video_ids_list = fn.get_video_ids(yt.youtube, playlist_id)
    video_ids_stats = fn.get_video_details(yt.youtube, video_ids_list)
    document = {"Playlist_id": playlist_id,
                "Playlist_name": playlist_name,
                "Videos": video_ids_stats}
    videos_details.append(document)

video_collection = db['channels_videos']
for video in videos_details:
    video_collection.insert_one(video) # Inserting data into mongodb collection(channels_videos)
print("Data inserted successfully.")

# Video-ID wise collection¶
video_id_details = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    playlist_id = channel_info['Playlist_Id']
    playlist_name = fn.get_playlist_details(yt.youtube, playlist_id)['Playlist_Name']
    video_ids_list = fn.get_video_ids(yt.youtube, playlist_id)
    video_ids_stats = fn.get_video_details_videoidwise(youtube=yt.youtube, channel_id = channel, video_ids = video_ids_list)
    video_id_details.append(video_ids_stats)

videoid_wise_collection = db['VideoId_Wise_Details']

for video in video_id_details:
    videoid_wise_collection.insert_many(video) # Inserting data into mongodb collection(VideoId_Wise_Details)
print("Data inserted successfully.")

# Collection For comments in videos
# Nested Comment Table
all_comments = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    playlist_id = channel_info['Playlist_Id']
    playlist_name = fn.get_playlist_details(yt.youtube, playlist_id)['Playlist_Name']
    video_ids_list = fn.get_video_ids(yt.youtube, playlist_id)

    channel_data = {
        "Channel_Id": channel_info['Channel_Id'],
        "Channel_Name": channel_info['Channel_Name'],
        "Playlist_Id": playlist_id,
        "Playlist_Name": playlist_name,
        "Videos_With_Comments": []
    }
    for video_id in video_ids_list:
        try:
            video_comments = fn.get_comment_ids_only5(yt.youtube, video_id)

            video_data = {
                "Comments": video_comments
            }

            channel_data["Videos_With_Comments"].append(video_data)

        except yt.googleapiclient.errors.HttpError as e:
            if e.resp.status == 403:
                print(f"Comments are disabled for the video: {video_id}")
            else:
                print(f"An error occurred for the video {video_id}: {e}")

    all_comments.append(channel_data)

comments_collection = db['channels_comments']
for document in all_comments:
    comments_collection.insert_one(document) # Inserting data into mongodb collection(channels_comments)
print("Data inserted successfully.")

# CommentID wise Table

all_comments = []
for channel in yt.channel_list:
    channel_info = fn.get_channel_stats(yt.youtube, channel_id=channel)
    playlist_id = channel_info['Playlist_Id']
    video_ids_list = fn.get_video_ids(yt.youtube, playlist_id)

    comments_list = []
    for video_id in video_ids_list:
        try:
            video_comments = fn.get_comment_ids_only5(yt.youtube, video_id)
            comments_list.append(video_comments)

        except yt.googleapiclient.errors.HttpError as e:
            if e.resp.status == 403:
                print(f"Comments are disabled for the video: {video_id}")
            else:
                print(f"An error occurred for the video {video_id}: {e}")

    all_comments.append(comments_list)

commentids_collection = db['CommentId_Wise_Details']
# Insert each comment data into MongoDB
for documents in all_comments:
    for document_list in documents:
        for document in document_list:
            commentids_collection.insert_one(document) # Inserting data into mongodb collection(CommentId_Wise_Details)
print("Data inserted successfully.")





