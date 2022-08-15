import streamlit as st
import spotipy 
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import polarplotting
import song_recommender

SPOTIFY_CLIENT_ID='457931e97e5147c791993bdbc1b5217e'
SPOTIFY_SECRET_KEY='9ac77fd6919b431b92f7b2d96fd78d5b'

auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_SECRET_KEY)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title('Spotify Analysis App')

st.sidebar.header("Welcome to Spotify")


search_choices = ['Song/Track', 'Artist', 'Album']
search_selected = st.sidebar.selectbox(" Search : ", search_choices)

search_keyword = st.text_input(search_selected + " ( Enter what you want to search ) ")
button_clicked = st.button("Search")


search_results = []
tracks = []
artists = []
albums = []
if search_keyword is not None and len(str(search_keyword)) > 0:
    if search_selected == 'Song/Track':
        st.subheader("Search Results For Songs/Tracks with" + " ' " + search_keyword + " ' ")
        tracks = sp.search(q='track:'+ search_keyword,type='track', limit=20)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list) > 0:
            for track in tracks_list:
                #st.write(track['name'] + " - By - " + track['artists'][0]['name'])
                search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])
        
    elif search_selected == 'Artist':
        st.subheader("Search Results in Artists for" + " ' " + search_keyword + " ' ")
        artists = sp.search(q='artist:'+ search_keyword,type='artist', limit=20)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                # st.write(artist['name'])
                search_results.append(artist['name'])
        
    if search_selected == 'Album':
        st.subheader("Search Results in Albums for" + " ' " + search_keyword + " ' ")
        albums = sp.search(q='album:'+ search_keyword,type='album', limit=20)
        albums_list = albums['albums']['items']
        if len(albums_list) > 0:
            for album in albums_list:
                # st.write(album['name'] + " - By - " + album['artists'][0]['name'])
                # print("Album ID: " + album['id'] + " / Artist ID - " + album['artists'][0]['id'])
                search_results.append(album['name'] + " - By - " + album['artists'][0]['name'])

selected_album = None
selected_artist = None
selected_track = None
if search_selected == 'Song/Track':
    selected_track = st.selectbox("Select your song/track: ", search_results)
elif search_selected == 'Artist':
    selected_artist = st.selectbox("Select your artist: ", search_results)
elif search_selected == 'Album':
    selected_album = st.selectbox("Select your album: ", search_results)


if selected_track is not None and len(tracks) > 0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']
                col41,col42,col43=st.columns((4,4,4))
                col43.image(img_album,caption=track_album)
                col41.write("Track Album: " + track_album)
                col42.write("Track ID: "+ track_id)
   
    selected_track_choice = None
    if track_id is not None:
        track_choices = ['Song Features','Similar Songs Recommendations']
        selected_track_choice = st.sidebar.selectbox('Please select your track choice :',track_choices)
        if selected_track_choice == 'Song Features':
            track_features=sp.audio_features(track_id)
            df=pd.DataFrame(track_features,index=[0])
            df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            st.dataframe(df_features)
            polarplotting.feature_plot(df_features)
        elif selected_track_choice == 'Similar Songs Recommendations':
            token = song_recommender.get_token(SPOTIFY_CLIENT_ID,SPOTIFY_SECRET_KEY)
            similar_songs_json = song_recommender.get_track_recommendations(track_id,token)
            recommendation_list=similar_songs_json['tracks']
            recommendation_list_df=pd.DataFrame(recommendation_list)
            recommendation_df= recommendation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
            st.dataframe(recommendation_df)
            song_recommender.song_recommendation_vis(recommendation_df)
    else:

        st.write("Please choose a track from the list")


elif selected_album is not None and len(selected_album)>0:
       albums_list = albums['albums']['items']
       album_id=None
       album_uri=None
       album_name=None

       if len(albums_list) > 0:
            for album in albums_list:
                str_temp = album['name'] + " - By - " + album['artists'][0]['name']
                if selected_album == str_temp:
                    album_id=album['id']
                    album_uri=album['uri']
                    album_name=album['name']
       
       if album_id is not None and album_uri is not None :
            st.write("Collecting all the tracks for the album... "+ " ' "+ album_name + " ' ")
            album_tracks=sp.album_tracks(album_id)
            album_tracks_df=pd.DataFrame(album_tracks['items'])
            #st.dataframe(album_tracks_df)
            df_tracks_min=album_tracks_df.loc[:,
                                     ['id','name','duration_ms','explicit','preview_url']]
            #st.dataframe(df_tracks_min)

            for idx in df_tracks_min.index:
                with st.container():
                    col1, col3, col4 = st.columns((4,1,1))
                    col11, col12 = st.columns((8,4))
                    col1.subheader(df_tracks_min['name'][idx])
                    #col2.write(df_tracks_min['id'][idx])
                    col3.write("Duration")
                    col3.write(df_tracks_min['duration_ms'][idx])
                    col4.write("Explicit")
                    col4.write(df_tracks_min['explicit'][idx])   
                    if df_tracks_min['preview_url'][idx] is not None:
                        #col11.write(df_tracks_min['preview_url'][idx])  
                        with col11:   
                            st.audio(df_tracks_min['preview_url'][idx], format="audio/mp3")  

elif selected_artist is not None and len(artists) > 0:
    artists_list = artists['artists']['items']
    artist_id=None
    artist_uri=None
    selected_artist_choice=None
    if len(artists_list) > 0:
        for artist in artists_list:
            # st.write(artist['name'])
            if selected_artist == artist['name']:
                artist_id=artist['id']
                artist_uri=artist['uri']
    
    if artist_id is not None :
        artist_choice = ['Albums','Top Songs']
        selected_artist_choice= st.sidebar.selectbox('Select Artist Choice :',artist_choice)
    
    if selected_artist_choice is not None:
        if selected_artist_choice == 'Albums':
            st.subheader("Collecting Albums...")
            artist_uri ='spotify:artist:'+ artist_id
            album_result = sp.artist_albums(artist_uri,album_type='album')
            all_albums = album_result['items']
            col1,col2,col3=st.columns((6,3,3))
            for album in all_albums:
                col1.markdown("***Album :***")
                col1.markdown(album['name'])
                col1.write("------------------")
                col2.markdown("Release Date")
                col2.markdown(album['release_date'])
                col2.write("------------------")
                col3.markdown("Total Tracks")
                col3.markdown( album['total_tracks'])
                col3.write("------------------")
        
        elif selected_artist_choice == 'Top Songs':
            artist_uri = 'spotify:artist:' + artist_id
            top_songs_result = sp.artist_top_tracks(artist_uri)
            
            for track in top_songs_result['tracks'][:10]:
                with st.container():
                    col1,col2,col3, col4 = st.columns((4,2,2,2))
                    col11, col12 = st.columns((8,2))
                    col21, col22 = st.columns((6,6))
                    col31, col32 = st.columns((11,1))
                    col7=st.columns((12,3))
                    col1.subheader(track['name'])
                    artist_img = track['album']['images'][0]['url']
                    col4.image(artist_img)
                    col2.write(track['id'])
                    track_id=track['id']
                    col2.write(track_id)
                    def feature_requested():
                                #st.write(track['id'])
                               
                                track_features  = sp.audio_features(track_id) 
                                df = pd.DataFrame(track_features, index=[0])
                                df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                                
                                with st.sidebar:
                                    tab3,tab4=st.tabs(["Audio Features", " Audio Visualization"])
                                    with tab3:
                                        st.dataframe(df_features)
                                    with tab4:
                                        polarplotting.feature_plot(df_features)

                    
                    #col3.markdown("***Duration***")
                    #col3.write(track['duration_ms'])
                    #col4.markdown("***Popularity***")
                    col2.metric("Popularity : "," ",delta=track['popularity'])
                    if track['preview_url'] is not None:
                        #col11.write(df_tracks_min['preview_url'][idx]) 
                        with col11:   
                            st.audio(track['preview_url'], format="audio/mp3")  
                        with col4:
                            feature_button_state = st.button('Track Audio Features', key= track['id'], on_click=feature_requested)

                            
                                            
                            
                           
                        with col4:
                            def similar_songs_requested():
                                track_id=track['id']
                                token=song_recommender.get_token(SPOTIFY_CLIENT_ID,SPOTIFY_SECRET_KEY)
                                similar_songs_json=song_recommender.get_track_recommendations(track_id,token)
                                recommendation_list=similar_songs_json['tracks']
                                recommendation_list_df=pd.DataFrame(recommendation_list)
                                recommendation_df=recommendation_list_df[['name','explicit','duration_ms','popularity']]
                                with st.sidebar:
                                    tab1, tab2= st.tabs(["Songs", "Visualization"])
                                    with tab1:
                                       st.dataframe(recommendation_df)
                                    with tab2:
                                        song_recommender.song_recommendation_vis(recommendation_df)
                            similar_songs_state = st.button('Similar Songs',key=track['name'],on_click=similar_songs_requested)

