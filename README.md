# Cup and Chaucer Simulation
This is folder contains the written analysis, data collection and source code
for a discrete-event simulation undertaken to determine the best way to staff
Cup & Chaucer Cafe, in the Hillman Library at The University of Pittsburgh.

## How to run the simulation
In order to run the simulation, please navigate to the source code folder via
the command line and execute the following command:  "python main.py".

Running this command will initiate a prompt, asking you how many days you would
like to run the simulation. Anything over about 7 days may take a minute or two,
depending on your processing power, so please give it time. Please be aware that
this simulation generates arrivals for the system once every hour of simulation time,
and when arrivals are generated, we're printing a confirmation message to the screen.
We kept this output because we found it beneficial to know that the simulation is still 
working when we ran long simulations (say a full year).

At the end of the simulation, the results for all key data points will be printed to the
console, so you can see how everything did.

We ran a number of simulations with different parameters over the course of this project,
and this source code represents the final state--this is these are the parameters
We are recommending the airport to use. So our design decisions are reflected when
you run the simulation, and our data analysis can be seen in the accompanying documents.


## Dependencies
NumPy
Python Modules: Random, Math, Queue

## Additional Notes
The initial version of the experiment for this project is still intact, and we've included here. 
The initial experiment can still be run, if you'd like to see how the system looked when we first ran it. 
In order to do this, take the following steps: 
    1.  cd into the folder named "INITIAL_EXPERIMENT".
    2.  Run the project from within this folder:  "python main.py" 

