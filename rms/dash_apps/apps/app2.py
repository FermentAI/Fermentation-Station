import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_apps.shared_components import *
from dash_apps.apps.myapp import app


content = html.Div(
    [
    html.H3('App 1'),
        dcc.Dropdown(
            id='app-1-dropdown',
            options=[
                {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                    'NYC', 'MTL', 'LA'
                ]
            ]
        ),
        html.Div(id='app-1-display-value'),
        dcc.Link('Go to App 1', href='/'),
    ],
    id="page-content",
    style = CONTENT_STYLE
)

layout = html.Div(
    [
        content,
    ],
)


@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)