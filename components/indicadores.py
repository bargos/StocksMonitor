from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from menu_styles import *
from functions import *
from functionsm import *
from app import *

from tvdatafeed_lib.main import TvDatafeed, Interval

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line_graph_indicadores', config={"displayModeBar": False, "showTips": False}, className='graph_line')    
            ], xs=12, md=12,)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.RadioItems(
                        options=[{'label': x, 'value': x} for x in PERIOD_OPTIONSML],
                        value='1y',
                        id="period_input_indicadores",
                        inline=True,
                        className='textoTerciario',
                    ),
                ], sm=5, md=5),
            ]),
        ], xs=12, md=12),     
    ],  className='g-2 my-auto'),
    
    dbc.Row([
        dbc.Col([
            html.Legend('ML Indicators', className='textoSecundario'),
        ], xs=12, md=12),
    ],  className='g-2 my-auto'),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(id='dropdown_card_indicadores', value=[], multi=False, options=[]),
                                    ]),
                                ])
                            ])
                        ],className='cards_linha2')
                    ],md=2),
                dbc.Col([
                    
                    ],md=10, id='cards_ativos_ml'),
            ],  className='g-2 my-auto')
        ], xs=12, md=12),
    ],  className='g-2 my-auto'),
], fluid=True)



# callback para atulizar o dropdown
@app.callback(
    Output('cards_ativos_ml', 'children'),
    Input('dropdown_card_indicadores', 'value'),
)

def update_cards_ativos_ml(dropdown):        
        
    ativo = 'PETR3'

    models_list = ['ml_rf_Interval.in_1_minute_ac_61.18',
    'ml_rf_Interval.in_5_minute_ac_57.22',
    'ml_rf_Interval.in_15_minute_ac_55.45',
    'ml_rf_Interval.in_30_minute_ac_56.79',
    'ml_rf_Interval.in_45_minute_ac_55.39',
    'ml_rf_Interval.in_1_hour_ac_55.33',
    'ml_rf_Interval.in_2_hour_ac_55.15',
    'ml_rf_Interval.in_daily_ac_55.45',
    'ml_rf_Interval.in_weekly_ac_60.30',
    'ml_rf_Interval.in_monthly_ac_72.94']

# DEU ERRO
#'ml_rf_Interval.in_3_minute_ac_59.17',
#'ml_rf_Interval.in_3_hour_ac_54.78',
        
    models_feat = PERIOD_OPTIONSML

    seta_crescendo = ["fa fa-arrow-up", 'textoQuartenarioVerde',]
    seta_caindo = ['fa fa-arrow-down', 'textoQuartenarioVermelho']

    lista_valores_ativos = []
    for ind in range(len(models_list)):
        if pred_ac(models_list[ind], ativo) < 0:
            lista_valores_ativos.append([models_feat[ind], seta_caindo[0], seta_caindo[1]])
        else:
            lista_valores_ativos.append([models_feat[ind], seta_crescendo[0], seta_crescendo[1]])

    lista_colunas = []
    for n, ativo in enumerate(lista_valores_ativos):
        if  n < 12:
            col = dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(ativo[0], className='textoTerciario'),
                                        
                                    ]),
                                    dbc.Col([
                                        html.H1([html.I(className=ativo[1])], className=ativo[2])
                                    ])
                                ])
                            ])
                        ],className='cards_linha2'), 
                    ], md=1, xs=10)
            
            lista_colunas.append(col)

    card_ativos= dbc.Row([
                    *lista_colunas
                ])
    
    return card_ativos


# callback para atulizar o dropdown
@app.callback(
    Output('dropdown_card_indicadores', 'value'),
    Output('dropdown_card_indicadores', 'options'),
    Input('historical_data_store', 'data'),
)
def update_dropdown(book):
    df = pd.DataFrame(book)
    #unique = df['ativo'].unique()
    unique = df['symbol'].unique()
    
    try:
       dropdown = [unique[0], [{'label': x, 'value': x} for x in unique]]
    except:
        dropdown = ['', [{'label': x, 'value': x} for x in unique]]
    
    return dropdown


# callback line graph
@app.callback(
    Output('line_graph_indicadores', 'figure'),
    Input('dropdown_card_indicadores', 'value'),
    Input('period_input_indicadores', 'value'),
    State('historical_data_store', 'data'),
)
def line_graph_indicadores(dropdown, period, historical_info):
    #if dropdown == None:
    #    return no_update
    #if type(dropdown) != list: dropdown = [dropdown]
    #dropdown = ['IBOV'] + dropdown

    #df_hist = pd.DataFrame(historical_info)
    #df_hist['datetime'] = pd.to_datetime(df_hist['datetime'], format='%Y-%m-%d %H:%M:%S')
    #df_hist = slice_df_timedeltas(df_hist, '3mo')



    tv = TvDatafeed()

    ativos_org_var = {}
    ativos_org_var['PETR3']  = 'BMFBOVESPA'

    for symb_dict in ativos_org_var.items():
        data = tv.get_hist(*symb_dict, n_bars = 90,
                        interval = Interval.in_daily).reset_index()

    data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low',
                'close': 'Close', 'volume': 'Volume'}, errors="raise", inplace=True)


    #### altera os indices do dataframe para as datas de cada linha
    data = data.set_index('datetime')
    
    #print(data)

    
    #fig = go.Figure()

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    
    #df_hist = df_hist[df_hist['symbol'].str.contains('|'.join(dropdown))]
    #for n, ticker in enumerate(dropdown):
    #    df_aux = df_hist[df_hist.symbol.str.contains(ticker)]
    #    df_aux.dropna(inplace=True)
    #    df_aux.close = df_aux.close / df_aux.close.iloc[0] - 1
    #    print(df_aux)
    #    fig.add_trace(go.Scatter(x=df_aux.datetime, y=df_aux.close*100, mode='lines', name=ticker, line=dict(color=LISTA_DE_CORES_LINHAS[n])))
 
    fig.update_layout(MAIN_CONFIG_2, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hoverlabel=HOVER_LINE_GRAPH)
    fig.update_xaxes(tickfont=dict(family='Nexa', size=AXIS_FONT_SIZE, color=AXIS_VALUES_COLOR), gridcolor=LINHAS_DE_GRADE)
    fig.update_yaxes(tickfont=dict(family='Nexa', size=AXIS_FONT_SIZE, color=AXIS_VALUES_COLOR), gridcolor=LINHAS_DE_GRADE, zerolinecolor=LINHA_ZERO_X)
    
    return fig