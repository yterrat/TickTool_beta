#!/usr/bin/env python3
# Import packages

import dash
from dash import dcc, html, Input, Output, callback, State

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Img(src='/assets/TickTOOL_logo.png', style={'width': '40%', 'height': '40%'}, className='image-gallery'),
    html.Hr(className='orange_line'),
    html.Br(),
    html.Div([
    html.B('Evaluate your prevention strategy', style={'font-size': '60px'})
        ], style={'text-align': 'center'}),
    html.Br(),
    html.Br(),
    html.P("Would you like to better understand your risk of being bitten by a tick or learn how to improve your \
           tick bite prevention strategy for yourself and your family? Fill the questionnaire below! \
               A personalised report will be created for you at the end.", 
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
    html.Br(),
    html.P("With your consent, the information you provide in this questionnaire may be used for research projects. \
           These projects will be under the responsibility of a principal investigator at the Université de Montréal \
           and will be authorized by a research ethics committee. \
           You will not be asked to provide your name or contact information. \
           The researcher undertakes to maintain and protect the confidentiality of the data concerning you, \
           under the conditions set out in this form. If you do not wish your responses to be used for research purposes, \
            you may still complete the questionnaire.",
            style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
    html.Br(),
    html.P("Consent for secondary use of data:",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px','text-decoration': 'underline'}),
    html.Br(),
    html.P("I consent to the researcher using, or authorizing students under their direction to use, \
           de-identified data for future research projects, conditional on their ethical \
               approval and in compliance with the same principles of confidentiality and protection of information.",
           style={"display":"flex", "gap":"1px", "align-items":"flex-end", 'font-size' : '20px'}),
    html.Br(),
    html.B("Do you consent to sharing your responses with the Université de Montréal?", style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.RadioItems(
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ],
                id = 'consent',
                #value='',
                inputStyle={"margin-right": "10px"},
                labelStyle={'display': 'inline-block', 'margin-right': '15px'}
            )
        ]),
    html.Br(),
    dcc.Link('Next page', href='/page-2', style={'font-size': '20px'}),
    html.Br(),
    html.Br(),
    html.Img(src='/assets/UdeM.png', style={'width': '20%', 'height': '20%'}, className='image-gallery'),
    html.Br(),
    html.Br(),
    # html.Div(id='display-answers_p1', style={'marginTop': '50px', 'whiteSpace': 'pre-wrap'})
])



@callback(
    Output('record_answers', 'data',  allow_duplicate=True),
    Input('consent', 'value'),
    State('record_answers', 'data'),
    prevent_initial_call=True,
)

def update_dic_page1(Q1, data):
    data = data or {}
    if Q1 is not None:
        data['consent'] = Q1
    return data

@callback(
    [Output('consent', 'value')],
    Input('url', 'pathname'),
    State('record_answers', 'data')
)

def initialize_inputs_page1(pathname, data):
    if not data:
        return [None, None]
    return [data.get('consent', None)]





####
#Affichage
###
# @callback(
#     Output('display-answers_p1', 'children'),
#     Input('record_answers', 'data')
# )

# def display_answers(data):
#     if data:
#         return html.Pre(json.dumps(data, indent=2))
#     return "No data recorded yet."

