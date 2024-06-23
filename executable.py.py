import pandas as pd
import csv
import googleapiclient.discovery
import os.path

API_KEY='AIzaSyDGQDH-sKHhAR4cmQjWTxCHbgzNY9v4Nlg'
channel_username = "@psitkanpur"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = API_KEY='AIzaSyDGQDH-sKHhAR4cmQjWTxCHbgzNY9v4Nlg'
channel_id = 'UC03XHJR0rh4t9MwwojbbiaA'
videoIds = []

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

#############################get_channeldetails- start##########################
#This function will provide the basic details of the channel only.
def get_channeldetails(channel_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=channel_id,
   )
    response = request.execute()
    channel_title_name=response ['items'][0]['snippet']['title']
    totalchannel_views_count=response ['items'][0]['statistics']['viewCount']
    total_subscriber_count=response ['items'][0]['statistics']['subscriberCount']
    total_video_count=response['items'][0]['statistics']['videoCount']
    data=[]
    extracteddata=dict(channel_title_name=response['items'][0]['snippet']['title'],totalchannel_views_count=response ['items'][0]['statistics']['viewCount'],total_subscriber_count=response ['items'][0]['statistics']['subscriberCount'],total_video_count=response['items'][0]['statistics']['videoCount'])
    data.append(extracteddata)
    datanew=pd.DataFrame(data)

    #print (datanew)
    with open('C:\\Users\\ANSHIKA TANDON\\Downloads\\channnel details1.csv', 'w',encoding="utf-8",newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['channel_id','channel_title_name','totalchannel_views_count','total_subscriber_count','total_video_count'])
        filewriter.writerow([channel_id,channel_title_name,totalchannel_views_count,total_subscriber_count,total_video_count])
###############################get_channeldetails- end#######################################        

#######################################get_playlistId- start##########################
#This function will provide the playlist id and merge with channel id
def get_playlistId(channel_id):
    playlist = []
    nextPageToken = None  # Initialize nextPageToken to None
    extra_pages_is_there = True
    
    # Keep fetching videos until all pages have been fetched
    while extra_pages_is_there:
        request = youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=50
        )
        response = request.execute()
        #print(response)
        #print('------->',playlist)# Append videos from this page to the playlist
        nextPageToken = response.get('nextPageToken')
        extra_pages_is_there = nextPageToken is not None
        #print(playlist)    
        with open('C:\\Users\\ANSHIKA TANDON\\Downloads\\playlistid_dips1.csv', 'w',encoding="utf-8",newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['channel_id','playlist_id','playlist_name'])
            for i in range(len(response['items'])):
                #print(len(response['items'])) 
                playlist.append(response['items'][i]['id'])
                playlist_id = response['items'][i]['id']
                playlist_name = response['items'][i]['snippet']['title']
                #print(playlist_id,' ', playlist_name)
                filewriter.writerow([channel_id,playlist_id,playlist_name])
            
######################get_playlistId- end##########################

##############################start-fetchingvideo_details########################################
def youtube_videoId(playlistId):
    videolist = []
    nextPageToken = None  # Initialize nextPageToken to None
    extra_pages_is_there = True
    
    # Keep fetching videos until all pages have been fetched
    while extra_pages_is_there:
        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId=playlistId,
            pageToken=nextPageToken  # Pass nextPageToken in the request
        )
        response = request.execute() 
        listing_video_indi= get_video_ids(response)
        if listing_video_indi:
            #print("list is not empty")
            videolist.extend(listing_video_indi)
            print(playlistId,videolist)
            get_videodetails(playlistId,videolist)
        else:
            #print("list is empty")
            break
        nextPageToken = response.get('nextPageToken')
        extra_pages_is_there = nextPageToken is not None
        
    return videolist

def get_video_ids(response):
    videolist = []
    length = len(response['items'])
    for i in range(length):
        videolist.append(response['items'][i]['contentDetails']['videoId'])
    if len(response['items'][i]['contentDetails']) > 1 :
        return videolist
    else:
        return None    
        
playlistId = ['PLykDsmqqAtOqXxfmOU-oyZbPJWlR8EQhf','PLykDsmqqAtOpp3Ekr3XdDXzv0kX3OR988','PLykDsmqqAtOrGT6KiDBnzEj5uGzYy5yN-','PLykDsmqqAtOq_KV5eYfja4MBFzy3QwZ0g','PLykDsmqqAtOrWRybth-jJJ1nU6aENQAhQ','PLykDsmqqAtOqrk_aGgWwgyNfu4WObWhDF','PLykDsmqqAtOr0dDi9estaSc4VVUEzCj7U','PLykDsmqqAtOqA3H0DeVL1bmDPdGvCXCF_','PLykDsmqqAtOqg5IAR2tlB0C4lbpXpoZEf','PLykDsmqqAtOpw3AGsNY7Yb6tHWQANZZRR']


def get_videodetails(playlist_id,videolist):
    
    videoDetails=[]
    print('------->',playlist_id,'-----------',videolist)
    file_exists = os.path.isfile('C:\\Users\\ANSHIKA TANDON\\Downloads\\aaa1.csv')
    headers = ['playlist_id','video_id','title_name', 'liveBroadcastContent','total_views_count','publishing_date','likeCount','favoriteCount','commentCount']
    with open('C:\\Users\\ANSHIKA TANDON\\Downloads\\aaa1.csv', 'a',encoding="utf-8",newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if not file_exists:
                filewriter.writerow(headers)
            for i in range(len(videolist)):
                #print('@@@@@@',videolist[i])
                request = youtube.videos().list(part="snippet,statistics",id=videolist[i])
                response = request.execute()
                #print(response)
                if len(response['items']) > 0:
                   title_name=response['items'][0]['snippet']['title']
                
                   liveBroadcastContent=response['items'][0]['snippet']['liveBroadcastContent']
                   publishing_date=response['items'][0]['snippet']['publishedAt']
                   total_views_count=response['items'][0]['statistics']['viewCount']
                   total_like_count=response ['items'][0]['statistics']['likeCount']
                   total_favorite_count=response['items'][0]['statistics']['favoriteCount']
                
                #total_comment_count=response['items'][0]['statistics']['commentCount']
                   data=[]
                   extracteddata=dict(title=response['items'][0]['snippet']['title'],liveBroadcastContent=response['items'][0]['snippet']['liveBroadcastContent'],publishing_date=response['items'][0]['snippet']['publishedAt'],total_like_count=response ['items'][0]['statistics']['likeCount'],total_favorite_count=response['items'][0]['statistics']['favoriteCount'])
                   data.append(extracteddata)
                else:
                     #print("The response['items'] list is empty!") 
                     return None
                print(playlist_id,videolist[i],title_name,liveBroadcastContent,total_views_count,publishing_date,total_like_count,total_favorite_count, '''total_comment_count''')
                value = [playlist_id,videolist[i],title_name,liveBroadcastContent,total_views_count,publishing_date,total_like_count,total_favorite_count, '''total_comment_count''']

                datanew=pd.DataFrame(data)
                filewriter.writerow([playlist_id,videolist[i],title_name,liveBroadcastContent,total_views_count,publishing_date,total_like_count,total_favorite_count,''' total_comment_count'''])
                
for i in playlistId :
    youtube_videoId(i)
##############################end-start-fetchingvideo_details###########################################
get_channeldetails(channel_id)
get_playlistId(channel_id)

###############################start-combining-channel-playlist#########################################

csv1 = pd.read_csv("C:\\Users\\ANSHIKA TANDON\\Downloads\\channnel details1.csv")
csv1.head()

csv2 = pd.read_csv("C:\\Users\\ANSHIKA TANDON\\Downloads\\playlistid_dips1.csv")
csv2.head()

merged_data = csv1.merge(csv2,on=["channel_id"])
print (merged_data.head())

df = merged_data.head()
df.to_csv("C:\\Users\\ANSHIKA TANDON\\Downloads\\firstleveljoin1.csv")

# ###############################end-combining-channel-playlist#########################################
###############################start-combining-channel-playlist-video#########################################
csv3 = pd.read_csv("C:/Users/ANSHIKA TANDON/Downloads\\firstleveljoin1.csv" )
csv3.head()
print(csv3)

csv4= pd.read_csv("C:/Users/ANSHIKA TANDON/Downloads/aaa1.csv")
csv4.head()

result = pd.merge(csv3, csv4, how="outer", on=["playlist_id"])
print(result)

result.to_csv("C:\\Users\\ANSHIKA TANDON\\Downloads\\secondleveljoin1.csv")
###############################end-combining-channel-playlist-video#########################################





