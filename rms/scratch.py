from model_def import Model 
import os
import glob
from pyfoomb import Caretaker
from pyfoomb import Visualization

path = os.getcwd()[:-4]
models = glob.glob(os.path.join(path,'models/**'))

a = Model(models[0])

caretaker = Caretaker(
    bioprocess_model_class=a.model_class, 
    model_parameters=a.get_all_params(), 
    initial_values=a.get_state(),
)