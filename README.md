# Reactor Modeling Sandbox
Here's an interactive tool to see how chemical reaction processes looks on a large scale. You can make predictions reactor outputs based on online measurements.
Check to see if your system's environment controls are working and test the efficiency of your machine.
\
\
\
![bioreactor](http://www.industrialpenicillinsimulation.com/images/IndPenSim_input_outputs_V2.png)
Source: http://www.industrialpenicillinsimulation.com
## Use cases:

- Meet Mary. Mary is an upstream process developer trying to optimize bioproduction of silk to be used for sustainable textile products. She believes that a better cooling system will improve overall protein yields, but needs to convince upper maganment to make the investment. To explain the process to non-engineers, she decides to __run simulations__ in the Reaction Modeling Sandbox. She uses the default penicilin fermentation model, but generalizes the simulations results to her specific use case in silk production. With a few clicks, she __varies the cooling water flow rate and temperature, and introduces disturbances to simulate faulty equipment__. She then __generates protein yield curves for the different conditions__, showing the importance of temperature control throughout the fermentation process. Upper managment can clearly see the performance improvement and decides to invest in a new cooling system for Mary.

- John is a chemical engineering undergrad at UW. He is currently taking a class on control theory but he's having trouble grasping feedback loops. His professor has suggested to use Reaction Modeling Sandbox to gain an intuition for the different variables and tunning parameters. Fortunantly, he is able to __implement his own control subroutines__ into the exisiting bioreactor model and simulate the system response under different control configurations.

- Dwight is a data analyst for a fermentation company. He has realized that off-line measurements are costly and time consuming, and that it may be possible to get good enough yield predictions based solely on on-line measurements. He is interested in testing several __machine learning models on the data available__ at Reactor Modeling Sandbox to see if this is actually the case. Later, he will __compare the different models on new simulation data__ and present it to upper managment, to hopefully receive the promotion to assistant data manager he's been dreaming of. 

- Jim's favorite pass time is to infuriate Dwight by messing up with the bioreactor without really affecting performance, so he never gets into trouble. He's eager to do some __sensitivity analysis__ on the new Reactor Modeling Sandbox models to see how far he can push the system and anger Dwight.

- Sally is a senior fermentation engineer at the same company. Her intern has just told her about Reactor Modeling Sandbox, and now she's trying to develop new models for their specific processes. Thankfully, Reactor Modeling Sandbox is capable of __loading custom bioreactor models and offer the same visualization and analysis capabalities__. Sally is able to customize the Reactor Modeling Sandbox and distriubute it among her colleagues.

- Jerry wants to verify his bioreactor's results and with a credible model without creating hundreds of batches and wasting tons of money. The Reactor Modeling Station is a tool that can __validate the process by comparing input and output parameters (ie. flow rates, nitrogen, temperature, pH, dissolved oxygen and pressure) with a simulation__. Jerry can run the simulation as many times as he likes to see if his production levels match those of the simulation.

- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process, completly substituting ODEs

## [Use cases](https://github.com/FermentAI/Fermentation-Station/blob/main/docs/use_cases.md#use-cases)
## User Checklist:
- [ ] Decide between advanced preferences to create a model or choose a simple model.
- [ ] Check the model and differential equations that you want.
- [ ] Check your parameters and any addtional settings.
- [ ] Check for data compatibility with the model; user input should align with the simulation output variables.
- [ ] Before the run, specify the input as a constant value or function
- [ ] Before the run, specify how many simulations you want to run
- [ ] Before the run, specify your control and variable parameters
- [ ] Run your simulation.
- [ ] Open a window that helps you select different output variables and use those to generate plots.
- [ ] Export the plots and/or raw data.

## Quick TO-DO list:
- [ ] get matlab model to run on python
- [ ] figure out scheme to wrap the model around, so then is easy to change the backend and update the frontend 
- [ ] set up frontend in a model-agnostic way
- [ ] widgets or dashboard to change inputs and visualize outputs?

## Future Works:
- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process, completely substituting ODEs.
- Allow the user to include their bioreactor build in the simulation and distinguish if parts are broken.

## Resources:
- dashboard / user interface: https://www.streamlit.io
- PID controller implementation: https://jckantor.github.io/CBE30338/04.01-Implementing_PID_Control_with_Python_Yield_Statement.html
- simple reactor example: https://jckantor.github.io/CBE30338/02.07-Fed-Batch-Bioreactor.html
- complex reactor example: https://jckantor.github.io/CBE30338/04.11-Implementing-PID-Control-in-Nonlinear-Simulations.html
- math input for variables/disturbances: https://docs.sympy.org/latest/modules/utilities/lambdify.html
- defining default model parameters and simulation settings: https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
