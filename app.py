import streamlit as st
import json
import FetchingData_From_MySQL as fetchsql
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


    # Button to trigger data retrieval
    if st.button('Fetch Channel Data'):
        if channel_id:
            result = fetchsql.get_channel_data(channel_id)

            if result:
                #st.write(json.dumps(result, indent=4))
                st.json(result)
            else:
                st.error("Channel not found or no data available.")
        else:
            st.warning("Please enter a valid Channel ID.")

if __name__ == '__main__':
    main()