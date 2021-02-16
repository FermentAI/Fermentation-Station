## Use cases:

- Meet Mary. Mary is an upstream process developer at FermentAI trying to optimize bioproduction of silk to be used for sustainable textile products. She believes that a better cooling system will improve overall protein yields, but needs to convince upper maganment to make the investment. To explain the process to non-engineers, she decides to __run simulations__ in the Reactor Modeling Sandbox. She uses the default penicilin fermentation model, but generalizes the simulations results to her specific use case in silk production. With a few clicks, she __varies the cooling water flow rate and temperature, and introduces distrubances to simulate faulty equipment__. She then __generates protein yield curves for the different conditions__, showing the importance of temperature control throughout the fermentation process. Upper managment can clearly see the performance improvement and decides to invest in a new cooling system for Mary.
5858 Horton St Suite 280, Emeryville, CA 94608- [ ] User: Selects the model
- [ ] RMS: Prompts user to enter modifications to the standard model.
- [ ] User: Enters modified reaction equations and rates.
- [ ] RMS: Prompts user to enters chemical names, concentrations, and reactor environmental conditions.
- [ ] User: Enters the requested information.
- [ ] RMS: Prompts user to choose variable and invariable conditions.
- [ ] User: Chooses to vary water flow rate and temperature.
- [ ] RMS: Asks user to enter the number of simulations to run.
- [ ] User: Types in the number of simulations and clicks run.
- [ ] RMS: Creates simulations from the user inputs. Displays run time and progress towards completion.
- [ ] User: Selects outputs graphs and variables to create a visual display.
- [ ] RMS: Displays the user's graphs after the simulation is complete.

- John is a chemical engineering undergrad at UW. He is currently taking a class on control theory but he's having trouble grasping feedback loops. His professor has suggested to use Reactor Modeling Sandbox to gain an intuition for the different variables and tunning parameters. Fortunantly, he is able to __implement his own control subroutines__ into the exisiting bioreactor model and simulate the system response under different control configurations.

- Dwight is a data analyst at FermentAI. He has realized that off-line measurements are costly and time consumming, and that it may be possible to get good enough yield predictions based solely on on-line measurements. He is interested in testing several __machine learning models on the data available__ at Fermentation Station to see if this is actually the case. Later, he will __compare the different models on new simulation data__ and present it to upper managment, to hopefully receive the promotion to assistant data manager he's been dreaming of. 

- Jim's favorite pass time is to infuriate Dwight by messing up with the bioreactor without really affecting performance, so he never gets into trouble. He's eager to do some __sensitivity analysis__ on the new Fermenation Station models to see how far he can push the system and anger Dwight.

- Sally is a senior fermentation engineer at FermentAI. Her intern has just told her about Fermentation Station, and now she's trying to develop new models for their specific processes. Thankfully, Fermenation Station is capable of __loading custom bioreactor models and offer the same visualization and analysis capabalities__. Sally is able to customize the Fermentation Station and distriubute it among her colleagues.

- Jerry wants to verify his bioreactor's results and with a credible model without creating hundreds of batches and wasting tons of money. The Fermentation Station is a tool that can __validate the process by comparing input and output parameters (ie. flow rates, nitrogen, temperature, pH, dissolved oxygen and pressure) with a simulation__. Jerry can run the simulation as many times as he likes to see if his production levels match those of the simulation.

- Patricia wants to check if her facility's bioreactor parts are working. She has made measurements for parameters along each reactor pathway. She can __use Fermentation Station to model her process at different settings and compare the off-line and on-line variables to those of the factory reactor__. A careful analysis of these results will tell what part(s) of the process require(s) maintenance.

- Data-driven vs model-driven? Maybe you only have data and want to create an ML model for the fermentation process, completly substituting ODEs
