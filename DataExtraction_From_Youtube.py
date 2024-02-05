# Functions To Scrape Youtube Channel's Info

# Function to get channel basic statistical data

def get_channel_stats(youtube, channel_id):
    response = youtube.channels().list(id=channel_id, part='snippet,statistics,contentDetails')
    channel_data = response.execute()

    channel_informations = {
              'Channel_Name' : channel_data['items'][0]['snippet']['title'],
              'Channel_Id' : channel_data['items'][0]['id'],
              'Subscription_Count' : channel_data['items'][0]['statistics']['subscriberCount'],
              'Channel_Views' : channel_data['items'][0]['statistics']['viewCount'],
              'Channel_Description' : channel_data['items'][0]['snippet']['description'],
              'Playlist_Id' : channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
              'Video_Count' : channel_data['items'][0]['statistics']['videoCount']}
    return channel_informations

# Function to get playlist data of a channel
def get_playlist_details(youtube, playlist_id):
    response = youtube.playlists().list(id=playlist_id, part='snippet,contentDetails')
    playlist_data = response.execute()

    playlist_informations = {
        'Playlist_Id': playlist_data['items'][0]['id'],
        'Channel_Id': playlist_data['items'][0]['snippet']['channelId'],
        'Playlist_Name': playlist_data['items'][0]['snippet']['title'],
        'Number_of_uploads': playlist_data['items'][0]['contentDetails']['itemCount']
    }

    return playlist_informations

# Get the list of all the videos in a playlist of a youtube channel

def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='contentDetails',
                                           maxResults=50)
    response = request.execute()

    video_ids = []
    for i in range(0, len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(playlistId=playlist_id,
                                                   part='contentDetails',
                                                   maxResults=50,
                                                   pageToken=next_page_token)
            response = request.execute()
            for i in range(0, len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')

    return video_ids


# Function to get the details of videos in the playlist

# Function to get video data in nested form
def get_video_details(youtube, video_ids):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(part='snippet,contentDetails,statistics',
                                        id=','.join(video_ids[i:i + 50]))
        response = request.execute()

        for video in response['items']:
            video_stats = dict(
                Video_Id=video['id'],
                Video_Name=video['snippet']['title'],
                # Video_Description=video['snippet']['description'],
                Tags=video['snippet'].get('tags', 0),
                PublishedAt=video['snippet']['publishedAt'],
                View_Count=video['statistics'].get('viewCount', 0),
                Like_Count=video['statistics'].get('likeCount', 0),
                Dislike_Count=video['statistics'].get('dislikeCount', 0),
                Favorite_Count=video['statistics'].get('favoriteCount', 0),
                Comment_Count=video['statistics'].get('commentCount', 0),
                Duration=video['contentDetails'].get('duration', 0),
                Thumbnail=video['snippet']['thumbnails']['default']['url'],
                Caption_Status=video['contentDetails'].get('caption', 'None')
            )

            all_video_stats.append(video_stats)
    return all_video_stats

# Function to get video_id wise data
def get_video_details_videoidwise(youtube, channel_id, video_ids):
    channel_response = youtube.channels().list(id=channel_id, part='snippet,statistics,contentDetails')
    channel_data = channel_response.execute()
    Playlist_Id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(part='snippet,contentDetails,statistics',
                                        id=','.join(video_ids[i:i + 50]))
        response = request.execute()

        for video in response['items']:
            video_stats = dict(
                Video_Id=video['id'],
                Video_Name=video['snippet']['title'],
                Playlist_Id=Playlist_Id,
                Tags=video['snippet'].get('tags', 0),
                PublishedAt=video['snippet']['publishedAt'],
                View_Count=video['statistics'].get('viewCount', 0),
                Like_Count=video['statistics'].get('likeCount', 0),
                Dislike_Count=video['statistics'].get('dislikeCount', 0),
                Favorite_Count=video['statistics'].get('favoriteCount', 0),
                Comment_Count=video['statistics'].get('commentCount', 0),
                Duration=video['contentDetails'].get('duration', 0),
                Thumbnail=video['snippet']['thumbnails']['default']['url'],
                Caption_Status=video['contentDetails'].get('caption', 'None')
            )

            all_video_stats.append(video_stats)
    return all_video_stats

# Function to get the comment details of a video

def get_comment_ids(youtube, video_id):
    request = youtube.commentThreads().list(videoId=video_id,
                                            part='snippet',
                                            maxResults=100)
    response = request.execute()

    Video_Id = video_id

    comments = []
    for comment in response['items']:
        comment_details = dict(
            Comment_Id=comment['snippet']['topLevelComment']['id'],
            Comment_Text=comment['snippet']['topLevelComment']['snippet']['textDisplay'],
            Comment_Author=comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            Comment_PublishedAt=comment['snippet']['topLevelComment']['snippet']['publishedAt'])

        comments.append(comment_details)
    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.commentThreads().list(videoId=video_id,
                                                    part='snippet',
                                                    maxResults=100,
                                                    pageToken=next_page_token)
            response = request.execute()
    for comment in response['items']:
        comment_details = dict(
            Comment_Id=comment['snippet']['topLevelComment']['id'],
            Comment_Text=comment['snippet']['topLevelComment']['snippet']['textDisplay'],
            Comment_Author=comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            Comment_PublishedAt=comment['snippet']['topLevelComment']['snippet']['publishedAt'],
            Video_Id=Video_Id)
        comments.append(comment_details)

        next_page_token = response.get('nextPageToken')
    return comments

# Function to pull max 5 comments for a video

def get_comment_ids_only5(youtube, video_id):
    request = youtube.commentThreads().list(videoId=video_id,
                                            part='snippet',
                                            maxResults=5)
    Video_Id = video_id
    response = request.execute()

    comments = []
    for comment in response['items']:
        comment_details = dict(
            Comment_Id=comment['snippet']['topLevelComment']['id'],
            Comment_Text=comment['snippet']['topLevelComment']['snippet']['textDisplay'],
            Comment_Author=comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            Comment_PublishedAt=comment['snippet']['topLevelComment']['snippet']['publishedAt'],
            Video_Id=Video_Id)

        comments.append(comment_details)

    return comments



