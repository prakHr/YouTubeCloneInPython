import dash
from dash import dcc, html, Input, State, Output, callback

import dash_bootstrap_components as dbc
import json
import requests
from config import api_key,api_host
from furl import furl
from pprint import pprint
def youtube_comments_component(comment):
    rv=dbc.Row(html.Div([
                    
                    html.Div(comment,style = {"margin":"20px 20px 20px 20px"}),
                        
                ],
                style = {"margin":"5px","padding":"20px"},
                className="h-10 p-5 text-white bg-dark rounded-1",
            ),
    )
    return rv
def youtube_title_component(channel_id,title,description,published_at):
    rv=dbc.Col(html.Div([
                    dcc.Link(
                        dbc.Button(
                            'Go to channel',
                            n_clicks = 0,
                            className="btn btn-secondary"
                        ),
                        
                        href = f'/ytChannels?param1={channel_id}',
                        refresh = True
                    ),
                    html.Div(published_at,style = {"margin":"20px 20px 20px 20px"}),
                    html.Div(title,style = {"margin":"20px 20px 20px 20px"}),
                    html.Div(description,style = {"margin":"20px 20px 20px 20px"})
                        
                ],
                style = {"margin":"60px","padding":"20px"},
                className="h-10 p-5 text-white bg-dark rounded-1",
            ),
            md=6,
    )
    return rv
def video_details_component(video_id):
        
    url = f"https://{api_host}/videos"
    querystring = {
                "part":"contentDetails,snippet,statistics",
                "id":video_id
    }
    headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    search_dict = json.loads(response.text)
    search_list = search_dict['items']
    snippet_details = [item['snippet'] for item in search_list]
    channel_ids = [item['channelId'] for item in snippet_details]

    title = [item['title'] for item in snippet_details]
    description = [item['description'] for item in snippet_details]
    published_at = [item['publishedAt'] for item in snippet_details]
    search_component_children = dbc.Row(
        [youtube_title_component(video_id,title,description,published_at) for video_id in channel_ids ],
        className="align-items-md-stretch",
    )
    # pprint(f"search_component_children={search_component_children}")
    return search_component_children

def youtube_component(video_id):
    children=[
                        # dash_player.DashPlayer(
                        #     id=f"{video_id}",
                        #     url=f"https://youtu.be/{video_id}",
                        #     controls=False,
                        #     width="30%",
                        #     height="250px",
                        # ),
                        html.Iframe(width="30%", 
                            height="250", 
                            src=f"https://www.youtube-nocookie.com/embed/{video_id}", 
                            title="YouTube video player", 
                            allow="accelerometer, autoplay, clipboard-write, encrypted-media, gyroscope, picture-in-picture "
                        )
                        
                ]
    return children[0]

def video_comments_component(video_id):
    url = f"https://{api_host}/commentThreads"

    querystring = {"part":"snippet","videoId":video_id,"maxResults":"100"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    search_dict = json.loads(response.text)
    search_list = search_dict['items']
    toplevel_comments = [item['snippet']['topLevelComment']['snippet']['textOriginal'] for item in search_list]
    rv = dbc.Col(
            [youtube_comments_component(comment) for comment in toplevel_comments],
            # className="align-items-md-stretch",
    )
    # pprint(f"search_component_children={search_component_children}")
    return rv

