
from pyfoomb import BioprocessModel
import pandas as pd
import os 
import importlib.util

class Model():

    # class to keep track of all model related info at a high level
    # receives directory name from drop down menu and loads corresponding data

    def __init__(self, model_path):
        self.name = model_path
        self.params = self.get_params() #read parameters
        self.mvars = self.get_mvars()
        self.cvars = None
        self.diagram = None
        self.model_class = self.get_model()
        self.state = self.get_state()
    
    def get_params(self):
        return pd.read_csv(os.path.join(self.name, 'parameters.csv')).set_index('Parameter')

    def get_mvars(self):
        return pd.read_csv(os.path.join(self.name, 'manipulated_vars.csv')).set_index('Var').fillna(False)

    def get_model(self):
        spec = importlib.util.spec_from_file_location('model', os.path.join(self.name, 'model.py'))
        model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model)
        return model.Model
    
    def get_all_params(self):
        return {**self.params.Value, **self.mvars[~self.mvars.State].Value}

    def get_state(self):
        return {**self.mvars[self.mvars.State].Value}