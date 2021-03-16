# Reactor Modeling Sandbox
[![Build Status](https://www.travis-ci.com/FermentAI/Reactor-Modeling-Sandbox.svg?branch=main)](https://www.travis-ci.com/github/FermentAI/Reactor-Modeling-Sandbox)
[![Coverage Status](https://coveralls.io/repos/github/FermentAI/Reactor-Modeling-Sandbox/badge.svg)](https://coveralls.io/github/FermentAI/Reactor-Modeling-Sandbox)

Here's an interactive tool to see how a chemical reactor works. You can play around with the inputs to see how they affect your reactor's outputs. Variables can be visualized on as many graphs as you want.
\
\
\
![RMS_Interface](https://user-images.githubusercontent.com/76971900/111372420-dc3a0a00-8657-11eb-8d50-49954cff9bc9.png)

## [Use cases](https://github.com/FermentAI/Reactor-Modeling-Sandbox/blob/main/rms/docs/use_cases.md#use-cases)

## App for Reactor Modeling Simulated Data Visualization
This dash app is useful for selecting different chemical reactor models and playing with reactor parameters, such as Coolant Flow Rate, Reactor Temperature, Concentration, and more. It visualizes data from these selections as time plots of different variables, based on the user's preferences. Differential equations are used in each model to represent the chemical reactions occurring in the reactor. Understanding the way a reactor performs based on how different variables are manipulated can help with the design of more complex reactors. Our hope is that this DASH app can be used as a teaching tool for those looking to understand how a reactor works and how to adjust different parameters to meet the expected reaction products.

## User Checklist:
- [ ] Choose a simple or complex model from the dropdown menu.
- [ ] Use the slider to select your model parameters.
- [ ] Click the button to run your simulation.
- [ ] Click the button to add charts.
- [ ] Select the variables you want to plot from the dropdown menu.
- [ ] Select the type of chart you want to visualize your data.
- [ ] Play around with the time feature to see your reactor's behavior at different time points.
- [ ] Add more graphs or change the parameters and run another simulation.

## Our Thought Process:
- [ ] Review other reactor model simulators: simple, complex, and industrial penicillin.
- [ ] Decide what interface building tool to use: dash, bokeh, voila, or streamlit.
- [ ] Design the models in separate files to simulate simple or complex reactors.
- [ ] Assign initial input values to manipulated or constant variables.
- [ ] Prepare a dash interface to visualize a graph of different parameters after running the simulation.
- [ ] Create sliders for the user to select values for each parameter.
- [ ] Create a simulate button for the user to interact with and initiate the graph display.
- [ ] Create a dropdown for the user to select different models.
- [ ] Design callbacks to relate the model selection to their respective model files.
- [ ] Create an "Add chart" button to add any number of charts as a line or bar graph.
- [ ] Create a dropdown to select a variable to plot.
- [ ] Design callbacks to relate the variable selections to the appropriate variables output from the simulation.
- [ ] Combine the model selection feature with the "Add Chart" button, chart style, and Variable dropdown features.
- [ ] Add a time element to allow the user to slide through different time points on each graph.

## Future Works:
- Make it possible for the user to download charts and raw data from each simulation.
- Create a way for the user to add their own reactor model with its own differential equations.
- Allow the user to see graphs change in real time with the simulation and manipulating input variables.
- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process, completely substituting ODEs.
- Allow the user to include their bioreactor build in the simulation and distinguish if parts are broken.

## Resources:
- dashboard / user interface: https://www.streamlit.io
- PID controller implementation: https://jckantor.github.io/CBE30338/04.01-Implementing_PID_Control_with_Python_Yield_Statement.html
- simple reactor example: https://jckantor.github.io/CBE30338/02.07-Fed-Batch-Bioreactor.html
- complex reactor example: https://jckantor.github.io/CBE30338/04.11-Implementing-PID-Control-in-Nonlinear-Simulations.html
- math input for variables/disturbances: https://docs.sympy.org/latest/modules/utilities/lambdify.html
- defining default model parameters and simulation settings: https://stackabuse.com/reading-and-writing-yaml-to-a-file-in-python/
- pyFOOMB: https://onlinelibrary.wiley.com/doi/full/10.1002/elsc.202000088
