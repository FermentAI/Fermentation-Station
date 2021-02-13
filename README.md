# Fermentation Station
Here's an interactive tool to see how the fermentation process looks on a large scale. You can make predictions of fermentation outputs based on online measurements.
Check to see if your system's environment controls are working and test the efficiency of your machine.
\
\
\
![bioreactor](http://www.industrialpenicillinsimulation.com/images/IndPenSim_input_outputs_V2.png)
Source: http://www.industrialpenicillinsimulation.com

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

## Resources:
- dashboard / user interface: https://www.streamlit.io
- PID controller implementation: https://jckantor.github.io/CBE30338/04.01-Implementing_PID_Control_with_Python_Yield_Statement.html
- simple reactor example: https://jckantor.github.io/CBE30338/02.07-Fed-Batch-Bioreactor.html
- complex reactor example: https://jckantor.github.io/CBE30338/04.11-Implementing-PID-Control-in-Nonlinear-Simulations.html
- math input for variables/disturbances: https://docs.sympy.org/latest/modules/utilities/lambdify.html
- defining default model parameters and simulation settings: https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
