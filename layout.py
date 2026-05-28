from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container([

        html.H2(
            "Simulations de dés",
            style={
                "color": "white",
                "margin": "0px"
            }
        ),

        html.Div([

            html.Span(
                "Version française",
                style={
                    "fontWeight": "bold",
                    "marginRight": "15px",
                    "fontSize": "14px",
                    "color": "white"
                }
            ),

            html.Img(
                src="/assets/Flag_of_France.svg.png",
                style={
                    "width": "32px",
                    "height": "22px",
                    "borderRadius": "4px",
                    "marginLeft": "10px",
                    "boxShadow": "0px 1px 4px rgba(0,0,0,0.2)"
                }
            )

        ],
        style={
            "display": "flex",
            "alignItems": "center"
        })

    ],
    fluid=True),

    color="primary",
    dark=True
)



tabs = dbc.Tabs(

    [

        dbc.Tab(

            [

                html.H2("Double un"),

                html.H3(
"Dans cette section, vous pouvez simuler des lancers de dés, analyser les fréquences des résultats et explorer des visualisations basées sur les probabilités."
                ),

                dbc.Row([

                    dbc.Col(

                        [

                            html.Label(
                                "Sélectionnez le nombre de dés à utiliser."
                            ),

                            dcc.Dropdown(
                                id="Dropdown_var_1",
                                options=[
                                    {"label": i, "value": i}
                                    for i in [1, 2, 3, 4, 5]
                                ],
                                value=1
                            )

                        ],

                        width=6

                    ),

                    dbc.Col(

                        [

                            html.Label(
                                "Sélectionnez un nombre pour voir sa fréquence."
                            ),

                            dcc.Dropdown(
                                id="Dropdown_var_2",
                                options=[],
                                value=None
                            )

                        ],

                        width=6

                    )

                ]),

                dbc.Row([

                    dbc.Col(

                        [

                            html.Label(
                                "Combien de simulations voulez-vous lancer ?"
                            ),

                            dcc.Slider(
                                id="n_sim",
                                min=100,
                                max=10000,
                                step=10,
                                value=5000
                            )

                        ],

                        width=6

                    )

                ],
                    justify="center"),
                dbc.Row([

                    dbc.Col([

                    dbc.Button(
                        "Lancer la simulation",
                                id="run_sim",
                                color="danger",
                                className="mt-3"
                    )
                    ],
                        width=12
                    )
                ]),
                dbc.Row([
                    dbc.Col(
                        html.Div(
                            id="selected_number_text"
                        ),
                        width=6
                    )
                ],
                    justify="center"),
                dbc.Row([
                    dbc.Col(
                        [
                            html.H4("Table de fréquences"),
                            dbc.Button(
                                "Télécharger le CSV des fréquences",
                                id="download_freq_btn",
                                color="secondary",
                                disabled=True,
                                className="mb-2"
                            ),
                            dcc.Download(id="download_freq_csv"),
                            dash_table.DataTable(
                                id="freq_table"
                            )
                        ],
                        width=4
                    ),
                    dbc.Col(
                        [
                            html.H4("Tableau récapitulatif"),
                            dbc.Button(
                                "Télécharger le résumé CSV",
                                id="download_summary_btn",
                                color="secondary",
                                disabled=True,
                                className="mb-2"
                            ),
                            dcc.Download(id="download_summary_csv"),
                            dash_table.DataTable(
                                id="summary_table")
                        ],
                        width=4
                    )
                ],
                    justify="center"),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id="hist_plot"
                        ),
                        width=8
                    )],
                    justify="center"
                )
            ],

            label="Double un"

        ),

        dbc.Tab(

            [

                html.H2("Lancer une pièce"),

                html.H3(
                    "Cette section vous permet de simuler des lancers de pièce, d’évaluer les distributions des résultats et d’examiner des visualisations probabilistes."
                ),

dbc.Row([
    dbc.Col(
        [
            html.Label("Combien de faces voulez-vous obtenir ?"),
            dcc.Dropdown(
                id="Dropdown_coin_2",
                options=[
                    {"label": str(i), "value": i}
                    for i in range(1, 11)
                ],
                value=1,
                clearable=False
            )
        ],
        width=6
    ),

    dbc.Col(
        [
            html.Label("Combien de simulations voulez-vous lancer ?"),
            dcc.Slider(
                id="n_sim_2",
                min=100,
                max=1000,
                step=10,
                value=500,
                marks={
                    i: str(i)
                    for i in range(100, 1001, 100)
                }
            )
        ],
        width=6
    )
]),

dbc.Row([

    dbc.Col(

        [

            html.Button(
                "Lancer la simulation",

                id="run_sim_coin",

                n_clicks=0,

                style={
                    "backgroundColor": "#B22222",
                    "color": "white",
                    "border": "none",
                    "padding": "10px 18px",
                    "borderRadius": "8px",
                    "fontWeight": "bold",
                    "marginTop": "20px",
                    "boxShadow": "0px 2px 5px rgba(0,0,0,0.25)"
                }
            )

        ],

        width=3

    )

]),

dbc.Row([

    dbc.Col(

        [

            html.H4("Table de fréquences"),

            dash_table.DataTable(
                id="freq_table_coins"
            )

        ],

        width=4

    ),

    dbc.Col(

        [

            html.H4("Tableau récapitulatif"),

            dash_table.DataTable(
                id="summary_table_coins"
            )

        ],

        width=4

    )

],

justify="center"

),

dbc.Row([

    dbc.Col(

        [

            dcc.Graph(
                id="hist_plot_coins"
            )

        ],

        width=8

    )

],

justify="center"

)

            ],

            label="Lancer une pièce"

        )

    ]

)

layout = html.Div([

    navbar,

    dbc.Row([



        dbc.Col(

            tabs,

            width=10
        )

    ])

])




