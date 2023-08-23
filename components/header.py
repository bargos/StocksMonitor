from dash import html
import dash_bootstrap_components as dbc

from components import modal

layout = dbc.Container([
    dbc.Row([
        modal.layout,
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([

                    ])
                ])
            ], className='card1_linha1')
        ], md=3, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Home", href='/home', className='textoSecundario')
                        ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Indicadores", href='/indicadores', className='textoSecundario')
                        ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Carteira", href='/wallet', className='textoSecundario')
                        ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Ativos", href='/ativos', className='textoSecundario')
                        ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Adicionar", href='', id='add_button', className='textoSecundario')
                        ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=4, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([html.Img(src='assets/logo_br2.png', height="80px"),

                                 ])
                    ])
                ])
            ], className='card1_linha1')
        ], md=1, xs=2),

    ], className='g-2 my-auto'),

], fluid=True)
