import numpy as np

######################################
##### CUP AND CHAUCER GENERATORS #####
######################################
def generate_hourly_arrivals():

    # create the array in which we will hold all of our arrivals
    final_data_set_of_timed_arrivals = []

    # create a counter to keep track of our times
    current_time_in_minutes = 0.0
    current_minute = 0

    # get an array of arrivals by minute
    num_arrivals_per_minute = np.random.poisson(1.60833333,60)

    # get specific times in each minute at which the people arrive
    for arrivals_this_minute in num_arrivals_per_minute:

        counter = 1
        arrivals_this_minute_as_a_float = float(arrivals_this_minute)

        # generate a time for each arrival by getting 1/arrival_num
        while counter <= arrivals_this_minute:

            current_time_in_minutes += 1.0/arrivals_this_minute_as_a_float
            # print current_time_in_minutes
            # print current_minute
            final_data_set_of_timed_arrivals.append(current_time_in_minutes)
            counter += 1

        current_minute += 1

        # only if we didn't have any arrivals in the last minute,
        # we need to add a minute to the time
        if arrivals_this_minute == 0:
            current_time_in_minutes += 1

    return final_data_set_of_timed_arrivals


def gen_customer_type_distribution(arrival_times_array):
    number_of_arrivals = len(arrival_times_array)
    number_of_cashier_only_customers = np.random.binomial(number_of_arrivals, .6627)

    arrivals_by_type = []
    # figure out what type of customer each is,
    # and construct an array of tuples containing that info
    for arrival in arrival_times_array:

        # if we get a true, then that customer is a cashier only customer
        if (np.random.binomial(1, .6627) == 1):
            cashier_arrival_tuple = (arrival, "cashier")
            arrivals_by_type.append(cashier_arrival_tuple)
        # else, that customer is served by the barista
        else:
            barista_arrival_tuple = (arrival, "barista")
            arrivals_by_type.append(barista_arrival_tuple)

    return arrivals_by_type

def create_array_of_cashier_arrivals(tuple_of_arrivals):
    cashier_arrivals = []

    # grab only the cashier arrivals and put them into an array
    for arrival in tuple_of_arrivals:
        if arrival[1] == "cashier":
            cashier_arrivals.append(arrival[0])

    return cashier_arrivals

def create_array_of_barista_arrivals(tuple_of_arrivals):
    barista_arrivals = []

    # grab only the cashier arrivals and put them into an array
    for arrival in tuple_of_arrivals:
        if arrival[1] == "barista":
            barista_arrivals.append(arrival[0])

    return barista_arrivals


##########################################
##### CUP AND CHAUCER SERVICE TIME #######
##########################################
def gen_cashier_service_time():
    return np.random.exponential(1.0/0.07070707) * .01

def gen_barista_service_time():
    return np.random.exponential(1.0/0.0248083) * .01
