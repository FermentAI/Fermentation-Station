from engine import Model, Simulator, ModelDefinitionError
from dash_apps.apps.myapp import app
import os

def test_load_each_model():
    path = os.getcwd()
    # get all models in the models directory, skip penicilin
    model_names = [o for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))]
    model_names.remove('penicillin_goldrick_2017')
    model_path = lambda model_name: os.path.join(path,'rms','models', model_name)

    for m in model_names:
        try:
            Model(model_path(m)).get_model()
            ok = True; er = 'all good'
        except Exception as e:
            ok = False; er = e
        assert ok, er

def test_handle_load_each_model():
    path = os.getcwd()
    model_names = [o for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))]
    model_path = lambda model_name: os.path.join(path,'rms','models', model_name)

    for m in [*model_names,'dummy']:
        try:
            Model(model_path(m)).get_model()
            ok = True; er = 'all good'
        except Exception as e:
            ok = False; er = e
            if isinstance(e,ModelDefinitionError) and m == 'penicillin_goldrick_2017':
                ok = True; er = 'hadled ok'
            elif isinstance(e,FileNotFoundError) and m == 'dummy':
                ok = True; er = 'hadled ok'
        assert ok, er

def test_load_each_simulator():
    path = os.getcwd()
    # get all models in the models directory, skip penicilin
    model_names = [o for o in sorted(os.listdir(os.path.join('rms','models'))) if os.path.isdir(os.path.join('rms','models',o))]
    model_names.remove('penicillin_goldrick_2017')
    model_path = lambda model_name: os.path.join(path,'rms','models', model_name)

    for m in model_names:
        try:
            Simulator(model = Model(model_path(m)))
            ok = True; er = 'all good'
        except Exception as e:
            ok = False; er = e
        assert ok, er

def test_simple_dash():
    try:
        import dash_html_components as html
        app.layout = html.Div(id="nully-wrapper", children=0)
        ok = True; er = 'all good'
    except Exception as e:
        ok = False; er = e
    assert ok, er

def test_rms_dash():
    try:
        import dash_core_components as dcc
        import dash_html_components as html
        from dash.dependencies import Input, Output
        import dash_bootstrap_components as dbc
        from dash_apps.apps import main
        import dash_apps.shared_callbacks
        from dash_apps.shared_components import navbar, sidebar, sidebar_btn

        app.layout = html.Div([
            dcc.Location(id='url', refresh = False),
            navbar,
            sidebar,
            sidebar_btn,
            html.Div(id='page', children = main.layout)
        ])

        ok = True; er = 'all good'
    except Exception as e:
        ok = False; er = e
    assert ok, er


test_rms_dash()
test_simple_dash()
test_load_each_model()
test_handle_load_each_model()
test_load_each_simulator()