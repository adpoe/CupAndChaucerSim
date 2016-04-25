# Cup and Chaucer Simulation
This is folder contains the written analysis, data collection and source code
for a discrete-event simulation undertaken to determine the best way to staff
Cup & Chaucer Cafe, in the Hillman Library at The University of Pittsburgh.

## How to run the simulation
In order to run the simulation, please navigate to the "FINAL_EXPERIMENT" folder via
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

## Additional Notes
The initial version of the experiment for this project is still intact, and we've included here. 
The initial experiment can still be run, if you'd like to see how the system looked when we first ran it. 
In order to do this, take the following steps: 
1) cd into the folder named "INITIAL_EXPERIMENT".
2) Run the project from within this folder:  "python main.py"  


## Dependencies
NumPy
Python Modules: Random, Math, Queue



## How the Program Works
Arrivals into the system are modeled hourly. We create an array of tuples which contain: The customer's arrival time, and their customer type. We then update the system time and see if anyone has arrived at the current time system-time. As soon as users arrive, they are placed in the Register Queue, and they start waiting. Each hour, the arrivals are refreshed, and the process continues. 

Customers are pushed customers through the system according to our parameters by updating the servers at each "clock-tick". The servers act as the force the that pull customers through the system once they have arrived. Whenever the system time is updated we check to see if each server is busy.  If the server is NOT busy, then it pulls the next available user from the queue it is serving, and calls the function to generate a service time. With each clock time (delta change), this service time is changed by -.01. Once the service time hits zero, the server pushes the user into the next queue (or the exit). And the server is no longer busy. Because the server is no longer busy, he can start looking for customers to serve, and the process repeats.  

Once customers reach end of the system, we tally how long they've been in the system. We also update other data collection parameters at this time, including:  Average Time In System (for both types of customers), Longest time in System, and Number of customers serviced (again categorized by customer type).  

We also collect data from the servers and queues to determine the state of the system at any given time.  Every time a user is pushed to the next step in the process, we gather data on that. This helps us determine if and WHERE there are any bottlenecks occur. We can also see how many users are 'still in the system' when the simulation finishes. Generally, the higher this number, the more inefficient our system has been performing. Large numbers of users left in the system means that lots of customers are getting stuck and never completing the queuing process. So a first goal is always to reduce this number as low as we possibly can, then optimize from there. 