import time_advance_mechanisms as tam
import cupAndChaucArrivs as cc

"""
@Author: Tony Poerio, Alex Lederer, Sarah Dubnik
@email:  adp59@pitt.edu, alexlederer@pitt.ed, sad93@pitt.edu
University of Pittsburgh
Spring 2016
CS1538 - Simulation
Assignment #6 - Cup and Chaucer Simluation

Generates a Simulation for Arrival Service times at Cup and Chaucer Cafe at
the University of Pittsburgh library.

Goal is to determine the best way to staff Cup and Chaucer to minimize wait times
and increase customer throughput.
"""

####################
### CONTROL FLOW ###
####################
def main():

    # TEST OUR PROGRAM'S PIECES
    """hourly_arrivals = cc.generate_hourly_arrivals()
    arrivals_by_type = cc.gen_customer_type_distribution(hourly_arrivals)

    for arrival in arrivals_by_type:
        print arrival

    cashier_arrivals = cc.create_array_of_cashier_arrivals(arrivals_by_type)
    barista_arrivals = cc.create_array_of_barista_arrivals(arrivals_by_type)

    print "CASHIER ARRIVALS:"
    print "------------------"
    for arrival in cashier_arrivals:
        print arrival

    print "BARISTA ARRIVALS:"
    print "------------------"
    for arrival in barista_arrivals:
        print arrival
"""


    ################## UNCOMMENT TO RUN FULL SIM ################

    print "UNIVERISTY OF PITTSBURGH - SPRING 2016:: CS1538, Assignment #6"
    print "--------------------------------------------------------------"
    print ""
    print "This program simulates the service process at Cup & Chaucer Cafe in the Hillman Library" \
          "at the University of Pittsburgh. "
    print "Throughout the process, data is collected. At the end of the simulation, the relevant"
    print "data points are output here, at the console."
    print "If you simulate more than about 7 days, please allow a few minutes of runtime, depending"
    print "on how powerful your computer is. "
    print "------------------------------------"
    print "How may days would you like to simulate?"
    simulation_time = raw_input("> ")
    simulation_time = int(simulation_time)
    mySim = tam.Simulation()
    mySim.run_simulation(simulation_time)
    mySim.print_simulation_results()

    ######################################################################
    return


###################
### ENTRY POINT ###
###################

if __name__ == "__main__":
    main()

