import dash
from dash import Dash, dcc, html, Input, State, Output, callback
# import dash_player
import dash_bootstrap_components as dbc
import json
import requests
from furl import furl
from config import api_key,api_host
from pprint import pprint
# print(f"api_host = {api_host}")
from yt_components import *
dash.register_page(__name__,path = '/')

layout = html.Div(children = [
        dcc.Input(
            id="search-term", 
            type="text", 
            placeholder="", 
            style={'marginRight':'10px'}
        ),    
        html.Button('SEARCH WITH NEXT',id='submit-val',n_clicks=0),
        html.Div(id="box-container", children=[],style={"display":"none"}),
        html.Div(id="search-component-container", children=[],style = {"display":"flex"}),
        html.Div(id="search-details-component-container", children=[],style = {"margin":"20px 20px 20px 20px"}),
        html.Div(id="video-comments-component-container", children=[],style = {"margin":"20px 20px 20px 20px"}),
        dcc.Location(id='url',refresh=False),
        html.Div(id='content')
])


'''
def youtube_title_component(channel_id,title,description,published_at):
    rv=dbc.Col(html.Div([
                    dcc.Link(
                        dbc.Button(
                            'Go to channel',
                            n_clicks = 0,
                            className="btn btn-secondary"
                        ),
                        
                        href = f'/ytb?param1={channel_id}',
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
    rv = dbc.Row(
            [youtube_comments_component(comment) for comment in toplevel_comments],
            className="align-items-md-stretch",
    )
    # pprint(f"search_component_children={search_component_children}")
    return rv
'''
@callback(
    [
        Output("box-container", "children"),
        Output("search-component-container","children"),
        Output("search-details-component-container","children"),
        Output("video-comments-component-container","children"),
    ],
    [
        Input("submit-val",'n_clicks'),
        Input("search-term", "value"),
        Input("box-container","children"),
        Input("search-component-container","children"),
        Input("search-details-component-container","children"),
        Input("video-comments-component-container","children")
    ]   
)
def populate_search_component(n_clicks,search_term,children,search_component_children,search_details_component_children,video_comments_component_children):
    
    search_component_children = []
    search_details_component_children = []
    video_comments_component_children = []
    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    # print(input_id)
    if n_clicks>0 and input_id=="submit-val":
        try:
            

            url = f"https://{api_host}/search"
            # print(f"search-term={search_term}")
            if children!=[]:
                prev_search_term = children[1]
                if prev_search_term != search_term:
                    children = []
            if children == []:
                querystring = {
                    "q":search_term,
                    "part":"snippet,id",
                    "order":"date",
                    # "regionCode":"US"
                    
                }

            else:
                pageToken = children[0]
                # print(f"next token = {pageToken}")
                querystring = {
                    "q":search_term,
                    "part":"snippet,id",
                    "order":"date",
                    # "regionCode":"US"
                    "pageToken":pageToken
                }

            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": api_host
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            # print(response.text)
            # pprint(response.text)
            search_dict = json.loads(response.text)
            # pprint(search_dict.keys())
            # pprint(search_dict)
            pageToken = search_dict["nextPageToken"]
            search_list = search_dict['items']
            # pprint(search_list)
            
            # print(len(search_list))

            children = [pageToken,search_term]
            video_ids = [video_id["id"]["videoId"]  for video_id in search_list]
            search_component_children = [
                youtube_component(video_id) for video_id in video_ids 
            ]
            # print("reached here")
            video_details_component_children = [
                video_details_component(video_id) for video_id in video_ids
            ]
            video_comments_component_children = [
                video_comments_component(video_id) for video_id in video_ids
            ]
            # print("reached till here")
            return children,search_component_children,video_details_component_children,video_comments_component_children
        except Exception as e:
            print(e)

            return children,search_component_children,search_details_component_children,video_comments_component_children
    return children,search_component_children,search_details_component_children,video_comments_component_children


@callback(Output('content','children'),
    [Input('url','href')])
def _content(href:str):
    f = furl(href)
    param1=''
    if param1 in f.args:
        param1=f.args['param1']
    return html.H1(children='')