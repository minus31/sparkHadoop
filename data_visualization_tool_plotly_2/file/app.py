import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import datetime


app = dash.Dash()
server = app.server

# Load Kaggle Data
df = pd.read_csv('data/bikesharing.csv')
df = df.reset_index(drop=False)

# season preprocessing
df_season = df.groupby(['season']).sum()

# date preprocessing
df['dayofweek'] = df['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday())
df_dayofweek = df.groupby(['dayofweek']).sum()

# groupby date
df['datetime2'] = df['datetime'].apply(lambda x: str(x)[:10])
df_daily = df.groupby(['datetime2']).sum().reset_index(drop=False)[['datetime2', 'count']]







app.title = 'Meetup-F10F11'


app.layout = html.Div(
    html.Div([
        # 우측 상단에 버튼 만들기
        html.Div(
            html.A([
                html.Img(
                    src = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Kaggle_logo.png',
                    style = {
                        'width' : '8%', # 너비 기준으로 조절하는 것을 추천
                        'float' : 'right', # 위치
                        'position' : 'relative', # 다른 요소의 위치 따라 상대적으로 배치
                        'padding-top' : 1, #윗 경계면으로부터 간격
                        'padding-right' : 15, #우측 경계면으로부터 간격
                    },
                )
            ], href='https://www.kaggle.com/c/bike-sharing-demand') #링크
        ),

        # Title
        html.Div(
            html.H1('Kaggle Bike Sharing Demand Visualization')
        ),


        # 드랍다운 기능 삽입
        html.Div(
            dcc.Dropdown(
                options=[
                    {'label' : 'Basic Plot', 'value':1},
                    {'label' : 'By Timeframes', 'value':2},
                    {'label' : 'Heatmap', 'value':3},
                    {'label' : 'Table', 'value':4},
                ],
                id = 'dropdown',
                placeholder = '시각화 타입을 선택하세요'
                # value=3, #로드 시 가장 먼저 보여주고 싶은 특정 탭이 있다면 해당 번호 고정,

            ),
            style = {
                'width' : '40%'
            }
        ),

        # 각 드랍다운에 해당하는 시각화를 보여주기 위한 공간 할당
        html.Div(
            html.Div(
                id = 'dropdown-output'
            )
        )
    ]
    )
)

# 콜백함수의 Input, Output 명시
@app.callback(
    Output('dropdown-output', 'children'),
    [Input('dropdown', 'value')],
)


def display_content(value):
    
    if value == 1:

        df['datetime'] = pd.to_datetime(df['datetime'])
        data_basic = [
            go.Scatter(
                x=df['datetime'],
                y=df['count'],
                line = dict(color = '#7F7F7F'),
                opacity = 0.8,
            )
        ]

        return html.Div([
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            dcc.Graph(
                id='lineplot',
                figure={
                    'title' : 'Time-Series',
                    'data' : data_basic,
                    'layout' : {
                        'title': 'Time-Series',
                        'xaxis': {
                            'rangeselector': {
                                'buttons' : [
                                    {'count':1,
                                     'label':'1 month',
                                     'step':'month',
                                     'stepmode':'backward'},
                                    {'count':6,
                                     'label':'6 month',
                                     'step':'month',
                                     'stepmode':'backward',},
                                    {'step':'all'}
                                ]
                            },
                            'rangeslider':{
                                'visible':True,
                            },
                            'type':'date'
                        },
                    },
                    'margin' : {
                        'l': 100, #left
                        'r': 100, #right
                        'b': 50,  #bottom
                        't': 100  #top
                    },
                },
                style={
                    'height': '80vh',
                    'width' : '150vh'
                }
            ),

        ])


    
    
    elif value == 2:
        
        data_season = [
            go.Bar(
                y=['spring', 'summer', 'autumn', 'winter'],
                x=list(df_season['count']),
                orientation='h',
                marker=dict(
                    color='rgb(255, 150, 0)' 
                )
            )
        ]

        data_dayofweek = [
            go.Bar(
                y=['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
                x=list(df_dayofweek['count']),
                orientation='h',
                marker=dict(
                    color=[
                        'rgb(100, 117, 166)',
                        'rgb(100, 117, 166)',
                        'rgb(100, 117, 166)',
                        'rgb(100, 117, 166)',
                        'rgb(100, 117, 166)',
                        'rgb(241, 117, 107)',
                        'rgb(241, 117, 107)',
                    ]
                )
            )
        ]

        data_daily = [
            go.Bar(
                y=df_daily['count'],
                x=df_daily['datetime2'],
                orientation='v',
                marker=dict(
                    color='rgb(94, 201, 135)'
                )
            )
        ]

        # Markdown 텍스트 넣어주기 : 줄 넣기 
        return html.Div([
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            html.Div(children=[
                html.Div(
                    dcc.Graph(
                        id='bar-plot1',
                        figure={
                            'title' : 'Seasonal Count',
                            'data' : data_season,
                            'layout' : {
                                'title' : 'Season',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 100,
                                },
                            } 
                        },
                        style={
                            'height': '40vh',
                            'width' : '60vh',
                        }
                    ),
                    style={
                        'display' : 'inline-block'
                    },
                ),

                html.Div(
                    dcc.Graph(
                        id='bar-plot2',
                        figure={
                            'title' : 'Day of Week Count',
                            'data' : data_dayofweek,
                            'layout' : {
                                'title' : 'Day of Week',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 100,
                                },
                            },
                        },
                        style={
                            'height': '40vh',
                            'width' : '60vh',
                        }
                    ),
                    style={
                        'display' : 'inline-block'
                    },
                ),

                html.Div(
                    dcc.Graph(
                        id='bar-plot3',
                        figure={
                            'data' : data_daily,
                            'layout' : {
                                'title' : 'Daily Count',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 50
                                },
                            }
                        },
                        style={
                            'height': '60vh',
                            'width' : '120vh'
                        }
                    ),
                ),
            ])
        ])
            


    elif value == 3:
        corrMatx = df[["temp","atemp","casual","registered","humidity","windspeed","count"]].corr()

        data_heatmap = [go.Heatmap(
            z=corrMatx.values,
            x=corrMatx.columns,
            y=corrMatx.columns,
            colorscale='Viridis'  # 히트맵 컬러스케일 ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu','Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet','Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis']
            )]

        return html.Div([
            # Markdown 텍스트 넣어주기 : 줄 넣기 
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            dcc.Graph(
                id='heatmap',
                figure={
                    'title' : 'Correlation Heatmap',
                    'data' : data_heatmap,
                    'layout' : {
                        'title': 'Heatmap',
                    'margin': {
                        'l': 100, #left
                        'r': 100, #right
                        'b': 50,  #bottom
                        't': 100  #top
                        },
                    }
                },
                style={
                    'height': '80vh',
                    'width' : '80vh'
                    }
            ),

        ])


    # Table 보기 호출
    elif value == 4:
        
        return html.Div([
            
            
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            html.Div( children=[
                html.Div(
                    dash_table.DataTable(
                        id='table',
                        data=df.to_dict('rows'),
                        columns=[{'name':i, 'id':i} for i in df.columns],
                        # n_fixed_rows=1, # Header 고정
                        style_cell={
                            'textAlign': 'left',
                            'minWidth': '50px', 'maxWidth': '180px',
                            },
                        style_cell_conditional=[
                            {
                                'if':{'column_id':'index'},
                                'textAlign' : 'right'
                            }
                        ],
                        style_table={
                            'overflowX':'scroll', # X축 스크롤
                            'maxHeight':'600', # Height 고정
                            },
                    )
                )
            ])
        ])












if __name__ == '__main__':
    app.run_server(debug=True)