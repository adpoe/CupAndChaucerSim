import Queue as q
import cupAndChaucArrivs as cc

"""
Discrete time advance mechanisms for airport simulation project.
This class will generate 6 hours worth of passenger arrivals, and store the data in two arrays:
- One for commuters passengers
- One for international passengers

For each passenger, also need to generate their wait times for each queue. Or is that done when a passenger queues up?

"""


"""
Goals
------

Generalize this code so it can be used for ANY queuing system.

Need to account for:
- How many steps?
   :: Spawn a Server-Queue System for each of these.... link these all together
        o  How many servers at each step?
        o  How many queues at each step?
             -- Make a class that holds each of these "single step" systems
             -- interface between these classes
             -- glue them all together with a start and end point
             -- make them each a member of the overall system and use the same time advance
             mechanisms I've already got in place.


"""

###########################
### ARRIVAL GENERATION ####
###########################
class CupChaucArrivals():
    """ Class used to generate one hour of arrivals at a time
    """
    def __init__(self):
        self.cashier_arrivals = []
        self.barista_arrivals = []


    def get_arrivals(self):
        """ Get all the arrivals to the system in the next six hours. Store the values in instance vars.
        """
        hourly_arrivals = cc.generate_hourly_arrivals()
        arrivals_by_type = cc.gen_customer_type_distribution(hourly_arrivals)

        self.cashier_arrivals = cc.create_array_of_cashier_arrivals(arrivals_by_type)
        self.barista_arrivals = cc.create_array_of_barista_arrivals(arrivals_by_type)



##########################
#### CHECK-IN QUEUES #####
##########################

#------------------#
#   C&C Queues     #
#------------------#
class RegisterQueue:
    """ Class used to model a register line Queue
    """
    def __init__(self):
        self.queue = q.Queue()
        self.customers_added = 0

    def add_customer(self, new_customer):
        self.queue.put_nowait(new_customer)
        self.customers_added += 1

    def get_next_customer_in_line(self):
        if not self.queue.empty():
            next_customer = self.queue.get_nowait()
            self.queue.task_done()
        else:
            next_customer = None
        return next_customer

class BaristaQueue:
    """ Class used to model a register line Queue
    """
    def __init__(self):
        self.queue = q.Queue()
        self.customers_added = 0

    def add_customer(self, new_customer):
        self.queue.put_nowait(new_customer)
        self.customers_added += 1

    def get_next_customer_in_line(self):
        if not self.queue.empty():
            next_customer = self.queue.get_nowait()
            self.queue.task_done()
        else:
            next_customer = None
        return next_customer

#                    #
#   End C&C Queues   #
#                    #




###########################
######  C&C SERVERS  ######
###########################
class CashierServer:
    """ Class used to model a server at the Check-in terminal
    """
    def __init__(self):
        """ Initialize the class variables
        """
        self.service_time = 0.0
        self.busy = False
        self.customer_being_served = q.Queue()
        self.customers_added = 0
        self.customers_served = 0
        self.idle_time = 0.00

    def set_service_time(self):
        """ Sets the service time for a new passenger
        :param passenger_type:  either "commuter" or "international"
        """
        self.service_time = cc.gen_cashier_service_time()
        self.busy = True

    def update_service_time(self):
        """ Updates the service time and tells us if the server is busy or not
        """
        self.service_time -= 0.01

        if self.service_time <= 0:
            self.service_time = 0
            self.busy = False

        if not self.is_busy():
            self.idle_time += 0.01

    def is_busy(self):
        """ Call this after updating the service time at each change in system time (delta). Tells us if server is busy.
        :return: True if server is busy. False if server is NOT busy.
        """
        return self.busy

    def add_customer(self, new_passenger):
        """ Adds a customer to the sever and sets his service time
        :param new_passenger: the passenger we are adding
        """
        # get the type of flight his passenger is on
        # add the passenger to our service queue
        self.customer_being_served.put_nowait(new_passenger)
        # set the service time, depending on what type of flight the customer is on
        self.set_service_time()
        # update the count of customers added
        self.customers_added += 1


    def complete_service(self):
        """ Models completion of our service
        :return: the customer who has just finished at this station
        """
        if not self.is_busy() and not self.customer_being_served.empty():
            next_customer = self.customer_being_served.get_nowait()
            self.customer_being_served.task_done()
            self.customers_served += 1
        else:
            next_customer = None
        return next_customer


class BaristaServer:
    """ Class used to model a server at the Security terminal
    """
    def __init__(self):
        """ Initialize the class variables
        """
        self.service_time = 0.0
        self.busy = None
        # self.customer = None
        self.customer_being_served = q.Queue()
        self.is_barista_class = False
        self.customers_added = 0
        self.customers_served = 0
        self.idle_time = 0.0

    def set_service_time(self):
        """ Sets the service time for a new passenger
        :param passenger_type:  either "commuter" or "international"
        """
        self.service_time = cc.gen_barista_service_time()
        self.busy = True

    def update_service_time(self):
        """ Updates the service time and tells us if the server is busy or not
        """
        self.service_time -= 0.01

        if self.service_time <= 0:
            self.service_time = 0
            self.busy = False

        if not self.is_busy():
            self.idle_time += 0.01

    def is_busy(self):
        """ Call this after updating the service time at each change in system time (delta). Tells us if server is busy.
        :return: True if server is busy. False if server is NOT busy.
        """
        return self.busy

    def add_customer(self, new_customer):
        """ Adds a customer to the sever and sets his service time
        :param new_passenger: the passenger we are adding
        """
        # add the passenger to our service queue
        self.customer_being_served.put_nowait(new_customer)
        # set the service time, depending on what type of flight the customer is on
        self.set_service_time()
        # update the count of customers added
        self.customers_added += 1

    def complete_service(self):
        """ Models completion of our service
        :return: the customer who has just finished at this station
        """
        next_customer = None
        # only try to pull a customer from the queue if we are NOT busy
        # AND the queue isn't empty
        # else we just return a None
        if not self.is_busy() and not self.customer_being_served.empty():
            next_customer = self.customer_being_served.get_nowait()
            self.customer_being_served.task_done()
            self.customers_served += 1
        else:
            next_customer = None
        return next_customer



#############################
######  C&C CUSTOMERS  ######
#############################
class Customer:
    """ Class used to model a passenger in our simulation
    """
    def __init__(self, system_time, customer_class, system_iteration, relative_time):
        self.system_time_entered = system_time
        self.customer_class = customer_class
        self.system_iteration = system_iteration
        self.relative_time = relative_time
        #--------DEBUGGING-------
        #if flight_type == "international" and system_time > 1490:
        #    print "here"
        #
        #confirm_system_time = (system_time / system_iteration)
        #confirm_relative_time = str(relative_time)
        #relative_system_time = system_time / (system_iteration * 360.0)
        #if not str(math.floor((system_time / system_iteration))) == str(math.floor(relative_time)):
        #    print "something's off."
        #------------------------

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))


##########################
#### SIMULATION CLASS ####
##########################

class Simulation:
    """ Class used to house our whole simulation
    """
    def __init__(self):
        """ Sets up all the variables we need for the simulation
        """
        #----TIME----
        # Time variables
        self.system_time = 0.00
        self.delta = 0.01
        self.hours_passed = 0   # = number of system iterations
        self.system_iteration = 0
        self.relative_global_time = 0.00
        self.time_until_next_arrival_generation = 60.0

        #-----ARRIVALS-----
        # Arrival list
        self.barista_ARRIVALS = []
        self.cashier_ARRIVALS = []
        # All arrivals
        self.arrivals = [self.barista_ARRIVALS,
                         self.cashier_ARRIVALS]

        #----QUEUES-----
        # Check-in Queues - separate for first and coach
        self.register_QUEUE = RegisterQueue()
        # Security Queues - also separate for first and coach
        self.barista_QUEUE = BaristaQueue()

        # All Queues
        self.queues = [self.register_QUEUE,
                       self.barista_QUEUE]

        #------SERVERS-------
        # Register Servers
        self.CASHIER_server01 = CashierServer()
        self.check_in_servers = [self.CASHIER_server01]

        # Barista Servers
        self.BARISTA_server01 = BaristaServer()
        self.BARISTA_server02 = BaristaServer()
        self.BARISTA_server03 = BaristaServer()
        self.barista_servers = [self.BARISTA_server01,
                                self.BARISTA_server02,
                                self.BARISTA_server03]
        # All servers
        self.servers = [self.CASHIER_server01,
                        self.BARISTA_server01,
                        self.BARISTA_server02,
                        self.BARISTA_server03,
                        ]



        #----INTERNAL_DATA COLLECTION-----
        self.total_cashier_customers_arrived = 0
        self.total_cashier_customers_serviced = 0
        self.total_barista_customers_arrived = 0
        self.total_barista_customers_serviced = 0
        self.customers_combined = 0
        # Then counters to see how far people are making it in the system....
        # Averaged data
        self.time_in_system = []
        self.time_in_system_CASHIER = []
        self.avg_time_in_system = 0
        self.avg_time_in_system_CASHIER = []
        self.time_in_system_BARISTA = []


        #-----INTERNAL MECHANISMS------
        self.data_users_added_to_REGISTER_QUEUE = 0
        self.data_users_added_to_BARISTA_QUEUE = 0
        self.data_users_added_to_FIRSTCLASS_SECURITY_QUEUE = 0
        self.data_CASHIER_customers_moved_to_EXIT = 0
        self.data_BARISTA_customers_moved_to_EXIT = 0
        self.data_users_currently_in_system = 0
        self.total_server_idle_time = 0.0
        self.data_num_customers_wait_over_one_min = 0



    def generate_ONE_HOUR_of_arrivals(self):
        """ Generates six hours of arrivals and stores in our ARRIVAL LIST instance variables.
        """
        # Create instance of arrival class
        new_arrivals = CupChaucArrivals()
        # Generate new arrivals
        new_arrivals.get_arrivals()
        # Add one to the system iteration (denoted by international flight number)
        self.hours_passed += 1

        # Transfer those values into our simulation, as arrivals for next six hours
        self.barista_ARRIVALS = new_arrivals.barista_arrivals
        self.cashier_ARRIVALS = new_arrivals.cashier_arrivals


        # clean up arrivals, so nothing greater 60, because we'll never reach it
        for arrival in new_arrivals.cashier_arrivals:
            if arrival > 59.99999999:
                new_arrivals.cashier_arrivals.remove(arrival)

        for arrival in new_arrivals.barista_arrivals:
            if arrival > 59.99999999:
                new_arrivals.barista_arrivals.remove(arrival)


        # Count our arrivals for data collection
        self.total_cashier_customers_arrived += len(new_arrivals.cashier_arrivals)
        self.total_barista_customers_arrived += len(new_arrivals.barista_arrivals)
        print "arrivals generated for hour: " + str(self.hours_passed)


    def update_servers(self):
        """ Updates servers after a change of DELTA in system time
        """
        for server in self.servers:
            server.update_service_time()

    def collect_and_create_passengers_from_arrivals(self):
        """ Looks at all arrival lists, and if there is new arrival at the current system time,
            creates a passenger object for use in the system, and places it in the check-in queue
        """
        relative_time = self.relative_global_time


        # make sure we're not checking an array that's empty
        if not len(self.barista_ARRIVALS) == 0:
            # Then get next available item from INTL FIRST CLASS ARRIVALS
            if self.barista_ARRIVALS[0] <= relative_time:
                # create passenger, put it in first class check in queue
                new_customer = Customer(self.system_time, "barista", self.hours_passed,
                                        self.barista_ARRIVALS[0])
                self.register_QUEUE.add_customer(new_customer)
                # pop from the list
                self.barista_ARRIVALS.pop(0)


        # make sure we're not checking an array that's empty
        if not len(self.cashier_ARRIVALS) == 0:
            # Then get next available item from COMMUTER COACH CLASS ARRIVALS
            if self.cashier_ARRIVALS[0] <= relative_time:
                # create passenger, put it in coach class check in queue
                new_customer = Customer(self.system_time, "cashier", self.hours_passed,
                                        self.cashier_ARRIVALS[0])
                self.register_QUEUE.add_customer(new_customer)
                # pop from the list
                self.cashier_ARRIVALS.pop(0)

    def move_to_CASHIER_server(self):
        """ Look at check in servers, and if they are not busy, advance the first item in the correct queue
            to the correct (and open) check in server
        """
        #>>>>>> Later, change this go through all checkin servers in a loop and do same action.
        #       This code can be very much condensed

        # If first class check-in server is NOT busy
        if not self.CASHIER_server01.is_busy():
            # de-queue from the FIRST class check-in queue
            if not self.register_QUEUE.queue.empty():
                next_passenger = self.register_QUEUE.queue.get()
                self.register_QUEUE.queue.task_done()
                # and move next passenger to server, since it isn't busy
                self.CASHIER_server01.add_customer(next_passenger)


    def update_register_queues(self):
        """ Updates queues after a change of DELTA in system time
        """
        # then check the servers, and if they're free move from queue to server
        self.move_to_CASHIER_server()
        # Check all arrivals and if the arrival time matches system time...
        # Create a passenger and ADD the correct queue
        self.collect_and_create_passengers_from_arrivals()


    def update_barista_queues(self):
        """ Updates queues after a change of DELTA in system time
        """
        # Check all check-in servers...  and if they are NOT busy, take their passenger...
        # Take the passenger, add the correct security queue

        # First, look at all servers
        for server in self.check_in_servers:
            # and if the server is NOT busy
            # if not server.is_busy():
            #if not server.last_customer_served.empty():
                # Take the passenger, who must have just finished being served
                my_customer = server.complete_service()
                # and move them to the correct security queue
                if not my_customer == None:
                    # but first make sure that the passenger does not == None
                    if my_customer.customer_class == "cashier":
                        # add to end of simulation
                        self.data_CASHIER_customers_moved_to_EXIT += 1
                        # data collection for coach
                        time_in_system = self.system_time - my_customer.system_time_entered
                        self.time_in_system.append(time_in_system)
                        self.time_in_system_CASHIER.append(time_in_system)
                        # data collection for commuters
                        self.time_in_system_CASHIER.append(time_in_system)
                        self.total_cashier_customers_serviced += 1
                     # else, add to barista queue
                    else:
                        # because if they are NOT cashier customers, they must be barista customers
                        self.barista_QUEUE.add_customer(my_customer)


    def move_to_BARISTA_server(self):
        """ If servers are not busy, advance next passenger in the security queue to to security server
        """
        # step through all the security servers and check if they are busy
        for server in self.barista_servers:
            # if the server isn't busy, we can take the next passenger from security queue
            # and put him in the server
            if not server.is_busy():
                # first make sure it's not empty
                if not self.barista_QUEUE.queue.empty():
                    # and if it's not, grab the next passenger out of it
                    next_customer = self.barista_QUEUE.queue.get()
                    self.barista_QUEUE.queue.task_done()
                    # And move that passenger into the available security server
                    server.add_customer(next_customer)


    def move_to_EXIT(self):
        """ Look at Security servers, and if they are NOT busy, someone just finished security screening.
            This means they've completed the queuing process.
            ---
            Once through queuing, go to GATE.
            Commuters --> Go straight to gate waiting area
            International --> First check if they missed their flight.
                - If yes:  They leave
                - If no:   They go to international gate
        """
        # step through all the security servers
        for server in self.barista_servers:
            # if the server is NOT busy
            #if not server.is_busy():
            #if not server.last_customer_served.empty():
                # passenger has completed queuing phase, and can move to gate.
                # but first, we need to check if they are commuters or international flyers
                # and in each case, need to handle that accordingly
                next_customer = server.complete_service()
                # first make sure that the passenger isn't a NONE
                if not next_customer == None:
                    # if the passenger is a commuter, they just go to gate
                    if next_customer.customer_class == "barista":
                        self.data_BARISTA_customers_moved_to_EXIT += 1
                        # data collection for coach
                        time_in_system = self.system_time - next_customer.system_time_entered
                        self.time_in_system.append(time_in_system)
                        self.time_in_system_BARISTA.append(time_in_system)
                        # data collection for commuters
                        self.time_in_system_BARISTA.append(time_in_system)
                        self.total_barista_customers_serviced += 1


    def advance_system_time(self):
        """ Advances the system time by delta --> .01 of a minute
            - Looks for arrivals at current time
            - If an arrival is valid, create a passenger object and place it in the proper Queue
            - Needs to update EVERY QUEUE and SERVER, advance wherever needed
        """
        # every six hours, generate new arrivals,
        # and perform accounting procedures on ticket
        # for those arrivals
        #if self.time_until_international_flight <= 0.0:
        #    self.generate_SIX_HOURS_of_arrivals()
        #    self.collect_revenue()
        #    self.every_six_hours_deduct_operating_costs()


        # increment the system time by delta
        self.system_time += self.delta
        self.time_until_next_arrival_generation -= self.delta

        # keep track of relative global time
        self.relative_global_time += self.delta
        if self.relative_global_time >= 60.0:
            self.relative_global_time = 0.0

        #print "gets system time update"

        # skip these on the first iteration because we don't have data yet
        if not self.hours_passed == 0:

            #DO IT IN REVERSE ORDER
            # start by updating the servers
            self.update_servers()
            # then, if we can pull someone FROM a sever, while not busy, do it
            self.move_to_EXIT()
            self.update_barista_queues()
            # then get passengers from arrivals, and fill the queues
            self.collect_and_create_passengers_from_arrivals()
            # then move people into any empty spots in the servers
            self.move_to_BARISTA_server()
            self.move_to_CASHIER_server()

        # every six hours, generate new arrivals,
        # and perform accounting procedures on ticket
        # for those arrivals
        if self.time_until_next_arrival_generation <= 0:
            self.generate_ONE_HOUR_of_arrivals()
            self.time_until_next_arrival_generation = 60.0

        #print "checks if planes depart"

        # print self.system_time

    def run_simulation(self, simulation_time_in_days):
        """ Use this to run simulation for as long as user has specified, in days
            While the counter < # of days, keep generating the arrivals every 6 hours
            and stepping through the simulation
        """
        simulation_time_in_minutes = simulation_time_in_days * 24.0 * 60.0 + 60.0
        # = days * 24 hours in a day * 60 minutes in an hour
        while self.system_time < simulation_time_in_minutes:
            # then, advance system time by delta:  0.01
            self.advance_system_time()

        print "SIMULATION COMPLETE:"


    #############################################
    ####### DATA REPORTING AND ANALYSIS #########
    #############################################

    def print_simulation_results(self):
        """ prints the results of our simulation to the command line/console
        """
        print "###################################"
        print "####### SIMULATION RESULTS ########"
        print "###################################"
        print "#-----System Info-----"
        print "Total CASHIER customers ARRIVED="+str(self.total_cashier_customers_arrived)
        print "Total CASHIER customers SERVICED="+str(self.total_cashier_customers_serviced)
        print "Total BARISTA customers ARRIVED="+str(self.total_barista_customers_arrived)
        print "Total BARISTA customers SERVICED="+str(self.total_barista_customers_serviced)
        total_customers_serviced = self.total_barista_customers_serviced + self.total_cashier_customers_serviced
        print "Total CUSTOMERS (all types) SERVICED="+str(total_customers_serviced)
        print "-------Averages-------"
        #sum_time_in_system = sum(self.time_in_system)
        length_of_time_in_system_list = len(self.time_in_system)
        #length_of_time_in_system_list = float(length_of_time_in_system_list)
        #print "SUM OF TIME IN SYSTEM: "+str(sum_time_in_system)
        #print "LENGTH OF TIME IN SYSTEM: "+str(length_of_time_in_system_list)
        self.avg_time_in_system = sum(self.time_in_system)/len(self.time_in_system)
        print "AVG Time In System for ALL CUSTOMERS (who make make it to EXIT)="+str(self.avg_time_in_system)
        self.time_in_system.sort(reverse=True)
        longest_time_in_system = self.time_in_system.pop(0)
        print "Longest time in system="+str(longest_time_in_system)
        average_time_in_system_cashier = sum(self.time_in_system_CASHIER) / len(self.time_in_system_CASHIER)
        print "AVG Time in system CASHIER="+str(average_time_in_system_cashier)
        average_time_in_system_barista = sum(self.time_in_system_BARISTA) / len(self.time_in_system_BARISTA)
        print "AVG Time in system all BARISTA="+str(average_time_in_system_barista)
        print "------Internal Mechanisms-------"
        print ".......Stage 1......"
        print "Customers added to RegisterQueue="+str(self.register_QUEUE.customers_added)
        print "......Stage 2......."
        print "Customers added to BaristaQueue="+str(self.barista_QUEUE.customers_added)
        print "......Stage 3......."
        print "CASHIER customers who make it to EXIT="+str(self.data_CASHIER_customers_moved_to_EXIT)
        print "BARISTA customers who make it to EXIT="+str(self.data_BARISTA_customers_moved_to_EXIT)
        print ". . . . didn't make it . . . . ."
        still_in_system = 0
        for queue in self.queues:
            still_in_system += queue.queue.qsize()
        print "Users STILL in SYSTEM="+str(still_in_system)


        print "======= GOALS ========"
        self.total_server_idle_time = 0.0
        for server in self.check_in_servers:
                self.total_server_idle_time += server.idle_time
        print "AGENTS' Total Idle Time="+str(self.total_server_idle_time)
        server_count = len(self.servers)
        print "AGENTS AVG IDLE TIME="+str(self.total_server_idle_time/server_count)

        print "TIMES GREATER THAN 1 MIN:"
        wait_times_longer_than_min = []
        wait_times_longer_than_2mins = []
        wait_times_longer_than_3mins = []
        wait_times_longer_than_5mins = []
        for time in self.time_in_system:
            if time > 1.0:
              #  print time
                wait_times_longer_than_min.append(time)
            if time > 2.0:
                wait_times_longer_than_2mins.append(time)
            if time > 3.0:
                wait_times_longer_than_3mins.append(time)
            if time > 5.0:
                wait_times_longer_than_5mins.append(time)
        print "TOTAL WAIT TIMES LONGER THAN 1 MINUTE: " + str(len(wait_times_longer_than_min))
        print "TOTAL WAIT TIMES LONGER THAN 2 MINUTES: " + str(len(wait_times_longer_than_2mins))
        print "TOTAL WAIT TIMES LONGER THAN 3 MINUTES: " + str(len(wait_times_longer_than_3mins))
        print "TOTAL WAIT TIMES LONGER THAN 5 MINUTES: " + str(len(wait_times_longer_than_5mins))
        print "Percentage of Barista Customers who waited longer than 1 minute: " + str(float(float(len(wait_times_longer_than_min))/self.total_barista_customers_serviced))
        print "Percentage of Barista Customers who waited longer than 2 minutes: " + str(float(float(len(wait_times_longer_than_2mins))/self.total_barista_customers_serviced))
        print "Percentage of Barista Customers who waited longer than 3 minutes: " + str(float(float(len(wait_times_longer_than_3mins))/self.total_barista_customers_serviced))
        print "Percentage of Barista Customers who waited longer than 5 minutes: " + str(float(float(len(wait_times_longer_than_5mins))/self.total_barista_customers_serviced))
        print ""
