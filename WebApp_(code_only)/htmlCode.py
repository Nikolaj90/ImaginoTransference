#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Aug  4 13:39:17 2022

@author: bjorn
'''
# Libraries
from plotly import graph_objects as go
import plotly.express as px
import pandas as pd
import dash
from dash.dependencies import Input, Output
from random import choice, random
from dash import Dash, html, dcc
from plotly.subplots import make_subplots
from PIL import Image
import numpy as np


veganGreen = 'rgb(16,114,60)' # Light-green for the vegan color option !!! Change for real color
veggieGreen = 'rgb(140,190,84)' # Dark-green for the vegetarian color option !!! Change for real color
veggieGreenLight = "rgb(180, 240, 120)"


# Load Veggie Data

df_nameIndex = pd.read_csv("data/fv_data.csv",
                 dtype={"fips": str})

df_sim = pd.read_excel("data_sim.xlsx",
                 dtype={"fips": str})
#df = df.fillna(0) # replace NA values with 0
#df_nameIndex = df.set_index("Navn")
#df["Candidate"] = [df['Navn'][i]+f" ({df['Parti'][i][:2]})" for i, x in enumerate(df["Navn"])]
df_nameIndex = df_nameIndex.set_index("Navn")
# Tilføjer en randomiseret kostkolonne
#df_nameIndex["Kost"] = list(np.random.randint(low=1, high=6,size=len(df_nameIndex)))
#kost_dict = {5: "Kødspiser", 4:"Fleksitar",3:"Pescetar", 2: "Vegetar",1:"Veganer", 6: "Ønsker ikke at svare"}
#kost_color = {"Kødspiser":"red", "Fleksitar":"turquoise","Pescetar":"blue", "Vegetar":veggieGreen,"Veganer":veganGreen
#              ,"Ønsker ikke at svare" : "grey"}
#df_nameIndex["Kost"] = [kost_dict[x] for x in df_nameIndex["Kost"]]
#df_nameIndex["Kost_color"] = [kost_color[x] for x in df_nameIndex["Kost"]]



# List of the five new columns
#q1Answers = ['Daginstitutioner','Hospitaler, psykiatrien','Plejehjem, plejecentre og offentlig madudbringning til ældre', 'Offentlige arbejdspladser', 'ALLE offentlige institutioner']
#Adding the five columns, if not allready added
#if q1Answers[0] not in df.columns:
#    df = df.reindex(columns = df.columns[0:5].tolist() + q1Answers + df.columns[5:].tolist())

# First value adds random boolean(0,1) to "Alle offentlige institutioner" column.
# Second value adds random boolean (0,1) to the remaining four columns,
# depending on the boolean from the "Alle offentlige institutioner" column.
#q1Questions = df.columns[4:9]
#for i in range(0,len(df)):
#    value = 1 if random() > 0.7 else 0
#    df.loc[i,q1Questions[4:5]] = value
#    for col in q1Questions[0:4]:
#        value2 = 1 if random() > 0.5 else 0
#        if value == 0:
#            df.loc[i,col] = value2
#        else:
#            df.loc[i,col] = 0
# Definitions from the main-file

# This codeblock contains the variables for the dash-board
#Style
textBlack = 'rgb(0,0,0)' #Black for text

H2Style = {"fontSize": "50px",
            "color": veganGreen,
            "text-align": "center",
            'background': 'white',
            'font-family': 'Calibri',
            "margin-top": "20px",
            "margin-bottom":'10px',
            "padding":"1.5%"}

pStyle = {'fontSize': '40px',
            'color': textBlack,
            'text-align': 'center',
            'background': 'white',
            'font-family': 'Calibri',
            'margin-top': '-40px',
            'margin-bottom':'1px',
            'padding':'1.5%'}

#Lists
parties = [] # !!! Add list according to values from survey
candidates = [] # !!! Add list according to values from survey

questions = df_nameIndex.columns[4:26] # !!! Add questions to this list
questionLabels = ["  " + question for question in questions]
questionItems = []

for i in range(len(questions)):
    value = questions[i]
    label = questionLabels[i]
    item = {"label":  label,"value": value}
    questionItems.append(item)

kommuneList = df_nameIndex["Storkreds"].unique()  # !!! change list according to values from survey
kommuneList.sort()
logo_img = Image.open("dvf_logo.png")

# Placeholder text
#loremIpsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


# function with html code


def CodeHTML(textBlack, veganGreen, labelsKommuneList):  
    headline = 'Grønt Valg 2022'
    subheadline = '''Grønt Valg 2022 er Dansk Vegetarisk Forenings valgundersøgelse forud for folketingsvalget.
    Her kan du finde ud af, hvad dine kandidater fra din storkreds vil gøre for at fremme grønne måltider, fødevarer,
    omstillingen af landbruget og hvordan de vil finansiere den grønne omstilling. 
    Du kan klikke dig ind på specifikke spørgsmål eller kandidater og undersøge deres svar, imens du selv tager stilling. 
    God fornøjelse!'''

    component = html.Div([
        html.Div(
            children=[
                html.Img(
                    src = logo_img,
                    height = "90px"
                    ),
                html.P("OBS: Hvis du har åbnet siden fra mobilen, skal du formentlig zoome ud for at få det hele med.", 
                       style= {"margin-right": "90%",
                           "fontSize":"15px"}),
                html.H1(
                    children= headline,
                    className='header-title',
                    style={'color': veganGreen,
                           'background': 'white',
                           'text-align': 'center',
                           'font-family': 'Calibri',
                           'font-weight': '6200',
                           'margin-top': '-10px',
                           'fontSize': '60px'}
                ),
                html.P(
                    children= [subheadline],
                    className='header-description',
                    style=pStyle,
                ),
            ], className='header', style={'background': 'white'}
            ),
        html.H2(
            children= 'Vælg en storkreds',
            className="header-description",
            style=H2Style,
            ),
        html.P('Herunder kan du vælge din storkreds, så du kun får resultater fra kandidater, du kan stemme på i dit område.',
               style = pStyle),
        html.Div(
            children= [
                dcc.Dropdown(id='kommuneValg',
                             options= kommuneList,
                             value=kommuneList[3],
                             style={"fontSize":"30px",
                                    "margin-bottom": '50px',
                                    "margin-left": "10%",
                                    "margin-right": "20%"
                                    },
                             searchable = False
                             ),
                dcc.Graph(id="candidate_all",
                          config = dict(staticPlot = True)),
                #dcc.Graph(id="candidate_profile")
                ]),
        html.Br(),
        html.P("Hvert svar kan give 2, 1 eller 0 point og det samlede antal point udgør kandidatens veggiescore. At ville arbejde aktivt for en grøn mærkesag giver 2 point. At ville støtte en grøn mærkesag uden at arbejde aktivt for den giver 1 point. Ikke at ville støtte sagen, at svare ‘ved ikke’ eller slet ikke at svare giver 0 point.", 
               style = pStyle),
        html.Div(
            children =[
                html.H2(
                    children= 'Vælg et spørgsmål',
                    className="header-description",
                    style=H2Style
                    ),
                html.P('Herunder kan du vælge specifikke spørgsmål og se, hvad kandidaterne har svaret på disse.',
                       style=pStyle),
                html.Div([
                    dcc.RadioItems(questionItems,
                                  value = questions[0],
                                  labelStyle={'display': 'block'},
                                  style = {'fontSize': '40px',
                                            'color': textBlack,
                                            'text-align': 'left',
                                            'background': 'white',
                                            'font-family': 'Calibri',
                                            'margin-left': '7%',
                                            'margin-right': '7%',
                                            'margin-top': '1%'
                                            #'padding':'1.5%'
                                            },
                                  inputStyle = {'margin-top': '40px'},
                                  id = 'questions')
                    ], style ={}),
                ]),
        html.H2(style = H2Style,
                id="question_sunburt"),
        html.Div([
            dcc.Graph(id="sunburst"),
            html.H2('Sammenlign din storkreds med resten af Danmark',
                    className = 'Header-description',
                    style = H2Style
                ),
            dcc.Graph(id="piecharts"),
            html.Br(),
            html.P('Grønt Valg 2022 er en undersøgelse foretaget af Dansk Vegetarisk Forening. Hvis en kandidat ikke er med i undersøgelsen, er det fordi, kandidaten ikke har besvaret undersøgelsen. Du kan læse mere her:',
               style = pStyle),
            html.A(id = "vegetarisk.dk",href= "https://vegetarisk.dk/valg2022/", children = "Grønt Valg 2022", target = "_blank", style = {"marginLeft":"35%",
                                                                                                                                    "fontSize": "50px",
                                                                                                                                    "color": veganGreen}),
            html.P("Husk at stemme tirsdag den 1. november",
                   style = H2Style),
            html.P("GODT VALG!",
                   style = {"fontSize": "50px",
                               "color": veganGreen,
                               "text-align": "center",
                               'background': 'white',
                               'font-family': 'Calibri',
                               "margin-top": "5px",
                               "margin-bottom":'10px',
                               "padding":"1.5%"})
            ]),
        ],style={'background-color':'white','margin':'2%','display':'inline-block'})
    return component

app = dash.Dash(__name__)

# google analytics
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-9CDEQDK05M"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-9CDEQDK05M');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>        
    </body>
</html>"""

app.layout = CodeHTML(textBlack, veganGreen, kommuneList)

# dash code

"""
lollipop-graph municipality
The following callback takes the choice of municipality as input an creates a subsection of
the dataframe, this is then used to make a lollipop graph for the scores of the candidates
in that municipality
"""
@app.callback(
    Output("candidate_all", "figure"),
    Input("kommuneValg","value"))
def lollipop_all(value):
    

    
    kost_color = {'Spiser kun vegansk':veganGreen,
                  'Spiser kun vegetarisk, sjældent mælkeprodukter og æg': veggieGreen,
                  'Spiser kun vegetarisk, aldrig kød, kødpålæg, fjerkræ og fisk': veggieGreenLight,
                  "Spiser fisk, men derudover kun vegetarisk, aldrig kød, kødpålæg og fjerkræ":"turquoise",
                  "Spiser vegetarisk mindst halvdelen af ugens dage, de øvrige dage kød, fjerkræ og/eller fisk":"blue",
                  "Spiser ofte kød, kødpålæg, fjerkræ og/eller fisk (hver dag eller næsten hver dag)": "red",
                  'Ønsker ikke at svare': "grey",
                  'Ved ikke / har ikke taget stilling':"grey"
                  }
    
    fig = go.Figure()
    df_temp = df_nameIndex[df_nameIndex["Storkreds"]==value]
    df_temp = df_temp.sort_values(["Score", "Navn"], ascending = [True, False])    
    
    for j, mean in enumerate(df_temp["Score"]):
        candidate = df_temp.index[j]
        fig.add_trace(go.Scatter(y=[j,j],x=[0,mean],
                                 marker_size = [0,12],
                                 marker_color = df_temp["Kost_color"][j],
                                 line=go.scatter.Line(color=veggieGreen),
                                 hovertext=[df_temp.loc[candidate]["Parti"],df_temp.loc[candidate]["Parti"]],
                                 showlegend=False,
                                 hoverinfo=["none","x+y+text"],
    
                                 )
                      )
    
    for i, score in enumerate(df_temp["Score"]):
        fig.add_trace(go.Scatter(x=[0],y=[i],
                                 marker_size = [0],
                                 mode="lines+markers+text",
                                 text = [f"Score: {str(score)}"],
                                 textposition="top right",
                                 showlegend=False
                                ))
    fig.update_traces(textfont_size=16)
        
    
    # Adding a hidden scatterplot to add a legend with the dietary choices of the candidates
    for k, v in kost_color.items():
        fig.add_trace(go.Scatter(x=[0],y=[0],
                                 marker_size = [0],
                                 marker_color = v,
                                 name=k
                                ))
    
    tickvals_ = list(range(len(df_temp)))
    ticktext_ = list(df_temp.index)
    fig.update_layout(
        yaxis = dict(
            tickfont = dict(size = 16),
            tickmode = "array",
            tickvals = tickvals_,
            ticktext = ticktext_),
        title = {"text":f"Veggiescoren for kandidater i {value}",
                 "font": {"size": 30},
                 "xanchor": "left",
                 "x":0
                 })    
    
    
    
    fig.update_layout(legend= {'itemsizing': 'constant',
                               "orientation" : "h",
                               "yanchor" : "bottom",
                               "y":-0.135,
                               "xanchor" : "right",
                               "x" : 0.75
                               })
    
    
    fig.update_layout(
        height=1500)
        
    return fig

"""
Candidates from the kommune/storkreds
The following callback takes a municipality as input from a dropdown, and from this it creates an output of the
candidates for that municipality.
This output is sent as options for the Dropdown menu below(in the html code), where candidates for the lollipop-graph
are chosen.
"""
@app.callback(
    Output("Candidate_dropdown", 'options'),
    Input('kommuneValg', 'value'))
def save_data(value):
    return [{"label":x,"value":x} for x in df_nameIndex[df_nameIndex["Storkreds"]==value].index]


"""
Candidate profile
The graph shows the profile for a single ca"ndidate given their answers to the questions.

"""
"""
@app.callback(
    Output("candidate_profile", "figure"),
    [Input("candidate_all", "clickData"), Input("kommuneValg","value")]
    )
def CandidateProfile(clickData, value):
    # The dataframe from the candidate_all-graph is remade from the municipality
    df_temp = df_nameIndex[df_nameIndex["Kommune"]==value]   
    df_temp = df_temp.sort_values("Score", ascending = False)
    
    # From the x-position of the space that is clicked in candidate_all graph the 
    # candidate is then found in the index-value
    if clickData == None:
        candidate = df_temp.index[0]
    else: 
        candidate = df_temp.index[clickData["points"][0]["x"]]

    fig = go.Figure()
    
    # I make a dictonary, keys are questions and values are answers (0-2)
    candidate_dict = dict(df_nameIndex.loc[candidate][5:21])
    
    # Tickvalues are a list from 0 to x, x being the number of questions in the questionaire
    tickvals_ = list(range(len(candidate_dict.keys())))
    
    for i, answer in enumerate(candidate_dict.values()):
        fig.add_trace(go.Scatter(x= [i+1,i+1], y=[0, answer],
                                 showlegend=False,
                                 marker_size = [0,12],
                                 marker_color = veggieGreen,
                                 line_color = veggieGreen,
                                ))
    
    fig.update_layout(yaxis = dict(range=[-0.1,2.1],
                                   tickmode= "array",
                                  tickvals=[0,1,2],
                                  ticktext= ["Uenig", "Delvist Enig", "Enig"]),
                     xaxis = dict(range = [0,max(tickvals_)+2],
                                tickmode= "array",
                                tickvals= [x+1 for x in tickvals_],
                                ticktext = [x+1 for x in tickvals_],
                                title= "Spørgsmål"),
                     title= dict(text=candidate,
                                 y=0.9,
                                 x=0.5
                     ))    

    return fig
"""




@app.callback(
    Output("question_sunburt","children"),
    Input("questions","value"))
def QuestionHeadline(value):
    return value


# """
# Lollipop-graph candidates
# The following callback takes multiple dropdown inputs, where the user picks one or several candidates, that are then
# visualized in a lollipop-graph, that is created in the callback and sent back as output.
# """
# @app.callback(
#     Output("Lollipop_candidates", "figure"),
#     Input("Candidate_dropdown", "value")
#     )
# def update_lollipop(value):
#     valueList = list(value)
#     fig = go.Figure()
#     df_temp = df_nameIndex.loc[valueList]

#     df_temp = df_temp.sort_values("Score", ascending = False)


#     for i, mean in enumerate(df_temp["Score"]):
#         fig.add_trace(go.Scatter(x=[i,i],y=[0,mean],
#                                  marker={"color":veggieGreen,"size":markerSize},
#                                 line=go.scatter.Line(color=veggieGreen),
#                                 showlegend=False))

#     tickvals_ = list(range(len(df_temp)))
#     ticktext_ = list(df_temp.index)
#     fig.update_layout(
#         xaxis = dict(
#             tickmode = "array",
#             tickvals = tickvals_,
#             ticktext = ticktext_),
#         xaxis_range=[-1,len(df_temp)])
#     return fig


"""
Piecharts for question, kommune and denmark
The following graph is a subplot of two subplots. Both shows the distribution of
answers to the question, that is chosen earlier. One shows the distrubution for
the chosen kommune and the other for all of the country.
IMPORTANT: Doesn't work correctly at the moment
"""
@app.callback(
    Output("piecharts","figure"),
    [Input("kommuneValg", "value"),Input("questions", "value")]
    )
def update_piechart(storkreds, question):
    df_temp =  df_nameIndex[df_nameIndex["Storkreds"]==storkreds]
    df_temp = df_temp.sort_values(question)
    
    
    fig_pie = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    
    # labels for piechart - kommune
    value_labels = {'Uenig - det vil jeg ikke støtte':"Uenig", 
                    'Enig - det vil jeg støtte, men jeg vil ikke selv sætte det på dagsordenen':"Delvist Enig", 
                    "Enig - det vil jeg arbejde aktivt for":"Enig",
                   'Ved ikke / har ikke taget stilling': "Ved ikke / Ikke taget stilling"}
    
    answers_storkreds = pd.Series([value_labels[x] for x in df_temp[question]],
                                  index =df_temp.index)
    
    
    # Value for kommune
    value_storkreds = df_temp.groupby(question).size()
    
    labels_storkreds = [value_labels[x] for x in value_storkreds.index]
    
    # Colors kommune
    color_dict = { "Enig":'rgb(15,122,55)',
                  "Delvist Enig": 'rgb(169,220,163)',
                  "Uenig":'rgb(218,241,212)',
                  "Ved ikke / Ikke taget stilling": "grey"}
    
    colors = [color_dict[label] for label in labels_storkreds]
    
    
    
    fig_pie.add_trace(go.Pie(labels=labels_storkreds,
                                values=value_storkreds,
                                hole=0.6,
                                marker_colors = colors,
                                showlegend=False,
                             text=labels_storkreds
                                ),row = 1,col = 1)
    
    answers_all = pd.Series([value_labels[x] for x in df_nameIndex[question]],
                                  index =df_nameIndex.index)
    
    values = df_nameIndex.groupby(question).size()
    labels = [value_labels[x] for x in values.index]
    
    colors = [color_dict[label] for label in labels]
    
    
    fig_pie.add_trace(go.Pie(labels=labels,
                                values=values,
                                hole=0.6,
                                marker_colors = colors,
                             showlegend=False,
                             text = labels
                                ),row = 1,col = 2)
    
    
    fig_pie.add_trace(go.Sunburst(
        labels=[storkreds],
        parents=[""],
        values=[1],
        ), row = 1, col=1)
    
    
    fig_pie.add_trace(go.Sunburst(
        labels=["Alle Kandidater"],
        parents=[""],
        values=[1],
        ), row = 1, col=2)
    
    
    
    fig_pie.update_layout(
        autosize=False,
        width=1200,
        height=720)
    return fig_pie



"""
Sunburst, answers hierachial with candidates
The sunburst graph shows a sunburst graph with two layers, the inner layer is the
possible answers, and the outer is the candidates that has given the answer respectively
"""
@app.callback(
    Output("sunburst","figure"),
    [Input("kommuneValg", "value"),Input("questions", "value")]
    )
def update_sunburst(storkreds,question):
    df_temp =  df_nameIndex[df_nameIndex["Storkreds"]==storkreds]
    df_temp = df_temp.sort_values(question)

    # Parents for sunburst
    value_labels = {'Uenig - det vil jeg ikke støtte':"Uenig", 
                    'Enig - det vil jeg støtte, men jeg vil ikke selv sætte det på dagsordenen':"Delvist Enig", 
                    "Enig - det vil jeg arbejde aktivt for":"Enig",
                   'Ved ikke / har ikke taget stilling': "Ved ikke / Ikke taget stilling"}
    parents_candidates = pd.Series([value_labels[x] for x in df_temp[question]],
                                  index =df_temp.index)

    sunburst_parents = []
    for answer in parents_candidates.unique():
        sunburst_parents.append("")
    sunburst_parents.extend(parents_candidates)

    # Names for sunburst
    sunburst_names = []

    inner_names = list(parents_candidates.value_counts(sort=False).index)
    sunburst_names.extend(inner_names)

    candidate_names = list(df_temp.index)
    sunburst_names.extend(candidate_names)

    # Values for sunburst
    sunburst_values = []

    inner_values = list(parents_candidates.value_counts(sort=False))
    sunburst_values.extend(inner_values)

    candidate_values = []
    for candidate in list(df_temp.index):
        candidate_values.append(1)

    sunburst_values.extend(candidate_values)

    fig = go.Figure()

    color_dict = { "Enig":'rgb(15,122,55)',
                  "Delvist Enig": 'rgb(169,220,163)',
                  "Uenig":'rgb(218,241,212)',
                  "Ved ikke / Ikke taget stilling": "white"}
    colors_sunburst = {}
    for answer in parents_candidates.unique():
        colors_sunburst[answer] = color_dict[answer]

    data = dict(
        names=sunburst_names,
        parent=sunburst_parents,
        value=sunburst_values)

    fig.add_trace(go.Sunburst(
        labels=data['names'],
        parents=data['parent'],
        values=data['value'],
        branchvalues="total",
        marker_colors = list(colors_sunburst.values()),
        insidetextorientation='radial',
        ))
    fig.update_layout(
        autosize=False,
        width=1200,
        height=720)
    return fig

server = app.server
# for google analytics

if __name__ == '__main__':
    app.run_server()
