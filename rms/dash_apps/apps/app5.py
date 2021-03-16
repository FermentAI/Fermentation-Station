import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_apps.shared_components as dsc
from dash_apps.shared_styles import *
from dash_apps.apps.myapp import app
import dash
from engine import Model, Simulator
import os
import plotly.express as px
import pandas as pd

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
    global mysim, mymvars, mycvars, mymparams, mysparams, data
    mysim = Simulator(model = Model(model_path(model_name)))
    mymvars = mysim.model.mvars.default
    try:
        mycvars = mysim.subroutines.subrvars.default
    except Exception as e:
        print(e)
        mycvars = None

    mymparams = mysim.model.params.default
    mysparams = mysim.simvars.default

    mysim.set_inputs()
    data = mysim.run()
    mymvars = mysim.model.reset()
    return 

def sliders_from_df(vars_df):
    """
    Generates sliders based on the variables in a DataFrame

    Arguments
    ---------
        vars_df: Pandas DataFrame containing variables
    """ 
    sliders = []
    if vars_df is not None:
        for i,var in enumerate(vars_df.index):
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
                        id={'type':'dynamic-var',
                            'index': var
                        },
                        min=minval,
                        max=maxval,
                        step=(maxval-minval)/100,
                        value = vars_df.loc[var,'Value'],
                        other = {'units':vars_df.loc[var,'Units']}
                    )
            sliders.append(slider)
    return sliders

# make a diagram, if any
diagram = lambda simulator: dbc.Card(
    [
        dbc.CardImg(src=simulator.model.diagram, top=True, alt = 'Oh snap! No diagram for this model!'),
        dbc.CardBody(
            html.P(simulator.model.doc, className="card-text")
        ),
    ],
)

# make a button to run the simulator
run_btn = dbc.Button(children = "Run Simulation", outline=True, size = "lg", color="primary", className="mr-1", id="btn_run", n_clicks = 0)

# make a button for plots
plot_btn = dbc.Button(children = "Add Chart", outline=True, size = "lg", color="primary", className="mr-1", id="btn_plot", n_clicks = 0)

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
                dbc.Row(dsc.collapse([], 'Manipulated Variables', 'mvars-collapse')),
                dbc.Row(dsc.collapse([], 'Control Variables', 'cvars-collapse')),
                # *dsc.collapse(inputs_from_df(mymparams), 'Model Parameters', 'mpars-collapse'),
                # *dsc.collapse(inputs_from_df(mysparams), 'Simulation Settings', 'spars-collapse')
            ],
                id = 'sliders2', width = 2),
            dbc.Col([],id = 'diagram1', width = 6),
            dbc.Col([],id = 'diagram2', width = 4)
        ]),

        dbc.Row(run_btn),
        dbc.Row(plot_btn),
        dbc.Row([
            dbc.Col(id = 'container', children = [], width = 9),
            dbc.Col(id = 'mvars4')
        ]),
    ],
    id="page-content",
    style = CONTENT_STYLE
)

#Layout includes a button simulate, a button to add charts, and an empty list to add graphs.
layout = html.Div(
    [
        content,
        html.Div(id='dummy-output4'),
        html.Div(id='dummy-output-models')
    ],
)

# callback to update the simulator with the selected model
@app.callback(
    [Output("dd_models", "children")],
    [Output(s+"-collapse", "children") for s in ['mvars','cvars']],#,'mparams','sparams']],,
    [Output('dummy-output-models','children')],
    [Output('diagram1','children')],
    [Input(m, "n_clicks") for m in model_names],
)

def update_simulator(*args):
    ctx = dash.callback_context
    # this gets the id of the button that triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    try:
        new_pick = model_names.index(button_id)
    except:
        new_pick = 0

    sim(model_names[new_pick])

    return dropdown_models(new_pick), sliders_from_df(mymvars[~mymvars.State]), sliders_from_df(mycvars), [], diagram(mysim)



# callback to update the model variables with the sliders / input box
@app.callback(
    [Output({'type': 'dynamic-var-input', 'index': ALL}, 'value'),
    Output({'type': 'dynamic-var', 'index': ALL}, 'value')],
    [Input({'type': 'dynamic-var-input', 'index': ALL}, 'value'),
    Input({'type': 'dynamic-var', 'index': ALL}, 'value')]
)
def update_mvars_slider(inputs,sliders):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id:
        if 'input' in button_id:
            sliders = inputs
        else:
            inputs = sliders

        idx = len(mysim.model.mvars.from_input['Value']) # cheap but works
        mysim.model.mvars.from_input['Value'].iloc[:] = sliders[:idx]
        mysim.subroutines.subrvars.from_input['Value'].iloc[:] = sliders[idx:]

    return inputs, sliders

# callback to run the simulator and display data when the button is clicked
@app.callback(
    Output('dummy-output4','children'),
    Input('btn_run', 'n_clicks'),
)
def run_simulation(n_clicks_run):
    if n_clicks_run>0:
        global data, mymvars
        mysim.set_inputs()
        data = mysim.run()
        mymvars = mysim.model.reset()
        print('1')
        print(mymvars)
    return
   
# Takes the n-clicks of the add-chart button and the state of the container children.
@app.callback(
   Output('container','children'),
   [Input('btn_plot','n_clicks'),
   Input('dummy-output4','children'),
   Input('dummy-output-models','children')],
   [State('btn_run','n_clicks'),
   State('container','children')]
)
#This function is triggered when the add-chart clicks changes. This function is not triggered by changes in the state of the container. If children changes, state saves the change in the callback.
def display_graphs(n_clicks, dummy,dummy_models, n_run, div_children):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(data.columns[data.columns.map(lambda x: '0' not in x)])
    print('data')
    print(mymvars)
    if button_id == 'dummy-output-models':
        div_children = []

    elif button_id == 'btn_plot' or (n_clicks == 0 and n_run == 0):
        new_child = dbc.Col(
            children=[
                dbc.Row([
                dbc.Col(dbc.RadioItems(
                    id={'type':'dynamic-choice',
                        'index':n_clicks
                    },
                    options=[{'label': 'Line Chart', 'value': 'line'},
                            {'label':'Bar Chart', 'value': 'bar'}
                            ],
                    value='line',
                ), width = 2),
                dbc.Col(dcc.Dropdown(
                    id={
                        'type': 'dynamic-dpn-var1',
                        'index': n_clicks
                    },
                    options=[{'label': pd.concat([mymvars,mycvars]).loc[var,'Label'] + ' ('+var+')', 'value': var} for var in data.columns[data.columns.map(lambda x: '0' not in x)]],
                    multi=True,
                    value = [],
                    placeholder='Select variables to plot...',
                    clearable=False
                ), width = 8),
                dbc.Col([
                    dbc.Label('Time'),
                    dcc.Slider(
                    id={'type':'dynamic-slider',
                        'index':n_clicks
                    },
                    min=1,
                    max=len(mysim.time)-1,
                    step=1,
                    value=len(mysim.time)-1,
                )], width = 2),
                ]),
                dcc.Graph(
                    id={
                        'type':'dynamic-graph',
                        'index':n_clicks
                    },
                    figure={}
                ),
            ]
        )
        div_children.append(new_child)

    elif button_id == 'dummy-output4':
        for c,child in enumerate(div_children):
            try:
                for l,line in enumerate(child['props']['children'][1]['props']['figure']['data']):
                    old_data = div_children[c]['props']['children'][1]['props']['figure']['data'][l]['y']
                    var = div_children[c]['props']['children'][1]['props']['figure']['data'][l]['legendgroup']
                    div_children[c]['props']['children'][1]['props']['figure']['data'][l]['y'] = data[var].iloc[:len(old_data)].tolist()
            except:
                pass

    return div_children

# callback to update the graphs with the selected variables and graph types
@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id={'type': 'dynamic-dpn-var1', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-choice', 'index': MATCH}, component_property='value'),
     Input(component_id={'type': 'dynamic-slider', 'index': MATCH}, component_property='value')],
     State({'type': 'dynamic-graph', 'index': MATCH}, 'figure')
)
def new_graph(var, chart_type, time_idx, old_fig):
    ctx = dash.callback_context

    if ctx.triggered[0]["prop_id"] != '.':

        if len(var) == 0:
            fig = old_fig
        else:
            if chart_type == 'bar':
                fig = px.bar(x = var, y= data[var].iloc[time_idx], color=var, labels = {'y':'Value at {:.2f}'.format(data.index[time_idx]), 'x':'Variable', 'color':'Variable'})
            elif chart_type == 'line':
                fig = px.line(data.iloc[:time_idx] , x = data.iloc[:time_idx].index, y = var, labels = {'x':'Time','value':'Value', 'variable':'Variable'})
                            
            # change labels
            labels = {v:mymvars.loc[v,'Label'] + ' (' + mymvars.loc[v,'Units'] +')' for v in var}
            for i, dat in enumerate(fig.data):
                for elem in dat:
                    if elem == 'name':
                        fig.data[i].name = labels[fig.data[i].name]

        return fig

    else:
        return old_fig

# callback to collapse the different slider menus
@app.callback(
    [Output(s+"-collapse", "is_open") for s in ['mvars','cvars']],#,'mparams','sparams']],
    [Input(s+"-collapse-button", "n_clicks") for s in ['mvars','cvars']],#,'mparams','sparams']],
    [State(s+"-collapse", "is_open") for s in ['mvars','cvars']],#,'mparams','sparams']],
)
def toggle_collapse(*args):
    are_open = list(args[int(len(args)/2):])
    ns = list(args[:int(len(args)/2)])

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
 
    for i,n in enumerate(['mvars','cvars']):
        if n in button_id:
            are_open[i] = not are_open[i]

    return are_open