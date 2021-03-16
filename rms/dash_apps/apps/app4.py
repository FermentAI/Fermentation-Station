import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import rms.dash_apps
import rms.dash_apps.shared_components as dsc
from rms.dash_apps.shared_styles import *
from rms.dash_apps.apps.myapp import app
import dash

import rms.engine
from rms.engine import Model, Simulator
import os
import plotly.express as px


path = os.getcwd()
# get all models in the models directory, skip penicilin
model_names = [o for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))]
model_names.remove('penicillin_goldrick_2017')
model_path = lambda model_name: os.path.join(path,'rms','models', model_name) 

# make a Dropdown Menu to select a models
dropdown_models = lambda pick: [dbc.DropdownMenuItem(m, id = m, active = True) if i is pick else dbc.DropdownMenuItem(m, id = m,  active = False) for i,m in enumerate(model_names)]

def sim(model_name):
    """
    Generates simulator object based on model name

    Arguments
    ---------
        model_name
    """
    global mysim, mymvars, mycvars, mymparams, mysparams
    mysim = Simulator(model = Model(model_path(model_name)))
    mymvars = mysim.model.mvars.default
    try:
        mycvars = mysim.subroutine.subroutine_vars.default
    except:
        mycvars = None

    mymparams = mysim.model.params.default
    mysparams = mysim.simvars.default
    return 

def sliders_from_df(vars_df):
    """
    Generates sliders based on the variables in a DataFrame

    Arguments
    ---------
        vars_df: Pandas DataFrame containing variables
    """
    if vars_df is None: return
    sliders = []
    for var in vars_df.index:
        if vars_df.loc[var,'Min'] is not False:
            minval = vars_df.loc[var,'Min']
        else:
            minval = vars_df.loc[var,'Value']*0.1

        if vars_df.loc[var,'Max'] is not False:
            maxval = vars_df.loc[var,'Max']
        else:
            maxval = vars_df.loc[var,'Value']*1.9

        slider = dsc.NamedSlider(
                    name= vars_df.loc[var,'Label'],
                    id="slider-"+var,
                    min=minval,
                    max=maxval,
                    step=(maxval-minval)/100,
                    value = vars_df.loc[var,'Value'],
                    other = {'units':vars_df.loc[var,'Units']}
                )
        sliders.append(slider)
    return sliders

# default to the first model 
sim(model_names[0])

# make a diagram, if any

diagram = lambda simulator: dbc.Card(
    [
        dbc.CardImg(src=simulator.model.diagram, top=True, alt = 'Oh snap!. No diagram for this model!'),
        dbc.CardBody(
            html.P(simulator.model.doc, className="card-text")
        ),
    ],
)

# make a button to run the simulator
run_btn = dbc.Button(children = "Run Simulation", outline=True, size = "lg", color="primary", className="mr-1", id="btn_run")

# make a button for plots
plot_btn = dbc.Button(children = "Add Chart", outline=True, size = "lg", color="primary", className="mr-1", id="btn_plot")

# make a plot for output 
sim_plot = dcc.Graph(id = 'sim_plot4')

# layout all the components to be displayed
content = html.Div(
    [
        dbc.Row([
            dbc.Col(width = 9),
            dbc.Col(
                dbc.DropdownMenu(
                    label = "Select a model",
                    children = dropdown_models(0),
                    right=False,
                    id = 'dd_models'
                ),
            )
        ]),

        dbc.Row([
            dbc.Col([
                *dsc.collapse(sliders_from_df(mymvars), 'Manipulated Variables', 'mvars-collapse'),
                *dsc.collapse(sliders_from_df(mycvars), 'Control Variables', 'cvars-collapse'),
                # *dsc.collapse(inputs_from_df(mymparams), 'Model Parameters', 'mpars-collapse'),
                # *dsc.collapse(inputs_from_df(mysparams), 'Simulation Settings', 'spars-collapse')
            ],
                id = 'sliders2', width = 2),
            dbc.Col(diagram(mysim), width = 6),
            dbc.Col(diagram(mysim), width = 4)
        ]),

        dbc.Row(run_btn),

        dbc.Row([
            dbc.Col(sim_plot, width = 9),
            dbc.Col(id = 'mvars4')
        ]),
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

print(os.path.join(mysim.model.path,'diagram.png'))

# callback to update the simulator with the selected model
@app.callback(
    [Output("dd_models", "children")],
    [Output(s+"-collapse", "children") for s in ['mvars','cvars']],#,'mparams','sparams']],
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
        
    sim(model_names[new_pick])
    return dropdown_models(new_pick), sliders_from_df(mymvars),sliders_from_df(mycvars)


# callback to update the model variables with the sliders / input boxes
@app.callback(
    [Output('slider-'+var+'-input', 'value') for var in mymvars.index],
    [Output('slider-'+var, 'value') for var in mymvars.index],
    [Input('slider-'+var+'-input', 'value') for var in mymvars.index],
    [Input('slider-'+var, 'value') for var in mymvars.index])

def update_mvars_slider(*args):
    sliders = list(args[int(len(args)/2):])
    inputs = list(args[:int(len(args)/2)])

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if len(button_id) > 3:
        for i,var in enumerate(mymvars.index):
            if 'input' in button_id:
                sliders[i] = inputs[i]
            else:
                inputs[i] = sliders[i]
            mysim.model.mvars.current.loc[var, 'Value'] = sliders[i]

    return (*inputs, *sliders)

# callback to run the simulator and display data when the button is clicked
@app.callback(
    [
        Output('sim_plot4', 'figure'),
        Output('mvars4','children')
    ],
    Input('btn_run', 'n_clicks'))
def update_figure(n_clicks):
    data = mysim.run()
    table = dsc.generate_table(mysim.model.mvars.current)
    fig = px.scatter(data)
    mysim.model.reset()
    return fig, table

@app.callback(
    [Output(s+"-collapse", "is_open") for s in ['mvars','cvars']],#,'mparams','sparams']],
    [Input(s+"-collapse-button", "n_clicks") for s in ['mvars','cvars']],#,'mparams','sparams']],
    [State(s+"-collapse", "is_open") for s in ['mvars','cvars']],#,'mparams','sparams']],
)
def toggle_collapse(*args):
    are_open = list(args[int(len(args)/2):])
    ns = list(args[:int(len(args)/2)])
    print(args)

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # this dsnt work
    for i,n in enumerate(ns):
        if n:
            are_open[i] = not are_open[i]

    return are_open

