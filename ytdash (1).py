import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Step 1: Load the Excel file
data = pd.read_csv("C:\\Users\\ANSHIKA TANDON\\Downloads\\secondleveljoin1.csv")

# Step 2: Convert columns to appropriate data types
data['publishing_date'] = pd.to_datetime(data['publishing_date'], errors='coerce')


# Step 3: Set up the Streamlit app
st.set_page_config(layout="wide")
st.title('YouTube Analytics Dashboard')

# Sidebar
st.sidebar.title('Dashboard Filters')

# Filter dropdown for playlist
playlist_options = sorted(data['playlist_id'].unique())
selected_playlist = st.sidebar.selectbox('Select Playlist', playlist_options)

# Apply filter on the data
filtered_data = data[data['playlist_id'] == selected_playlist]

# Display the raw data
st.sidebar.subheader('Raw Data')
st.sidebar.dataframe(filtered_data)

# Layout using columns
col1, col2 = st.columns(2)

# Column 1: Bar chart - total_views_count by Video Title
col1.subheader('total_views_count by Video Title')
views_by_video_title = filtered_data.groupby('title_name')['total_views_count'].sum().reset_index()
fig_bar = px.bar(views_by_video_title, x='title_name', y='total_views_count',
                 labels={'title_name': 'Video Title', 'total_views_count': 'total_views_count'},
                 title='total_views_count by Video Title',
                 template='plotly_dark')  # Use dark template for a sleek look
fig_bar.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
fig_bar.update_layout(xaxis_tickangle=-45, xaxis_title=None, yaxis_title='total_views_count')
col1.plotly_chart(fig_bar)

# Add spacing between the charts
col1.write("")

# Column 2: Line chart - Likes, Comments, and Favorites Over Time
col2.subheader('Likes, Comments, and Favorites Over Time')
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=filtered_data['publishing_date'], y=filtered_data['likeCount'],
                             mode='lines', name='Likes', line=dict(color='rgb(255, 127, 14)')))
fig_line.add_trace(go.Scatter(x=filtered_data['publishing_date'], y=filtered_data['commentCount'],
                             mode='lines', name='Comments', line=dict(color='rgb(44, 160, 44)')))
fig_line.add_trace(go.Scatter(x=filtered_data['publishing_date'], y=filtered_data['favoriteCount'],
                             mode='lines', name='Favorites', line=dict(color='rgb(31, 119, 180)')))
fig_line.update_layout(xaxis_title='publishing_date', yaxis_title='Count',
                       title='Likes, Comments, and Favorites Over Time',
                       template='plotly_dark')  # Use dark template for a sleek look
col2.plotly_chart(fig_line)

# Area chart: Subscribers Over Video Title
st.subheader('Area Chart: Subscribers Over Video Title')
fig_area = go.Figure()
for video_title in filtered_data['title_name'].unique():
    video_data = filtered_data[filtered_data['title_name'] == video_title]
    fig_area.add_trace(go.Scatter(x=video_data['title_name'], y=video_data['total_subscriber_count'],
                                  mode='lines', name=video_title, fill='tozeroy'))
fig_area.update_layout(xaxis_title='title_name', yaxis_title='Subscribers',
                       title=f'Area Chart: Subscribers Over Video Title - {selected_playlist}',
                       template='plotly_dark')  # Use dark template for a sleek look
fig_area.update_xaxes(showline=True, linewidth=2, linecolor='white', gridcolor='rgba(255, 255, 255, 0.1)')
fig_area.update_yaxes(showline=True, linewidth=2, linecolor='white', gridcolor='rgba(255, 255, 255, 0.1)')
st.plotly_chart(fig_area)

# Donut chart: Subscribers, Likes, Comments, and Total Views
st.subheader('Metrics Overview')
total_subscribers = filtered_data['total_subscriber_count'].sum()
total_likes = filtered_data['likeCount'].sum()
total_comments = filtered_data['commentCount'].sum()
total_views = filtered_data['total_views_count'].sum()

labels = ['Subscribers', 'Likes', 'Comments', 'Total Views']
values = [total_subscribers, total_likes, total_comments, total_views]
colors = ['rgb(140, 86, 75)', 'rgb(85, 168, 104)', 'rgb(84, 121, 175)', 'rgb(227, 119, 194)']

fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=colors))])
fig_donut.update_layout(title='Metrics Overview', template='plotly_dark')  # Use dark template for a sleek look
fig_donut.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_donut)
