import dash
dash.register_page(__name__,path = '/ytChannels')

from dash import dcc, html, Input, State, Output, callback

import dash_bootstrap_components as dbc
import json
import requests
from config import api_key,api_host
from furl import furl
from pprint import pprint
# print(f"api_host = {api_host}")
from yt_components import *


layout  = html.Div(children = [
            
        dcc.Link(
            dbc.Button('BACK'),
            href='/',
            refresh = False
        ),
        html.H5(id='output',children=[]),
        dcc.Location(id='channel-url',refresh=False),
        html.Button('GO TO NEXT',id='submit-yt-val',n_clicks=0),
        html.Div(id="box-yt-container", children=[],style={"display":"none"}),
        html.Div(id="search-yt-component-container", children=[],style = {"display":"flex"}),
        html.Div(id="search-yt-details-component-container", children=[],style = {"margin":"20px 20px 20px 20px"}),
        html.Div(id="video-yt-comments-component-container", children=[],style = {"margin":"20px 20px 20px 20px"}),
        
])

# def layout(**other_unknown_query_strings):
#     print(other_unknown_query_strings)
#     return html.Div(
#         f"The user requested report ID: ."
#     )
# @callback(
#     dash.dependencies.Output('output', 'children'),
#     [dash.dependencies.Input('channel-url', 'href')])
# def update_output(value):
#     print('Request', value, flask.request.args)

#     return value

@callback(
    [
        Output("box-yt-container", "children"),
        Output("search-yt-component-container","children"),
        Output("search-yt-details-component-container","children"),
        Output("video-yt-comments-component-container","children"),
    ],
    [
        Input('channel-url','href'),
        Input("submit-yt-val",'n_clicks'),
        Input("box-yt-container","children"),
        Input("search-yt-component-container","children"),
        Input("search-yt-details-component-container","children"),
        Input("video-yt-comments-component-container","children")
    ]   
    # Output('output','children'),
    # [Input('channel-url','href')]
)
def _content(href,n_clicks,children,search_component_children,search_details_component_children,video_comments_component_children):
    f = furl(href)
    param1='default params'
    if 'param1' in f.args:
        param1 = f.args['param1']

    
    current_channel_id = param1
    url = f"https://{api_host}/search"
    search_component_children = []
    video_details_component_children = []
    video_comments_component_children = []
    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    # print(input_id)
    if n_clicks>0 and input_id=="submit-yt-val":
        try:
            if children==[]:
                querystring = {
                        "channelId":current_channel_id,
                        "part":"snippet,id",
                        "order":"date",
                        "maxResults":"50"
                }
            else:
                next_page_token = children[0]
                # print(f"next_page_token={next_page_token}")
                querystring = {
                    "channelId":current_channel_id,
                    "part":"snippet,id",
                    "order":"date",
                    "maxResults":"50",
                    "pageToken":next_page_token
                }

            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": api_host
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            search_dict = json.loads(response.text)
            pprint(search_dict)
            pageToken = search_dict["nextPageToken"]
            search_list = search_dict['items']

            children = [pageToken]
            video_ids = [video_id["id"]["videoId"]  for video_id in search_list]
            search_component_children = [
                youtube_component(video_id) for video_id in video_ids 
            ]
            video_details_component_children = [
                video_details_component(video_id) for video_id in video_ids
            ]
            video_comments_component_children = [
                video_comments_component(video_id) for video_id in video_ids
            ]
            return children,search_component_children,video_details_component_children,video_comments_component_children
        except Exception as e:
            print(e)
            return children,search_component_children,video_details_component_children,video_comments_component_children
    return children,search_component_children,video_details_component_children,video_comments_component_children