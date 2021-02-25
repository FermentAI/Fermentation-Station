from model_def import Model, Simulator
import os
import glob
from pyfoomb import Visualization

path = os.getcwd()[:-4]
models = glob.glob(os.path.join(path,'models/**'))

a = Model(models[0])

sim = Simulator(
    model = a,
    t= 8,
    bioprocess_model_class=a.model_class, 
    model_parameters=a.get_all_params(), 
    initial_values=a.get_state(),
)

data = sim.run()