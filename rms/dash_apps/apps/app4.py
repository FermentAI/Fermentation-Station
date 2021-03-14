import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_apps.shared_components import *
from dash_apps.apps.myapp import app
import dash


from engine import Model, Simulator
import os
import plotly.express as px


path = os.getcwd()
model_names = [o for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))][:-1]
model_path = lambda model_name: os.path.join(path,'rms','models', model_name) 

sim = lambda model_name: Simulator(model = Model(model_path(model_name)))
mvars = lambda vars_df: [NamedSlider(
                        name= vars_df.loc[var,'Label'],
                        id="slider-"+var,
                        min=0,
                        max=500,
                        step=100,
                        value = vars_df.loc[var,'Value'],
                        other = {'units':vars_df.loc[var,'Units']}
                        )
                        for var in vars_df.index]

mysim = sim(model_names[0])
myvars = mysim.model.mvars.default

dropdown_models = lambda pick: [dbc.DropdownMenuItem(m, id = m, active = True) if i is pick else dbc.DropdownMenuItem(m, id = m,  active = False) for i,m in enumerate(model_names)]
run_btn = dbc.Button(children = "Run Simulation", outline=True, size = "lg", color="primary", className="mr-1", id="btn_run")
sim_plot = dcc.Graph(id = 'sim_plot4')


content = html.Div(
    [
        dbc.Row([
            dbc.Col(
                dbc.DropdownMenu(
                    label = "Select a model",
                    children = dropdown_models(0),
                    right=False,
                    id = 'dd_models'
                ),
            )
        ]),
        dbc.Row(dbc.Label("Alo, This is a row", width=2)),
        dbc.Row([
            dbc.Col(id = 'sliders', children = mvars(myvars), width = 2),
            dbc.Col(sim_plot, width = 9)
        ]),
        dbc.Row(run_btn),
        dbc.Row(id = 'mvars4')
    ],
    id="page-content",
    style = CONTENT_STYLE
)

layout = html.Div(
    [
        content,
        html.Div(id='dummy-output4')
    ],
)

@app.callback(
    [Output("dd_models", "children"),
    Output("sliders", "children")],
    [Input(m, "n_clicks") for m in model_names],
)
def update_label(*args):
    ctx = dash.callback_context
    # this gets the id of the button that triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    try:
        new_pick = model_names.index(button_id)
    except:
        new_pick = 0
        
    global mysim, myvars
    mysim = mysim = sim(model_names[new_pick])
    myvars = mysim.model.mvars.default
    return dropdown_models(new_pick), mvars(myvars)

@app.callback(
    Output('dummy-output4', 'children'),
    [Input('slider-'+var, 'value') for var in myvars.index])

def update_mvars(*args):
    for var, new_value in zip(myvars.index,args):
        mysim.model.mvars.current.loc[var, 'Value'] = new_value
    return None

@app.callback(
    [
        Output('sim_plot4', 'figure'),
        Output('mvars4','children')
    ],
    Input('btn_run', 'n_clicks'))
def update_figure(n_clicks):
    data = mysim.run()
    table = generate_table(mysim.model.mvars.current)
    fig = px.scatter(data)
    mysim.model.reset()
    return fig, table

