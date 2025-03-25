#!/usr/bin/env python3

# Import packages
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/page-5')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    ######
    ######
   html.Div([
       html.B('Prior tick exposure', style={'font-size': '60px'})
       ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.B("In the last year, how frequently did you find ticks in the following contexts?", className='question_style2'),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Label('Attached to your skin', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Daily', 'value': 'Daily'},
                    {'label': "Weekly", 'value': "Weekly"},
                    {'label': "Monthly", 'value': "Monthly"},
                    {'label': "Less than once a month", 'value': "Less than once a month"},
                    {'label': "Once or twice a season", 'value': "Once or twicw a season"},
                    {'label': "Never", 'value': "Never"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'attached_to_your_skin'
            ),
            html.Br(),
            html.Label('Freely moving on your skin or clothing', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Daily', 'value': 'Daily'},
                    {'label': "Weekly", 'value': "Weekly"},
                    {'label': "Monthly", 'value': "Monthly"},
                    {'label': "Less than once a month", 'value': "Less than once a month"},
                    {'label': "Once or twicw a season", 'value': "Once or twicw a season"},
                    {'label': "Never", 'value': "Never"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'Freely_moving'
            ),
            html.Br(),
            html.Label('On a pet', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Daily', 'value': 'Daily'},
                    {'label': "Weekly", 'value': "Weekly"},
                    {'label': "Monthly", 'value': "Monthly"},
                    {'label': "Less than once a month", 'value': "Less than once a month"},
                    {'label': "Once or twicw a season", 'value': "Once or twicw a season"},
                    {'label': "Never", 'value': "Never"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'On_a_pet'
            ),
            html.Br(),
            html.Label('Freely moving outside in the environment', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': 'Daily', 'value': 'Daily'},
                    {'label': "Weekly", 'value': "Weekly"},
                    {'label': "Monthly", 'value': "Monthly"},
                    {'label': "Less than once a month", 'value': "Less than once a month"},
                    {'label': "Once or twicw a season", 'value': "Once or twicw a season"},
                    {'label': "Never", 'value': "Never"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'Freely_moving_outside'
            ),
        ], style={'font-size': '15px', 'marginLeft' : '30px'})
    ]),
    html.Br(),
    ######
    ######
    html.Hr(className='grey_blue_line'),
    html.B('Approximately how many ticks did you find in the following contexts last year, \
           between the months of April and November?', className='question_style2'),
    html.Br(),
    html.Br(),
    html.Div([
            html.Label('Embedded in your skin', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': "I don't remember", 'value': "I don't remember"},
                    {'label': "0", 'value': "0"},
                    {'label': "1-5", 'value': "1-5"},
                    {'label': "6-25", 'value': "6-25"},
                    {'label': "> 25", 'value': "> 25"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'How_many_embedded_in_your_skin'
            ),
            html.Br(),
            html.Label('Freely moving on your skin or cloth', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': "I don't remember", 'value': "I don't remmber"},
                    {'label': "0", 'value': "0"},
                    {'label': "1-5", 'value': "1-5"},
                    {'label': "6-25", 'value': "6-25"},
                    {'label': "> 25", 'value': "> 25"},
                    {'label': "Not applicable", 'value': "Not applicable"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'How_many_freely_moving_on_your_skin'
            ),
            html.Br(),
            html.Label('On a pet', style={'font-size' : '20px'}),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                options=[
                    {'label': "I don't remember", 'value': "I don't remmber"},
                    {'label': "0", 'value': "0"},
                    {'label': "1-5", 'value': "1-5"},
                    {'label': "6-25", 'value': "6-25"},
                    {'label': "> 25", 'value': "> 25"},
                    {'label': "Not applicable", 'value': "Not applicable"},
                    {'label': "I don’t remember", 'value': "I don’t remember"}
                ],
                style={'width': '200px'},
                #value='',
                id = 'How_many_on_a_pet'
            ),
            html.Br(),
    ], style={'font-size': '15px', 'marginLeft' : '30px', 'marginRight' : '30px'}),
    html.Br(),
    dcc.Link('Next page', href='/page-6', style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    dbc.Progress(value=63, style={"height": "15px"}, className="mb-3", label = "63% done"),
])


@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('attached_to_your_skin', 'value'),
    Input('Freely_moving', 'value'),
    Input('On_a_pet', 'value'),
    Input('Freely_moving_outside', 'value'),
    Input('How_many_embedded_in_your_skin', 'value'),
    Input('How_many_freely_moving_on_your_skin', 'value'),
    Input('How_many_on_a_pet', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_p5(Q1,Q2,Q3,Q4,Q5,Q6,Q7,data):
    data = data or {}
    if Q1 is not None :
        data['attached_to_your_skin'] = Q1
    if Q2 is not None :
        data['Freely_moving'] = Q2
    if Q3 is not None :
        data['On_a_pet'] = Q3
    if Q4 is not None :
        data['Freely_moving_outside'] = Q4
    if Q5 is not None :
        data['How_many_embedded_in_your_skin'] = Q5
    if Q6 is not None :
        data['How_many_freely_moving_on_your_skin'] = Q6
    if Q7 is not None :
        data['How_many_on_a_pet'] = Q7
    return data

# @callback(
#     [Output('attached_to_your_skin', 'value'),
#      Output('Freely_moving', 'value'),
#      Output('On_a_pet', 'value'),
#      Output('Freely_moving_outside', 'value'),
#      Output('How_many_embedded_in_your_skin', 'value'),
#      Output('How_many_freely_moving_on_your_skin', 'value'),
#      Output('How_many_on_a_pet', 'value')
#     ],
#     Input('url', 'pathname'),
#     State('record_answers', 'data')
# )
  
# def initialize_inputs_page5(pathname, data):
#     if not data:
#         return [None, None]
#     return [
#      data.get('attached_to_your_skin', None),
#      data.get('Freely_moving', None),
#      data.get('On_a_pet', None),
#      data.get('Freely_moving_outside', None),
#      data.get('How_many_embedded_in_your_skin', None),
#      data.get('How_many_freely_moving_on_your_skin', None),
#      data.get('How_many_on_a_pet', None)
#      ]
         
