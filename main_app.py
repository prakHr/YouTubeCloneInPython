import dash
from dash import Dash, dcc, callback, Output, State, Input, dash_table # pip install dash
# import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from dash import html
import plotly.express as px
import pandas as pd
import os
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
# Instructions dash-labs is the worst library ever, please uninstall it and then continue ...
app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.MORPH],pages_folder="pages")
   
    
# for page in dash.page_registry.values():
    # print(page)
    # print("*"*100)

graph = html.Div(
    html.Div([

        dash.page_container
    ],
    id="theme-changer-div",
    className="m-4")
)
theme_change = ThemeChangerAIO(aio_id="theme")
# layout2  = html.Div(children = [
            
#         dcc.Link(
#             dbc.Button('BACK'),
#             href='/',
#             refresh = False
#         ),
#         html.H5(id='output',children=[]),
#         dcc.Location(id='channel-url',refresh=False),
        
# ])
app.layout = dbc.Container([theme_change,graph],className = "m-4 dbc")

@app.callback(
    Output("theme-changer-div","id"),
    Input(ThemeChangerAIO.ids.radio("theme"),"value"),
)
def update_graph_theme(theme):
    template=template_from_url(theme)
    return template



# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/app1':
#         return app1.layout
#     elif pathname == '/apps/app2':
#         return app2.layout
#     else:
#         return '404'
# navbar = dbc.NavbarSimple(
#     dbc.Nav(
#         [
#             dbc.NavLink(page["name"], href=page["path"])
#             for page in dash.page_registry.values()
#             if page["module"] != "pages.not_found_404"
#         ],
#     ),
#     brand="Multi Page App Demo: Query Strings",
#     color="primary",
#     dark=True,
#     className="mb-2",
# )

# app.layout = dbc.Container(
#     [dash.page_container],
#     fluid=True,
# )

if __name__ == "__main__":

    # app.config['suppress_callback_exceptions'] = True
    # Dont do the above line to debug the errors in app efficiently using inbuilt-debugger
    app.run_server(debug=True)
