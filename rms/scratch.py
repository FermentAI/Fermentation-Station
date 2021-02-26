from model_def import Model, Simulator
import os
import glob
from pyfoomb import Visualization
import matplotlib.pyplot as plt

path = os.getcwd()[:-4]
models = glob.glob(os.path.join(path,'models/**/'))

a = Model(models[0])

sim = Simulator(
    model = a,
    t= 4,
    bioprocess_model_class=a.model_class, 
    model_parameters=a.get_all_params(), 
    initial_values=a.get_state(),
)

data = sim.run()

labels = [i[8:] for i in a.get_mvars()[a.get_mvars().State].Label]
for i in list(data):
    plt.figure()
    data[i].plot(use_index='True')
    plt.title(labels[i])