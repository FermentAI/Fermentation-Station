
from pyfoomb import BioprocessModel, Caretaker
import pandas as pd
import numpy as np
import os 
import importlib.util

class Model():

    # class to keep track of all model related info at a high level
    # receives directory name from drop down menu and loads corresponding data

    def __init__(self, model_path):
        self.model_name = model_path
        self.params = Vars(self.model_name, 'parameters.csv')
        self.mvars = Vars(self.model_name, 'manipulated_vars.csv')
        self.cvars = None
        self.diagram = None
        self.model_class = self.get_model()
        self.state = self.get_mv_state()
    
    def get_params(self):
        return self.params.current

    def get_mvars(self):
        return self.mvars.current

    def get_model(self):
        spec = importlib.util.spec_from_file_location('model', os.path.join(self.model_name, 'model.py'))
        model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model)
        return model.Model
    
    def get_all_params(self):
        return {**self.params.current.Value, **self.mvars.current[~self.mvars.current.State].Value}

    def get_mv_state(self):
        return {**self.mvars.current[self.mvars.current.State].Value}

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state.update(state)
        return

class Vars():
    
    # class to keep track of a set of variables
    # receives model info and listents for changes in dash

    def __init__(self, model_name, var_file):
        self.model_name = model_name
        self.var_file = var_file
        self.default = self.read_vars()
        self.current = self.default
    
    def __update(self, pd):
        self.current = pd

    def read_vars(self):
        return pd.read_csv(os.path.join(self.model_name, self.var_file)).set_index('Var').fillna(False).sort_index()


class Simulator(Caretaker):

    # wrapper for caretacker
    # keep track of simulation settings
    # keep track of control subroutines?
    # evaluate time-dependent input

    def __init__(self, model,  t:np.ndarray,**kwds):
        super(Simulator, self).__init__(**kwds)
        self.time = t
        self.model = model


    def run(self):
        ti = 0
        tf = self.time
        n = 100
        time = np.linspace(ti,tf,n)
        dt = (tf-ti)/n
        data = [[] for _ in range(len(self._Caretaker__initial_values))]
        for t in time:
            # PID control calculations
            # eP = beta*Tsp - T
            # eI = Tsp - T
            # eD = gamma*Tsp - T
            # qc -= kp*(eP - eP_) + ki*dt*eI + kd*(eD - 2*eD_ + eD__)/dt
            # qc = sat(qc)
            
            # log data and update state
            self.simulators[None]._initial_values = self.model.get_state()
            results = self.simulate(np.array([t,t+dt]), self.model.get_all_params())

            for i,(r,k) in enumerate(zip(results, self.model.state.keys())):
                self.model.state[k] = r.values[-1]
                data[i].append(r.values[-1])

        return pd.DataFrame(data).T.set_index(time, 'Time')