
from pyfoomb import Caretaker
import pandas as pd
import numpy as np
import os
import errno
import importlib.util
import inspect
from scipy.integrate import odeint

class ModelDefinitionError(Exception):
    """Raised when there is a problem loading the model"""
    pass

class SubroutineError(Exception):
    """Raised when there is a problem running a subroutine"""
    pass

class Vars():
    """
    Manages sets of variables in a Pandas DataFrame.
    Receives model info and listens for changes in Dash.
    Keeps track of both defualt and current variable values.
    """
    def __init__(self, path, var_file):
        """
        Arguments
        ---------
            path :
                Path poiting to a specific model directory.
            var_file : 
                Name of the file to load.
        """
        self.path = path
        self.var_file = var_file
        self.default = self.read_vars()
        self.from_input = self.default.copy(True) 
        self.current = self.default.copy(True)
        self.REQUIRED = ['parameters.csv','manipulated_vars.csv','simulator_vars.csv', 'controlled_vars.csv']

    def _update(self, pd:pd.DataFrame):
        """
        Updates current variable values with values from passed DataFrame, based on index

        Arguments
        ---------
            pd: pd.DataFrame
                DataFrame with which to update vales
        """
        self.current.update(pd)

    def read_vars(self):
        """
        Reads the specified file into a Pandas DataFrame.
        The column "Var" is used as index.

        Raises
        ------
            FileNotFoundError
                If there is no file with that name in the specified directory.
        """
        try:
            return pd.read_csv(os.path.join(self.path, self.var_file)).set_index('Var').fillna(False).sort_index()
        except:
            if self.var_file in self.REQUIRED:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.path, self.var_file))
            else:
                return None

    def _eval_time(self, t:float):
        """
        Checks variables for functions, evaluates them with the current simulation time, and updates the current variables

        Arguments
        ---------
            t:flaot
        """
        funs = self.default.Value.apply(callable)
        if funs.any():
            for i in self.default[funs].index:
                self.current.loc[i,'Value'] = self.default.loc[i,'Value'](t)

    def get_all_vars_dict(self, t=0):
        """
        Return the current variable values in a dictionary
        
        Arguments
        ---------
            t:flaot
                Current time, provided by Simulator.
        """
        self._eval_time(t)
        return {**self.current.Value}

class Model():
    """
    Keeps track of all model related info at a high level
    Receives directory name and loads corresponding files

    """
    def __init__(self, model_path):
        """
        Arguments
        ---------
            model_path :
                Path poiting to a specific model directory.
        """
        self.path = model_path
        self.model_class = self.get_model()
        self.params = Vars(self.path, 'parameters.csv')
        self.mvars = Vars(self.path, 'manipulated_vars.csv')
        self.initial_values_dict = self.get_state_dict()
        self.subroutine_class = self.get_subroutine()
        self.doc = self.model_class.rhs.__doc__
        self.diagram = self.get_diagram()
        self.reset()

    def reset(self, hard = False):
        """
        Sets the current variables to their original value.
        If "hard", set the variables to the default values, otherwise to the current

        Arguments
        ---------
            hard : boolean
                Set the variables to the default values. Default is False
        """
        # back to default
        #current = self.mvars.current['Value'].copy(True)
        self.mvars.current = self.mvars.default.copy(True)
        # add rows to keep track of state
        self.state = self.mvars.current[self.mvars.current.State].copy(True)
        self.mvars.current.State = False
        self.state.index = self.state.index.map(lambda x: str(x)[:-1])
        self.state.Label = self.state.Label.map(lambda x: str(x)[8:])
        self.mvars.current = self.mvars.current.append(self.state)
        self.state = self.get_state_dict()
        #if hard is False: self.mvars._update(current)
        return self.mvars.current

    def __import_module(self):
        """
        Dynamic import of modules.
        Raises
        ------
            FileNotFoundError
                If there is no model.py file
        """
        try:
            spec = importlib.util.spec_from_file_location('model', os.path.join(self.path, 'model.py'))
        except:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(self.path, 'model.py'))
        model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(model)
        return model

    def get_model(self):
        """
        Imports the model class

        Raises
        ------
            ModelDefinitionError
                If there "MyModel" class has not been defined by the user
        """
        try:
            return self.__import_module().MyModel
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise e
            else:
                raise ModelDefinitionError('Need to define the class "MyModel" in the corresponding model file.')

    def get_subroutine(self):
        """
        Imports the subroutine class, if any
        """
        try:
            return self.__import_module().MySubroutines
        except AttributeError:
            return None

    def get_diagram(self):
        """
        Loads model diagram. If file not found, load default image.
        """
        if os.path.isfile(os.path.join(self.path,'diagram.png')):
            diagram_path =  os.path.join(self.path,'diagram.png')
        else:
            diagram_path = None # TODO
        return diagram_path

    def get_vars_dict(self, t = 0.):
        """
        Returns the current variables, excluding the state, in a dictionary

        Keyword Arguments
        -----------------
            t:flaot
                Current time, provided by Simulator. Degaults to 0.
        """
        self.mvars._eval_time(t)
        return {**self.params.get_all_vars_dict(t), **self.mvars.current[~self.mvars.current.State].Value}

    def get_all_vars_dict(self, t = 0.):
        """
        Returns all the current variables, including the state, in a dictionary

        Keyword Arguments
        -----------------
            t:flaot
                Current time, provided by Simulator. Degaults to 0.
        """
        return {**self.params.get_all_vars_dict(t), **self.mvars.get_all_vars_dict(t)}

    def get_state_dict(self, t = 0.):
        """
        Returns the state variables in a dictionary

        Keyword Arguments
        -----------------
            t:flaot
                Current time, provided by Simulator. Degaults to 0.
        """
        self.mvars._eval_time(t)
        self.state = {**self.mvars.current[self.mvars.current.State].Value}
        return self.state

    def update_mvars_from_dict(self, new_mvars_dict:dict, also_IC = False):
        """
        Updates manipulated variables from a dictionary

        Arguments
        ---------
            new_mvars_dict:dict
                Dicitonary with new values

        Keyword Arguments
        -----------------
            also_IC:boolean
                Flag used to also update the initial conditions. Degaults to False.
        """
        def _update(new_mvars_dict):
            new_mvars_df = pd.DataFrame.from_dict(new_mvars_dict, orient = 'index', columns = ['Value'])
            new_mvars_df.index.name = 'Var'
            self.mvars._update(new_mvars_df)

        _update(new_mvars_dict)
        if also_IC:
            new_mvars_dict = {key+'0': value for key, value in new_mvars_dict.items()}
            _update(new_mvars_dict)

class Simulator(Caretaker):
    """
    Wrapper for pyfoomb.Caretacker
    Keeps track of simulation settings
    Integrates the model and call subroutines
    """
    def __init__(self, model: Model,**kwds):
        """
        Arguments
        ---------
            model : Model
                Model object to integrate

        Keyword Arguments for Caretaker
        -------------------------------
            bioprocess_model_class : Subclass of BioprocessModel
                This class implements the bioprocess model.
            model_parameters : list or dict
                The model parameters, as specified in `bioprocess_model_class`.
            states : list
                The model states, as specified in `bioprocess_model_class`.
                Default is none, which enforces `initial_values` not to be None.
            initial_values : dict
                Initial values to the model, keys must match the states with a trailing '0'. 
                Default is None, which enforces `states` not to be None.
            replicate_ids : list
                Unique ids of replicates, for which the full model applies. 
                The parameters, as specified for the model and observation functions are  considered as global ones, 
                which may have different names and values for each replicate.
                Default is None, which implies a single replicate model.
            initial_switches : list
                A list of booleans, indicating the initial state of switches. 
                Number of switches must correpond to the number of return events in method `state_events`,
                if this method is implemented by the inheriting class.
                Default is None, which enables auto-detection of initial switches, which all will be False.
            model_name : str
                A descriptive model name. 
                Default is None.
            observation_funtions_parameters : list of tuples
                Each tuple stores a subclass of ObservationFunction 
                and a dictionary of its correponding parametrization.
                Default is None, which implies that there are no ObservationFunctions.
            model_checking_assistance : bool
                Runs a few sanity and call checks on the implemented model
        """
        super().__init__(
                bioprocess_model_class = model.model_class,
                model_parameters = model.get_all_vars_dict(),
                initial_values = model.initial_values_dict,
                **kwds)

        # read settings
        try:
            self.simvars = Vars(os.getcwd(), 'rms/simulator_vars.csv')
        except:
            self.simvars = Vars(os.getcwd(), 'simulator_vars.csv')
            
        self.model = model

        self.integrator = self.simvars.current.loc['integrator','Value']
        ti = float(self.simvars.current.loc['Ti','Value'])
        tf = float(self.simvars.current.loc['Tf','Value'])
        n = int(self.simvars.current.loc['n','Value'])
        self.dt = (tf-ti)/n
        self.simvars.current.loc['dt','Value'] = self.dt
        self.time = np.linspace(ti,tf,n) 

        # load subroutines
        if model.subroutine_class: 
            self.subroutines = model.subroutine_class(model, self)
        else:
            self.subroutines = None
    def set_inputs(self):
        """
        Sets the current variables to their input value.

        """
        self.model.mvars._update(self.model.mvars.from_input['Value'])
        if self.subroutines: self.subroutines.subrvars._update(self.subroutines.subrvars.from_input['Value'])
        self.model.params._update(self.model.params.from_input['Value'])
        self.simvars._update(self.simvars.from_input['Value'])
        
    def run(self): #TODO: beautify


        mdata = self.model.mvars.current.T[0:0].rename_axis('Time')
        
        try:
            cdata = self.subroutines.subrvars.current.T[0:0].rename_axis('Time')
        except:
            cdata = pd.DataFrame()

        for t in self.time:
            state = self.model.get_state_dict()
            mdata = pd.concat([mdata,pd.DataFrame(self.model.mvars.get_all_vars_dict(t),index = [t])])

            # run any subroutine
            if self.subroutines:
                self.subroutines._run_all(t)
                cdata = pd.concat([cdata,pd.DataFrame(self.subroutines.subrvars.get_all_vars_dict(t),index = [t])])
            else:
                pass

            # update, integrate, log
            self.simulators[None].set_parameters(self.model.get_vars_dict(t))

            if self.integrator == 'CVODE': # TODO: make sure this works
                results = self.simulate(np.array([t,t+self.dt]))
                # log data
                for i,(r,k) in enumerate(zip(results, state.keys())):
                    state[k] = r.values[-1]

            elif self.integrator == 'scipy':

                myfun = lambda y,t: self.model.model_class.rhs(self.simulators[None].bioprocess_model,t,y)
                results = odeint(myfun, t = np.array([t,t+self.dt]), y0 = [value for _, value in state.items()])[-1]
                # log data
                for i,(r,k) in enumerate(zip(results.T, state.keys())):
                    state[k] = r
            else:
                raise Exception('Integrator not recognized. Please use "CVODE" or "scipy".')


            self.model.update_mvars_from_dict(state, also_IC = True)

        return mdata.join(cdata)

class Subroutine():
    """
    Keeps track of all subrutine related info at a high level
    Receives model and simluator
    """
    def __init__(self, model: Model, simulator: Simulator):
        """
        Arguments
        ---------
            model : Model
                Model object this subroutine is associated with
            simulator : Simulator
                Simulator object running the model and subroutines
        """
        self.model = model
        self.subrvars = Vars(model.path, 'controlled_vars.csv')
        self.subroutine_vars = self.subrvars.get_all_vars_dict()
        self.model_parameters = model.get_all_vars_dict()
        self.model_state = model.get_state_dict()
        self.simulator_vars = simulator.simvars.get_all_vars_dict()

        self._initialization()

    def _initialization(self):
        """
        Method run once in the first integration iteration. Useful for initializing variables.

        THIS METHOD SHOULD BE OVERWRITTEN BY USER
        """
        pass
    
    def _run_all(self,t: float):
        """
        Eexecutes all subroutine methods specified by the user and udpates variables

        Arguments
        ---------
            t:flaot
                Current time, provided by Simulator.
        
        Raises
        ------
            SubroutineError
        """
        self.model_parameters = self.model.get_all_vars_dict(t)
        self.model_state = self.model.get_state_dict(t)
        self.subroutine_vars = self.subrvars.get_all_vars_dict()

        all_methods = (getattr(self, name) for name in dir(self))
        self.exe_methods = filter(lambda x: not x.__name__.startswith('_') ,filter(inspect.ismethod,all_methods))
        for method in self.exe_methods:
            try:
                method()
            except:
                raise SubroutineError('Run into an issue with the subroutine at time {}'.format(t))
        
        self.model.update_mvars_from_dict(self.model_parameters)

# this dsnt work

# class RMS_Model(BioprocessModel):
#     '''
#     Casting BioprocessModel to have consistent nomenclature
#     '''
#     def __init__(self, **kwds):
#         super(RMS_Model,self).__init__(**kwds)
#         self.model_vars = self._model_parameters