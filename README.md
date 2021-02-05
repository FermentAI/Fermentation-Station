# Fermentation Station
Here's an interactive tool to see how the fermentation process looks on a large scale. You can make predictions of fermentation outputs based on online measurements.
Check to see if your system's environment controls are working and test the efficiency of your machine.
\
\
\
![bioreactor](http://www.industrialpenicillinsimulation.com/images/IndPenSim_input_outputs_V2.png)
Source: http://www.industrialpenicillinsimulation.com
## Use cases:
- John is a chemical engineering student at UW. Tryng to learn control theory. run some optimization in Fermentation Station

- Dwight is a data analyst at FermentAI. Tryng to predict off-line measuremnts from on-line measurements to improve production

- Jim wants to mess up Dwight by perturbing bioreactor without really affecting yield, so he does not get fired.

- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process

- Meet Mary. Mary is an upstream process developer at FermentAI trying to optimize bioproduction of silk to be used for sustainable textile products. She believes that a better cooling system will improve overall protein yields, but needs to convince upper maganment to make the investment. To explain the process to non-engineers, she decides to run simulations in the Fermenation Station. She uses the default penicilin fermentation model, but generalizes the simulations results to her specific use case in silk production. With a few clicks, she varies the cooling water flow rate and temperature, and introduces distrubances to simulate faulty equipment. She then generates protein yield curves for the different conditions, showing the importance of temperature control throughout the fermentation process. Upper managment can clearly see the performance improvement and decides to invest in a new cooling system for Mary.

- Sally is a senior fermentation engineer at FermentAI. Her intern has just told her about Fermentation Station, and now she's trying to develop new models for their specific processes. Thankfully, Fermenation Station is capable of loading custom bioreactor models and offer the same visualization and analysis capabalities. Sally is able to customize the Fermentation Station and distriubute among her colleagues.  

## Quick TO-DO list:
- [ ] get matlab model to run on pyhon
- [ ] figure out scheme to wrap the model around, so then is easy to change the backend and update the frontend 
- [ ] set up frontend in a model-agnostic way
- [ ] widgets or dashboard to change inputs and visualize outputs?
