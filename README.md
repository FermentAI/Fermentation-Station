# Reactor Modeling Sandbox
[![Build Status](https://www.travis-ci.com/FermentAI/Reactor-Modeling-Sandbox.svg?branch=main)](https://www.travis-ci.com/github/FermentAI/Reactor-Modeling-Sandbox)
[![Coverage Status](https://coveralls.io/repos/github/FermentAI/Reactor-Modeling-Sandbox/badge.svg)](https://coveralls.io/github/FermentAI/Reactor-Modeling-Sandbox)

## App for Dynamic Model Exploration and Data Visualization
This DASH app is useful for selecting different chemical reactor models and playing with reactor parameters, such as Coolant Flow Rate, Reactor Temperature, Concentration, and more. It visualizes data from these selections as time plots of different variables, based on the user's preferences. Differential equations are used in each model to represent the chemical reactions occurring in the reactor. Understanding the way a reactor performs based on how different variables are manipulated can help with the design of more complex reactors. Our hope is that this DASH app can be used as a teaching tool for those looking to understand how a reactor works and how to adjust different parameters to meet the expected reaction products.
\
\
\
![RMS_Interface](https://user-images.githubusercontent.com/76971900/111372420-dc3a0a00-8657-11eb-8d50-49954cff9bc9.png)https://github.com/FermentAI/Reactor-Modeling-Sandbox/issues

## [Use cases](https://github.com/FermentAI/Reactor-Modeling-Sandbox/blob/main/rms/docs/use_cases.md#use-cases)



## Software Dependencies
- Python3
- plotly [Dash](https://dash.plotly.com/installation)
- [dash_core_components](https://pypi.org/project/dash-core-components/)
- [dash_html_components](https://pypi.org/project/dash-html-components/)
- [dash_bootstrap_components]()
- plotly [express](https://pypi.org/project/plotly-express/)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)

## How to Install
Clone this repository:

```sh
git clone https://github.com/FermentAI/Reactor-Modeling-Sandbox.git
```
Inside of the repository, run the setup.sh file:
```sh
bash setup.sh
```
Next, check for any errors. If there are, open an issue on github.
```sh
https://github.com/FermentAI/Reactor-Modeling-Sandbox/issues
```
If no errors arise, launch the app.
```sh
bash launch.sh
```
## Dash App Tutorial:
Once you have cloned the repository and installed the packages, the Dash app can be used to interact with different models to produce graphs of reactor variables. After launching the app, copy the URL to your browser. From there, you should see the interface.

The app loads a single chart without any lines or plots. From that point, you can choose a model from the dropdown menu at the top. Then, click add chart to produce multiple charts and select the chart type (line or bar) or variables you want to plot. Following this click the buttons above to see variables and manipulate their settings with the slider. Finally, rum simulation and see how the charts you added change according to you model and variable settings. Play around with it as much as you like.

## User Checklist:
- [ ] Choose a simple or complex model from the dropdown menu.
- [ ] Use the slider to select your model parameters.
- [ ] Click the button to run your simulation.
- [ ] Click the button to add charts.
- [ ] Select the variables you want to plot from the dropdown menu.
- [ ] Select the type of chart you want to visualize your data.
- [ ] Play around with the time feature to see your reactor's behavior at different time points.
- [ ] Add more graphs or change the parameters and run another simulation.

## Running Tests:

## Code Structure
```
|   LICENSE
|   README.md
|   environment.yml
|   setup.py
+---rms
|   +---dash_apps
|   |      __init__.py
|   |      shared_callbacks.cpython-38.pyc
|   |      shared_components.cpython-38.pyc
|   |      shared_styles.cpython-38.pyc
|   +---apps
|   |      dummy.py
|   |      main.py
|   |      myapp.py
|   +---shared_callbacks.py
|   +---shared_components.py
|   +---shared_styles.py
+---dash_main.py
+---docs
|       components_RMS.svg
|       landing_frontend_RMS.svg
|       tech_review_RMS.pdf
|       use_cases.md
|
+---engine.py
+---models
|   +---jckantor_complex
|   |       controlled_vars.csv
|   |       diagram.png
|   |       manipulated_vars.csv
|   |       model.py
|   |       parameters.csv
|   +---jckantor_simple
|   |       manipulated_vars.csv
|   |       model.py
|   |       parameters.csv
|   +---penicillin_goldrick_2017
|   |       model.py
+---simulator_vars.csv
+---test.py
```

## Running Tests
From the root directory: 
```
./runTests
```
If the executable file does not work, you can run the tests with the command: 

```
pytest --cov-report term --cov=diffcapanalyzer tests/
```


## Our Work Process:
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
