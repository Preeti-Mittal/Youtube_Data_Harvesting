import streamlit as st
import json
import FetchingData_From_MySQL as fetchsql
import Function_To_Upload_Result_In_Mongodb as upload_func
import Result_Oriented_Function as rof
import Queries_From_SQL as sq

def main():

    st.title('YouTube API')
    html_temp = """
    <div style = "background-color: tomato;padding:10px">
    <h2 style = "color:white; text-align:center;"> YouTube Channel Data Harvesting </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    # Input field for channel_id
    channel_id = st.text_input('Enter Channel ID:', '')


    # Initialize result variable
    result = None

    # Button to trigger data retrieval
    if st.button('Fetch Channel Data'):
        if channel_id:
            result = fetchsql.get_channel_data(channel_id)

            if result:
                st.json(result)  # Display fetched channel data in JSON format
                # Uncomment the following line to upload the fetched data to MongoDB
                # upload_to_mongodb(result)
            else:
                st.error("Channel not found or no data available.")
        else:
            st.warning("Please enter a valid Channel ID.")


        # Button to upload data to MongoDB
    #if result:  # Only execute if result is not None
    if st.button("Upload to MongoDB") and not result:
            # Upload the result to MongoDB
            channel_data_id = str(channel_id)
            upload_func.upload_to_mongodb(channel_data_id)
            st.success("Data uploaded to MongoDB successfully!")

    # Dropdown to select channel name
    channel_names = rof.fetch_channel_names()
    selected_channel = st.selectbox('Select Channel:', channel_names)
    st.write('Select Youtube Channel:', selected_channel)

    connection = sq.connect_to_mysql()
    if connection:
        st.title('YouTube Analytics Dashboard')

        if st.button('Video and Channel Names'):
            video_channel_names = sq.get_video_channel_names(connection)
            st.write("Video and Channel Names:", video_channel_names)

        if st.button('Channels with Most Videos'):
            channels_most_videos = sq.get_channels_with_most_videos(connection)
            st.write("Channels with Most Videos:", channels_most_videos)

        if st.button('Top 10 Most Viewed Videos'):
            top_10_viewed_videos = sq.get_top_10_viewed_videos(connection)
            st.write("Top 10 Most Viewed Videos:", top_10_viewed_videos)

        if st.button('Comments per Video'):
            comments_per_video = sq.get_comments_per_video(connection)
            st.write("Comments per Video:", comments_per_video)

        if st.button('Videos with Highest Likes'):
            videos_highest_likes = sq.get_videos_with_highest_likes(connection)
            st.write("Videos with Highest Likes:", videos_highest_likes)

        if st.button('Likes and Dislikes per Video'):
            likes_dislikes_per_video = sq.get_likes_dislikes_per_video(connection)
            st.write("Likes and Dislikes per Video:", likes_dislikes_per_video)

        if st.button('Views per Channel'):
            views_per_channel = sq.get_views_per_channel(connection)
            st.write("Views per Channel:", views_per_channel)

        if st.button('Channels Published in 2022'):
            channels_published_in_2022 = sq.get_channels_published_in_2022(connection)
            st.write("Channels Published in 2022:", channels_published_in_2022)

        if st.button('Average Duration per Channel'):
            average_duration_per_channel = sq.get_average_duration_per_channel(connection)
            st.write("Average Duration per Channel:", average_duration_per_channel)

        if st.button('Videos with Highest Comments'):
            videos_highest_comments = sq.get_videos_with_highest_comments(connection)
            st.write("Videos with Highest Comments:", videos_highest_comments)


if __name__ == '__main__':
    main()