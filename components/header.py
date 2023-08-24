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
            ],  className='card1_linha1  align-items-center')
        ], md=3, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Home", href='/home', className='header_icon')
                        ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Indicadores", href='/indicadores', className='header_icon')
                        ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Carteira", href='/wallet', className='header_icon')
                        ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Ativos", href='/ativos', className='header_icon')
                        ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Adicionar", href='', id='add_button', className='header_icon')
                        ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=1, xs=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([html.Img(src='assets/logo_br2.png', height="80px"),

                                 ])
                    ])
                ])
            ],  className='card1_linha1  align-items-center')
        ], md=4, xs=2),

    ], className='g-2 my-auto align-items-center'),

], fluid=True)
