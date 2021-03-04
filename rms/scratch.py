from engine import Model, Simulator
import os
from pyfoomb import Visualization
import matplotlib.pyplot as plt
import numpy as np

path = os.getcwd()
d = 'rms\\models'
models = [os.path.join(path, d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]

a = Model(models[0])

sim = Simulator(model = a)

data = sim.run()

labels = [i for i in a.get_mvars_df()[a.get_mvars_df().State].Label]

_, ax = plt.subplots(1,3)

ax[2].plot(sim.time, data[0])
ax[2].set_title('Concentration')

ax[1].plot(sim.time, data[1])
ax[1].plot(sim.time, data[2])
ax[1].set_title('Temperature')
ax[1].legend(['Reactor','Cooling Jacket'], frameon = False)

ax[0].plot(sim.time, np.array(sim.subroutines.qLog))
ax[0].set_title('Coolant Flow Rate')

plt.show()
print('ok!')