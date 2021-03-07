import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_apps.shared_styles import *

# https://stackoverflow.com/questions/62732631/how-to-collapsed-sidebar-in-dash-plotly-dash-bootstrap-components
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="/app2"),
                dbc.DropdownMenuItem("Page 3", href="/app2"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Brand",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
    sticky='top'
)

sidebar = html.Div(
    [
        html.H2("Navigate", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Link("Test 1", href="/"),
                dcc.Link("Model 2", href='/app2'),
                dcc.Link("Check 3", href="/app2"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

sidebar_btn = dbc.Button(children = "<", outline=True, size = "sm", color="secondary", n_clicks =0, className="mr-1", id="btn_sidebar", style = SIDEBAR_BTN_STYLE)

def NamedSlider(name, **kwargs):
    other = kwargs.pop('other')
    return html.Div(
        children=[
            dbc.FormGroup(
            [
                dbc.Label(f"{name}\n ({other['units']})", width=8),
                dbc.Col(
                    dbc.Input(id=kwargs['id']+'-input', type="number", placeholder = kwargs['value']),
                    width=4,
                ),
            ],
            row=True,
        ),
        dcc.Slider(**kwargs),
        ],
    )


def generate_table(dataframe, max_rows=20):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

'''
from sympy import var, stats
from sympy import sympify
from sympy.utilities.lambdify import lambdify

t = var('t')
tv = np.arange(0,100)

text = st.text_input('Define Variable','u=f(t)')
# sanitize input
u = lambdify(t, sympify(text))
text = st.text_input('Add Disturbances','d=f(t)')
d = lambdify(t, sympify(text))

df = pd.DataFrame({
'time (hr)': tv,
selected_f: u(tv)+d(tv)
})

'''