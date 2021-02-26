from engine import Model, Simulator
import os
import glob
from pyfoomb import Visualization
import matplotlib.pyplot as plt
import numpy as np

path = os.getcwd()[:-4]
models = glob.glob(os.path.join(path,'models/**/'))

a = Model(models[0])

sim = Simulator(model = a)

data = sim.run()

labels = [i for i in a.get_mvars_df()[a.get_mvars_df().State].Label]
for i in list(data):
    plt.figure()
    data[i].plot(use_index='True')
    plt.title(labels[i])

# plt.figure()
# plt.plot(np.array(sim.subroutines.qLog))

# plt.figure()
# plt.plot(np.array(sim.subroutines.TLog))