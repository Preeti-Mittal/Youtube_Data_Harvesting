import Connectivity_MongoDB as md

db = md.client['Youtube_Data_Scrapping']
result_collection = db['result_data']
#result_collection = db['youtube_channels']

def fetch_channel_names():
    # Query MongoDB collection to retrieve channel names
    channel_names = result_collection.distinct("Channel_Name")
    return channel_names

