import Connectivity_MongoDB as md
import DataExtraction_From_Youtube as fn
import Connectivity_Youtube as yt


def upload_to_mongodb(channel_id):


    channel_list = [channel_id]

    all_comments = []

    for channel in channel_list:
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

    db = md.client['Youtube_Data_Scrapping']
    result_collection = db['result_data']

    for document in all_comments:
        result_collection.insert_one(document)

    print("Data inserted successfully.")

