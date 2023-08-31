import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pymongo
from googleapiclient.discovery import build
from PIL import Image

# SETTING PAGE CONFIGURATIONS
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing | By Paila Hemalatha",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded")

# CREATING OPTION MENU
with st.sidebar:
    selected = option_menu(None, ["Home","Extract & Transform","View"],
                           icons=["house-door-fill","tools","card-text"],
                           default_index=0,
                           orientation="vertical"
                           )

#Connection with Mongodb and creating a new database
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Youtube_database"]

#Connection with mysql database
mydb = sql.connect(host="127.0.0.1",
                   user="root",
                   password="Mysql@2023",
                   database= "youtube",
                   port = "3306"
                  )

cursor = mydb.cursor()

# BUILDING CONNECTION WITH YOUTUBE API
api_key = 'AIzaSyAbKVvw49P8TnpEJBEf4WJpcapMioRqEYM'
# channel_ids = "UCihUiDJzjyo2ov_qGtW33lw"
api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client
youtube = build(
    api_service_name, api_version, developerKey=api_key)

#To get the channel details
def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_ids
    )
    response = request.execute()

    # loop through items
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalViews': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads'],
                'Description': item['snippet']['description']

                }
        all_data.append(data)

    return ((all_data))

#To get video IDs
def get_channel_videos(channel_ids):
    video_ids = []
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_ids,
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()

        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids

#To get Video_details
def get_video_details(video_ids):
    video_stats = []

    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i + 50])).execute()
        for video in response['items']:
            video_details = dict(Channel_name=video['snippet']['channelTitle'],
                                 Channel_id=video['snippet']['channelId'],
                                 Video_id=video['id'],
                                 Title=video['snippet']['title'],
                                 Tags=video['snippet'].get('tags'),
                                 Thumbnail=video['snippet']['thumbnails']['default']['url'],
                                 Description=video['snippet']['description'],
                                 Published_date=video['snippet']['publishedAt'],
                                 Duration=video['contentDetails']['duration'],
                                 Views=video['statistics']['viewCount'],
                                 Likes=video['statistics'].get('likeCount'),
                                 Comments=video['statistics'].get('commentCount'),
                                 Favorite_count=video['statistics']['favoriteCount'],
                                 Definition=video['contentDetails']['definition'],
                                 Caption_status=video['contentDetails']['caption']
                                 )
            video_stats.append(video_details)
    return video_stats

#To get comment details
def get_comments_details(video_ids):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=video_ids,
                                                    maxResults=100,
                                                    pageToken=next_page_token).execute()
            for cmt in response['items']:
                data = dict(Comment_id = cmt['id'],
                            Video_id = cmt['snippet']['videoId'],
                            Comment_text = cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_author = cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_posted_date = cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                            Like_count = cmt['snippet']['topLevelComment']['snippet']['likeCount'],
                            Reply_count = cmt['snippet']['totalReplyCount']
                           )
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return comment_data

#Home Page
if selected == "Home":
    col1,col2 = st.columns(2,gap= 'medium')
    col1.markdown("## :Orange[Domain] : Social Media")
    col1.markdown("## :Orange[Technologies used] : Python,MongoDB, Youtube Data API, MySql, Streamlit")
    col1.markdown("## :Orange[Overview] : Retrieving the Youtube channels data from the Google API, storing it in a MongoDB as data lake, migrating and transforming data into a SQL database,then querying the data and displaying it in the Streamlit app.")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.markdown("#   ")

# EXTRACT AND TRANSFORM PAGE
if selected == "Extract & Transform":
    tab1, tab2 = st.tabs(["$\huge 📝 EXTRACT $", "$\huge🚀 TRANSFORM $"])

    # EXTRACT TAB
    with tab1:
        st.markdown("#    ")
        st.write("### Enter YouTube Channel_ID below :")
        ch_id = st.text_input(
            "Hint : Goto channel's home page > Right click > View page source > Find channel_id").split(',')

        if ch_id and st.button("Extract Data"):
            ch_details = get_channel_details(ch_id)
            st.write(f'#### Extracted data from :green["{ch_details[0]["Channel_name"]}"] channel')
            st.table(ch_details)

        if st.button("Upload to MongoDB"):
            with st.spinner('Please Wait for it...'):
                ch_details = get_channel_details(ch_id)
                v_ids = get_channel_videos(ch_id)
                vid_details = get_video_details(v_ids)


                def comments():
                    com_d = []
                    for i in v_ids:
                        com_d += get_comments_details(i)
                    return com_d


                comm_details = comments()

                collections1 = db.channel_details
                collections1.insert_many(ch_details)

                collections2 = db.video_details
                collections2.insert_many(vid_details)

                collections3 = db.comments_details
                collections3.insert_many(comm_details)
                st.success("Data Uploaded to MongoDB successfully !!")

# TRANSFORM TAB
    with tab2:
        st.markdown("#   ")
        st.markdown("### Select a channel to begin Transformation to SQL")
        ch_names = channel_names()
        user_inp = st.selectbox("Select channel", options=ch_names)

#Transform TAB
def insert_into_channels():
    collections = db.channels
    query = """INSERT INTO channel_details VALUES(%s,%s,%s,%s,%s,%s)"""

    for i in collections.find({'channelName': "The Yoga Institute"}, {'_id': 0}):
        cursor.execute(query, tuple(i.values()))
    mydb.commit()

insert_into_channels()

def insert_into_videos():
    collections1 = db.videos
    query1 = """INSERT INTO videos
                (channel_name,channel_id,video_id,video_title,tags,Thumbnail,video_desp,published_st,duration,
                viewCount,likeCount,commentCount,favouriteCount,definition,caption_status)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%S)"""

    for i in collections1.find({"channelName" : "The Yoga Institute"},{'_id' : 0}):
        # values = [str(val).replace("'", "''").replace('"', '""') if isinstance(val, str) else val for val in i.values()]
        cursor.execute(query1, tuple(i.values()))
    mydb.commit()

insert_into_videos()

def insert_into_comments():
    collections1 = db.video_details
    collections2 = db.comments_details
    query2 = """INSERT INTO comments
                (Comment_id,Video_id,Comment_Text,Comment_Author,Comment_Published_At)
                VALUES(%s,%s,%s,%s,%s)"""

    for vid in collections1.find({"channelName" : 'The Yoga Institiute'},{'_id' : 0}):
        for i in collections2.find({'Video_id': vid['Video_id']},{'_id' : 0}):
            cursor.execute(query2,tuple(i.values()))
        mydb.commit()

insert_into_comments()

if st.button("SUBMIT"):
        try:
            insert_into_videos()
            insert_into_channels()
            insert_into_comments()
            st.success("Transformation to MySQL Successful !!")
        except:
            st.error("Channel details already transformed !!")

# VIEW PAGE
if selected == "View":

    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Questions',
                             ['1. What are the names of all the videos and their corresponding channels?',
                              '2. Which channels have the most number of videos, and how many videos do they have?',
                              '3. What are the top 10 most viewed videos and their respective channels?',
                              '4. How many comments were made on each video, and what are their corresponding video names?',
                              '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
                              '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                              '7. What is the total number of views for each channel, and what are their corresponding channel names?',
                              '8. What are the names of all the channels that have published videos in the year 2022?',
                              '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                              '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

    if questions == '1. What are the names of all the videos and their corresponding channels?':
        cursor.execute("""SELECT Video_name AS Video_name, channel_name AS Channel_Name
                            FROM videos
                            ORDER BY channel_name""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)

    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        cursor.execute("""SELECT channel_name AS Channel_Name, total_videos AS Total_Videos
                            FROM channels
                            ORDER BY total_videos DESC""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        # st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        fig = px.bar(df,
                     x=cursor.column_names[0],
                     y=cursor.column_names[1],
                     orientation='v',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        cursor.execute("""SELECT channel_name AS Channel_Name, Video_name AS Video_Title, View_count AS Views 
                            FROM videos
                            ORDER BY views DESC
                            LIMIT 10""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=cursor.column_names[2],
                     y=cursor.column_names[1],
                     orientation='h',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        cursor.execute("""SELECT a.video_id AS Video_id, Video_name AS Video_Title, b.Total_Comments
                            FROM videos AS a
                            LEFT JOIN (SELECT video_id,COUNT(comment_id) AS Total_Comments
                            FROM comments GROUP BY video_id) AS b
                            ON a.video_id = b.video_id
                            ORDER BY b.Total_Comments DESC""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name,Video_name AS Title,Like_count AS Like_Count 
                            FROM videos
                            ORDER BY Like_count DESC
                            LIMIT 10""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=cursor.column_names[2],
                     y=cursor.column_names[1],
                     orientation='h',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        cursor.execute("""SELECT Video_name AS Title, Like_count AS Like_count
                            FROM videos
                            ORDER BY Like_count DESC""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)

    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name, channel_views AS Views
                            FROM channels
                            ORDER BY views DESC""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Channels vs Views :]")
        fig = px.bar(df,
                     x=cursor.column_names[0],
                     y=cursor.column_names[1],
                     orientation='v',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        cursor.execute("""SELECT channel_name AS Channel_Name
                            FROM videos
                            WHERE published_date LIKE '2022%'
                            GROUP BY channel_name
                            ORDER BY channel_name""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)

    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name,
                            AVG(duration)/60 AS "Average_Video_Duration (mins)"
                            FROM videos
                            GROUP BY channel_name
                            ORDER BY AVG(duration)/60 DESC""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Avg video duration for channels :]")
        fig = px.bar(df,
                     x=cursor.column_names[0],
                     y=cursor.column_names[1],
                     orientation='v',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)

    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name,Video_id AS Video_ID,Comment_count AS Comments
                            FROM videos
                            ORDER BY comments DESC
                            LIMIT 10""")
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df,
                     x=cursor.column_names[1],
                     y=cursor.column_names[2],
                     orientation='v',
                     color=cursor.column_names[0]
                     )
        st.plotly_chart(fig, use_container_width=True)
