# Fermentation Station
Here's an interactive tool to see how the fermentation process looks on a large scale. You can make predictions of fermentation outputs based on online measurements.
Check to see if your system's environment controls are working and test the efficiency of your machine.
\
\
\
![bioreactor](http://www.industrialpenicillinsimulation.com/images/IndPenSim_input_outputs_V2.png)
Source: http://www.industrialpenicillinsimulation.com
## Use cases:

- Meet Mary. Mary is an upstream process developer at FermentAI trying to optimize bioproduction of silk to be used for sustainable textile products. She believes that a better cooling system will improve overall protein yields, but needs to convince upper maganment to make the investment. To explain the process to non-engineers, she decides to __run simulations__ in the Fermenation Station. She uses the default penicilin fermentation model, but generalizes the simulations results to her specific use case in silk production. With a few clicks, she __varies the cooling water flow rate and temperature, and introduces distrubances to simulate faulty equipment__. She then __generates protein yield curves for the different conditions__, showing the importance of temperature control throughout the fermentation process. Upper managment can clearly see the performance improvement and decides to invest in a new cooling system for Mary.

- John is a chemical engineering undergrad at UW. He is currently taking a class on control theory but he's having trouble grasping feedback loops. His professor has suggested to use Fermentation Station to gain an intuition for the different variables and tunning parameters. Fortunantly, he is able to __implement his own control subroutines__ into the exisiting bioreactor model and simulate the system response under different control configurations.

- Dwight is a data analyst at FermentAI. He has realized that off-line measurements are costly and time consumming, and that it may be possible to get good enough yield predictions based solely on on-line measurements. He is interested in testing several __machine learning models on the data available__ at Fermentation Station to see if this is actually the case. Later, he will __compare the different models on new simulation data__ and present it to upper managment, to hopefully receive the promotion to assistant data manager he's been dreaming of. 

- Jim's favorite pass time is to infuriate Dwight by messing up with the bioreactor without really affecting performance, so he never gets into trouble. He's eager to do some __sensitivity analysis__ on the new Fermenation Station models to see how far he can push the system and anger Dwight.

- Sally is a senior fermentation engineer at FermentAI. Her intern has just told her about Fermentation Station, and now she's trying to develop new models for their specific processes. Thankfully, Fermenation Station is capable of __loading custom bioreactor models and offer the same visualization and analysis capabalities__. Sally is able to customize the Fermentation Station and distriubute it among her colleagues.

- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process, completly substituting ODEs

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
