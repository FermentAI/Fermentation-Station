from engine import Model, Simulator, ModelDefinitionError
from dash_apps.apps.myapp import app
import dash_html_components as html

import os
import unittest

class MyTests(unittest.TestCase):

    def test_load_each_model(self):
        path = os.getcwd()
        # get all models in the models directory, skip penicilin
        model_names = [o for o in sorted(os.listdir(os.path.join('models'))) if os.path.isdir(os.path.join('models',o))]
        model_names.remove('penicillin_goldrick_2017')
        model_path = lambda model_name: os.path.join(path,'models', model_name)

        for m in model_names:
            try:
                Model(model_path(m)).get_model()
                ok = True; er = 'all good'
            except Exception as e:
                ok = False; er = e
            self.assertTrue(ok, model_path(m))

    def test_handle_load_each_model(self):
        path = os.getcwd()
        model_names = [o for o in sorted(os.listdir(os.path.join('models'))) if os.path.isdir(os.path.join('models',o))]
        model_path = lambda model_name: os.path.join(path,'models', model_name)

        for m in [*model_names,'dummy']:
            try:
                Model(model_path(m)).get_model()
                ok = True; er = 'all good'
            except Exception as e:
                if isinstance(e,ModelDefinitionError) and m == 'penicillin_goldrick_2017':
                    ok = True; er = 'hadled ok'
                elif isinstance(e,FileNotFoundError) and m == 'dummy':
                    ok = True; er = 'hadled ok'
                else:
                    ok = False; er = e

            self.assertTrue(ok, er)

    def test_load_each_simulator(self):
        path = os.getcwd()
        # get all models in the models directory, skip penicilin
        model_names = [o for o in sorted(os.listdir(os.path.join('models'))) if os.path.isdir(os.path.join('models',o))]
        model_names.remove('penicillin_goldrick_2017')
        model_path = lambda model_name: os.path.join(path,'models', model_name)

        for m in model_names:
            try:
                Simulator(model = Model(model_path(m)))
                ok = True; er = 'all good'
            except Exception as e:
                ok = False; er = e
            self.assertTrue(ok, er)

    def test_simple_dash(self):
        try:
            app.layout = html.Div(id="nully-wrapper", children=0)
            ok = True; er = 'all good'
        except Exception as e:
            ok = False; er = e
        self.assertTrue(ok, er)
    
    def test_run_each_simulator(self):
        path = os.getcwd()
        # get all models in the models directory, skip penicilin
        model_names = [o for o in sorted(os.listdir(os.path.join('models'))) if os.path.isdir(os.path.join('models',o))]
        model_names.remove('penicillin_goldrick_2017')
        model_path = lambda model_name: os.path.join(path,'models', model_name)

        for m in model_names:
            try:
                mysim = Simulator(model = Model(model_path(m)))
                mysim.set_inputs()
                data = mysim.run()
                mymvars = mysim.model.reset()
                
                ok = True; er = 'all good'
            except Exception as e:
                print(m)
                ok = False; er = e
            self.assertTrue(ok, er)
