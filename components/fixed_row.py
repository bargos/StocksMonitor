from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date

from menu_styles import *
from functions import *
from app import *

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Legend('Principais destaques', className='textoSecundario'),
        ], xs=12, md=12),
    ],  className='g-2 my-auto'),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([

                ],md=12, id='cards_ativos'),
            ],  className='g-2 my-auto')
        ], xs=12, md=12),
    ],  className='g-2 my-auto'),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    
                ],md=12, id='cards_ativos2'),
            ],  className='g-2 my-auto')
        ], xs=12, md=12),
    ],  className='g-2 my-auto'),    

], fluid=True)



#callback para atualizar os cards
@app.callback(
    Output('cards_ativos', 'children'),
    Output('cards_ativos2', 'children'),
    State('historical_data_store', 'data'),
    Input('period_input', 'value'),
    Input('dropdown_card1', 'value'),
    Input('book_data_store', 'data'),
)

def update_cards_ativos(historical_data, period, dropdown, book_data):

    if dropdown == None:
        return no_update
    if type(dropdown) != list: dropdown = [dropdown]
    dropdown = ['IBOV'] + dropdown
    
    df_hist = pd.DataFrame(historical_data)
    
    ativos_existentes = iterar_sobre_df_ibov2(df_ibov)
       
    if period == 'ytd':
        correct_timedelta = date.today().replace(month=1, day=1)
        correct_timedelta = pd.Timestamp(correct_timedelta)
    else:
        correct_timedelta = date.today() - TIMEDELTAS[period]

    dict_valores = {}

    for key, value in ativos_existentes.items():
        df_auxiliar = (df_hist[df_hist.symbol.str.contains(key)])
        df_auxiliar['datetime'] = pd.to_datetime(df_auxiliar['datetime'], format='%Y-%m-%d %H:%M:%S')
        df_periodo = df_auxiliar[df_auxiliar['datetime'] > correct_timedelta]
        # import pdb; pdb.set_trace()
        valor_atual = df_periodo['close'].iloc[-1]
        diferenca_periodo= valor_atual/df_periodo['close'].iloc[0]
        dict_valores[key] = valor_atual, diferenca_periodo
        dfativos= pd.DataFrame(dict_valores).T.rename_axis('ticker').add_prefix('Value').reset_index()
        dfativos['Value1']= dfativos['Value1']*100 - 100
    
    dfativos.sort_values(by=['Value1'], ascending=False, inplace=True)

    seta_crescendo = ['fa fa-angle-up', 'textoQuartenarioVerde',]
    seta_caindo = ['fa fa-angle-down', 'textoQuartenarioVermelho']

    lista_valores_ativos = []
    lista_tags = []
    for ativo in range(len(dfativos)):
        tag_ativo = dfativos.iloc[ativo][0]
        lista_tags.append(tag_ativo)
        valor_ativo = dfativos.iloc[ativo][1]
        variacao_ativo = dfativos.iloc[ativo][2]
        if variacao_ativo < 0:
            lista_valores_ativos.append([tag_ativo, valor_ativo, variacao_ativo, seta_caindo[0], seta_caindo[1]])
        else: 
            lista_valores_ativos.append([tag_ativo, valor_ativo, variacao_ativo, seta_crescendo[0], seta_crescendo[1]])

    #Graficos
    df_hist = pd.DataFrame(historical_data)
    df_hist['datetime'] = pd.to_datetime(df_hist['datetime'], format='%Y-%m-%d %H:%M:%S')
    df_hist = slice_df_timedeltas(df_hist, period)

    df_hist = df_hist[df_hist['symbol'].str.contains('|'.join(lista_tags))]

    lista_graficos = []
    #for n, ticker in enumerate(lista_tags):
    #    if  n < 6:
    #        fig = go.Figure()
    #        df_aux = df_hist[df_hist.symbol.str.contains(ticker)]
    #        df_aux.dropna(inplace=True)
    #        df_aux.close = df_aux.close / df_aux.close.iloc[0] - 1

    #        fig.add_trace(go.Scatter(x=df_aux.datetime, y=df_aux.close*100, mode='lines', name=ticker,line=dict(color=CARD_GRAPHS_LINE_COLOR), hoverinfo = "skip"))

    #        fig.update_layout(MAIN_CONFIG_3, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    #        fig.update_xaxes(visible=False)
    #        fig.update_yaxes(visible=False)
            
    #        lista_graficos.append(fig)

    lista_colunas = []
    for n, ativo in enumerate(lista_valores_ativos):
        if  n < 6:
            col = dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(ativo[0], className='textoQuartenario'),
                                        
                                    ], md=4),
                                    dbc.Col([
                                        #dcc.Graph(figure=lista_graficos[n], config={"displayModeBar": False, "showTips": False}, className='graph_cards'),
                                    ], md=8)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.H5(["R$",'{:,.2f}'.format(ativo[1]), " "], className='textoTerciario'),
                                        html.H5([html.I(className=ativo[3]), " ", '{:,.2f}'.format(ativo[2]), "%"], className=ativo[4])
                                    ])
                                ])
                            ])
                        ],className='cards_linha2'), 
                    ], md=2, xs=12)
            
            lista_colunas.append(col)

    card_ativos= dbc.Row([
                    *lista_colunas
                ])
    
    lista_colunas2 = []
    for n, ativo in reversed(list(enumerate(lista_valores_ativos))):
        if  n > (len(lista_valores_ativos) - 7):
            col = dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(ativo[0], className='textoQuartenario'),
                                        
                                    ], md=4),
                                    dbc.Col([
                                        #dcc.Graph(figure=lista_graficos[n], config={"displayModeBar": False, "showTips": False}, className='graph_cards'),
                                    ], md=8)
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.H5(["R$",'{:,.2f}'.format(ativo[1]), " "], className='textoTerciario'),
                                        html.H5([html.I(className=ativo[3]), " ", '{:,.2f}'.format(ativo[2]), "%"], className=ativo[4])
                                    ])
                                ])
                            ])
                        ],className='cards_linha2'), 
                    ], md=2, xs=12)
            
            lista_colunas2.append(col)

    card_ativos2= dbc.Row([
                    *lista_colunas2
                ])
    
    return card_ativos, card_ativos2

