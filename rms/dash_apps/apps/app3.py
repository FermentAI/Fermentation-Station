import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_apps.shared_components import *
from dash_apps.apps.myapp import app



from engine import Model, Simulator
import os
import plotly.express as px


path = os.getcwd()
models = [os.path.join(path,'rms','models', o) for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))]
print(models,type(models[0]))

sim = Simulator(model = Model(models[0]))

lol = sim.model.mvars.default
mvars = [NamedSlider(
            name= lol.loc[var,'Label'],
            id="slider-"+var,
            min=0,
            max=500,
            step=100,
            value = lol.loc[var,'Value'],
            other = {'units':lol.loc[var,'Units']}
            )
     for var in lol.index]

run_btn = dbc.Button(children = "Run Simulation", outline=True, size = "lg", color="primary", className="mr-1", id="btn_run")
sim_plot = dcc.Graph(id = 'sim_plot')

#content = html.Div(
#    [
#        dbc.Row(dbc.Label("Alo, This is a row", width=2)),
#        dbc.Row([
#            dbc.Col(id = 'sliders', children = mvars, width = 2),
#            dbc.Col(sim_plot, width = 9)
#        ]),
#        dbc.Row(run_btn),
#        dbc.Row(id = 'mvars')
#    ],
#    id="page-content",
#    style = CONTENT_STYLE
#)

#app.layout = html.Div(
#    [
#        content,
#        html.Div(id='dummy-output')
#    ],
#)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Reactor Modeling Simulator',

                        ),
                        html.H4(
                            'Reaction Results',
                        )
                    ],

                    className='eight columns'
                ),
            html.A(
                html.Button(
                    "Learn More",
                    id = "learnMore"
                ),
                href="https://github.com/FermentAI/Reactor-Modeling-Sandbox",
                className="two columns"
            )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Filter by initial concentration:',
                            className="control_label"
                        ),
                        dcc.Input(id='C0',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by inlet feed concentration:',
                            className="control_label"
                        ),
                        dcc.Input(id='Cf',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by initial reactor temperature:',
                            className="control_label"
                        ),
                        dcc.Input(id='T0',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by initial cooling jacket temperature:',
                            className="control_label"
                        ),
                        dcc.Input(id='Tc0',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by coolant feed temperature:',
                            className="control_label"
                        ),
                        dcc.Input(id='Tcf',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by inlet feed temperature:',
                            className="control_label"
                        ),
                        dcc.Input(id='Tf',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by cooling jacket volume:',
                            className="control_label"
                        ),
                        dcc.Input(id='Vc',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by flow rate:',
                            className="control_label"
                        ),
                        dcc.Input(id='q',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by nominal coolant flow rate:',
                            className="control_label"
                        ),
                        dcc.Input(id='qc',
                            value='',
                            type='number'
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by types of models:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='model_selector',
                            options=[
                                {'label': 'Complex', 'value': 'complex'},
                                {'label': 'Simple', 'value': 'simple'}
                            ],
                            value='active',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("Final Concentration"),
                                        html.H6(
                                            id="models_text",
                                            className="info_text"
                                        )
                                    ],
                                    id = "Cx",
                                    className="pretty_container"
                                ),
                                
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("Final Temperature"),
                                                html.H6(
                                                    id="temp_text",
                                                    className="info_text"
                                                )
                                            ],
                                            id="Tx",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("Final Cooling Jacket Temperature")
                                                html.H6(
                                                    id="CJT_text",
                                                    className="info_text"
                                                )
                                            ],
                                            id="Tcx",
                                            className="pretty_container"
                                        ),
                                    ],
                                    id="tripleContainer",
                                )
                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="count_graph",
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol"
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Dive(
            [
                html.Div(
                    [
                        dcc.Graph(id='individual_graph')
                    ],
                    className="pretty_container four columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='aggregate_graph')
                    ],
                    className='pretty container five columns',
                ),
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

@app.callback(
    Output('dummy-output', 'children'),
    [Input('slider-'+var, 'value') for var in lol.index])

def update_mvars(*args):
    for var, new_value in zip(lol.index,args):
        sim.model.mvars.current.loc[var, 'Value'] = new_value
    return None

@app.callback(
    [
        Output('sim_plot', 'figure'),
        Output('mvars','children')
    ],
    Input('btn_run', 'n_clicks'))
def update_figure(n_clicks):
    data = sim.run()
    table = generate_table(sim.model.mvars.current)
    fig = px.scatter(data)
    sim.model.reset()
    return fig, table


# this callback uses the current pathname to set the active state of the
#corresponding nav link to true, allowing users to tell see page they are on
# @app.callback(
#     [Output(f"page-{i}-link", "active") for i in range(1, 4)],
#     [Input("url", "pathname")],
# )
# def toggle_active_links(pathname):
#     if pathname == "/":
#         # Treat page 1 as the homepage / index
#         return True, False, False
#     return [pathname == f"/page-{i}" for i in range(1, 4)]


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/", "/page-1"]:
#         return html.P("This is the content of page 1!")
#     elif pathname == "/page-2":
#         return html.P("This is the content of page 2. Yay!")
#     elif pathname == "/page-3":
#         return html.P("Oh cool, this is page 3!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#    )
