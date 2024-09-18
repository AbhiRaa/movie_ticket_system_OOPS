# Programming Fundamental Assignment 2
# Student Name: Abhinav
# Student Number: s3977487
# Highest Part attempted: HD LEVEL - part iii

from os import path
import sys

# Customer class that manages customer related functionalities
# Refernce: https://stackoverflow.com/questions/9585978/what-is-the-simplest-way-to-define-setter-and-getter-in-python?rq=4
class Customer:

    # Constructor for Customer class to initialise ID and name which are the unique attributes for a customer
    def __init__(self, ID, name):
        self.__ID = ID
        self.__name = name

    # Getter methods
    @property   
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    # Method which takes the ticket cost and returns 0, since a normal customer is not qualified for any discount
    def get_discount(self, cost):
        return 0

    # Method to return the booking fees, which is 2$ per ticket 
    def get_booking_fee(self, ticket_quantity):
        return 2 * ticket_quantity

    def display_info(self):
        print("Customer ID:", self.__ID)
        print("Customer Name:", self.__name)

# Reward Flat Customer class that manages customer that are in the rewards program and have a flat discount rate when purchasing tickets
# Inherits Customer class since every customer have ID and name in common
class RewardFlatCustomer(Customer):
    def __init__(self, ID, name, discount_rate=20):
        super().__init__(ID, name)
        self.__discount_rate = discount_rate
    
    # Method to get discount
    def get_discount(self, cost):
        return (self.__discount_rate) * cost
    
    # Getter method
    @property
    def discount_rate(self):
        return self.__discount_rate

    # Setter method
    @discount_rate.setter
    def discount_rate(self, discount_rate):
        self.__discount_rate = discount_rate

    def display_info(self):
        super().display_info()
        print("Discount Rate:", self.discount_rate)

# RewardStep customers are customers that are in the rewards program and have a different discount rate structure
# Inherits Customer class since every customer have ID and name in common
class RewardStepCustomer(Customer):
    def __init__(self, ID, name, discount_rate=30, threshold=50):
        super().__init__(ID, name)
        self.__discount_rate = discount_rate
        self.__threshold = threshold

    # Method to get discount
    def get_discount(self, cost):
        if cost > self.threshold:
            return (self.discount_rate) * cost
        else:
            return 0

    # Getter method
    @property   
    def discount_rate(self):
        return self.__discount_rate

    @property
    def threshold(self):
        return self.__threshold

    # Setter methods
    @discount_rate.setter
    def discount_rate(self, discount_rate):
        self.__discount_rate = discount_rate

    @threshold.setter
    def threshold(self, threshold):
        self.__threshold = threshold

    def display_info(self):
        super().display_info()
        print("Discount Rate:", self.discount_rate)
        print("Threshold:", self.threshold)

# Movie class is to keep track of information on different movies that the cinema offers
class Movie:
    def __init__(self, ID, name, seat_available):
        self.__ID = ID
        self.__name = name
        self.__seat_available = seat_available
    
    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name
    
    @property
    def seat_available(self):
        return self.__seat_available
    
    @seat_available.setter
    def seat_available(self, seat_available):
        self.__seat_available = seat_available

    def display_info(self):
        print("Movie ID:", self.__ID)
        print("Movie Name:", self.__name)
        print("Available Seats:", self.__seat_available)

# Ticket class is to keep track of information on different ticket types that the cinema offers
class Ticket:
    def __init__(self, ID, name, price):
        self.__ID = ID
        self.__name = name
        self.__price = price

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name
    
    @property
    def price(self):
        return self.__price

    def display_info(self):
        print("Ticket ID:", self.__ID)
        print("Name:", self.__name)
        print("Price:", self.__price)

# This class is to deal with group/combination of different ticket type purchases
class GroupTicket():
    def __init__(self, ID, name, components):
        self.__ID = ID
        self.__name = name
        self.__components = components

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def components(self):
        return self.__components

# Booking class to manage all bookings 
# Type Hinting: movie : Movie - we can use type hinting. Note, however, that this is not enforced, but guides you - and the IDE - into knowing if you're passing correct arguments or not.
class Booking:
    def __init__(self, customer, movie : Movie, ticket, quantity):
        self.customer = customer
        self.movie = movie
        self.ticket = ticket
        self.quantity = quantity

    # Method to calculate ticket cost, booking fee, discount amount and total quantity for bookings
    def compute_cost(self):
        self.ticket_cost = 0
        self.total_quantity = 0
        for index, type in enumerate(self.ticket):
            if isinstance(type, GroupTicket):
                total_component_quantity = 0
                total_component_price = 0
                for component, component_quantity in type.components:
                        total_component_price += component.price * component_quantity * self.quantity[index]
                        total_component_quantity += component_quantity
                self.total_quantity += self.quantity[index] * total_component_quantity
                # Managing 20% discount functionality in the group ticket types
                self.ticket_cost += total_component_price * 0.8
            else:
                self.total_quantity += self.quantity[index]
                self.ticket_cost += type.price * self.quantity[index]

        # Sum of all ticket types quantity entered 
        self.booking_fee = self.customer.get_booking_fee(self.total_quantity)
        self.discount = self.customer.get_discount(self.ticket_cost)
        self.total_cost = self.ticket_cost - self.discount + self.booking_fee
        return self.ticket_cost, self.booking_fee, round(self.discount,2), self.total_quantity

# Class Record is the central data repository
class Records:
    def __init__(self):
        self.customers : list[Customer]  = []
        self.movies : list[Movie] = [] 
        self.tickets : list[Ticket]  = []
        self.bookings : list[Booking] = []

    # Read method to read about customers from customer.txt and throws exception if file not found
    def read_customers(self, file_path = "customers.txt"):
        try:    
            with open(file_path, 'r') as file:
                for line in file:
                    # Getting each comma seprated value to store in the lists
                    customer_data = line.strip().split(',')
                    customer_id = customer_data[0].strip()
                    customer_name = customer_data[1].strip()
                    discount_value = float(customer_data[2].strip()) if len(customer_data) > 2 else None
                    threshold = float(customer_data[3].strip()) if len(customer_data) > 3 else None

                    if customer_id.startswith('C'):
                        customer = Customer(customer_id, customer_name)
                    elif customer_id.startswith('F'):
                        customer = RewardFlatCustomer(customer_id, customer_name, discount_value)
                    elif customer_id.startswith('S'):
                        customer = RewardStepCustomer(customer_id, customer_name, discount_value, threshold)
                    
                    self.customers.append(customer) 

        except FileNotFoundError:
            print(f"Error: File '{file_path}' is missing. Program is exiting...")
            quit()          

    # Read method to read about movies from movies.txt and throws exception if file not found
    def read_movies(self, file_path = "movies.txt"):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Getting each comma seprated value to store in the lists
                    movie_data = line.strip().split(',')
                    movie_id = movie_data[0].strip()
                    movie_name = movie_data[1].strip()
                    available_seat = int(movie_data[2].strip())

                    movie = Movie(movie_id, movie_name, available_seat)
                    self.movies.append(movie)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' is missing. Program is exiting...")
            quit()

    # Read method to read different ticket and group ticket types from tickets.txt and throws exception if file not found
    def read_tickets(self, file_path = "tickets.txt"):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Getting each comma seprated value to store in the lists
                    ticket_data = line.strip().split(',')
                    if ticket_data[0].startswith('T'):
                        ticket_id = ticket_data[0].strip()
                        ticket_name = ticket_data[1].strip()
                        ticket_unit_price = float(ticket_data[2].strip())

                        ticket = Ticket(ticket_id, ticket_name, ticket_unit_price)
                        self.tickets.append(ticket)
                    
                    elif ticket_data[0].startswith('G'):
                        ticket_id = ticket_data[0].strip()
                        ticket_name = ticket_data[1].strip()

                        # Retrieivng components which is List of tuples that stores normal ticket type and its quantity
                        # Main thing here is that we have to hop alternatively, to get all ticket-quantity pair
                        components = [(self.find_ticket(ticket_data[i].strip()), int(ticket_data[i + 1].strip())) for i in range(2, len(ticket_data), 2)]
                        
                        #Checking if the price <= 50$, condition for a valid group ticket otherwise throws exception 
                        price = 0
                        for ticket, quantity in components:
                            price += ticket.price * quantity
                        group_price = 0.8 * price
                        if group_price <= 50.0:
                            raise InvalidGroupTicketException(f"Group ticket {ticket_id} is not valid! The price of group ticket needs to be equal to or higher than 50$")

                        group_ticket = GroupTicket(ticket_id, ticket_name, components)
                        self.tickets.append(group_ticket)

        except (InvalidGroupTicketException) as e:
            print(str(e))
        except FileNotFoundError:
            print(f"Error: File '{file_path}' is missing. Program is exiting...")
            quit()
    
    # Read method to read bookings from bookings.txt and throws exception if file not found
    def read_bookings(self, file_path = "bookings.txt"):
        if not path.exists(file_path):
            print("Cannot load the booking file, running as if there is no previous booking file")
            return

        with open(file_path, 'r') as file:
            for line in file:
                booking_data = line.strip().split(',')
                customer_data = booking_data[0].strip()
                movie_data = booking_data[1].strip()
                ticket_data = [bd.strip() for bd in booking_data[2:-3:2]]  # Extract ticket type IDs or names
                quantity_data = [bd.strip() for bd in booking_data[3:-2:2]]  # Extract ticket quantities
                discount = float(booking_data[-3])
                booking_fee = float(booking_data[-2])
                total_cost = float(booking_data[-1])

                customer = self.find_customer(customer_data)
                movie = self.find_movie(movie_data)
                tickets = [self.find_ticket(ticket) for ticket in ticket_data]
                quantities = [int(quantity) for quantity in quantity_data]

                booking = Booking(customer, movie, tickets, quantities)
                booking.discount = discount
                booking.booking_fee = booking_fee
                booking.total_cost = total_cost

                self.bookings.append(booking)

    # Method to find customer form customers list from ID or name
    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.ID == search_value or customer.name == search_value:
                return customer     
        return None

    # Method to find movie form movies list from ID or name
    def find_movie(self, search_value):
        for movie in self.movies:
            if movie.ID == search_value or movie.name == search_value:
                return movie
        return None

    # Method to find ticket type form tickets list from ID or name
    def find_ticket(self, search_value):
        for ticket in self.tickets:
            if ticket.ID == search_value or ticket.name == search_value:
                return ticket
        return None

    # Display function to display all customers of all types and attributes 
    def display_customers(self):
        for customer in self.customers:
            if isinstance(customer, RewardFlatCustomer):
                print(f"Customer ID: {customer.ID}, Name: {customer.name}, Discount: {customer.discount_rate}")
            elif isinstance(customer, RewardStepCustomer):
                print(f"Customer ID: {customer.ID}, Name: {customer.name}, Discount: {customer.discount_rate}, Threshold: {customer.threshold}")
            elif isinstance(customer, Customer):
                print(f"Customer ID: {customer.ID}, Name: {customer.name}")

    # Display function to display all movies 
    def display_movies(self):
        for movie in self.movies:
            if isinstance(movie, Movie):
                print(f"Movie ID: {movie.ID}, Name: {movie.name}, Available Seats: {movie.seat_available}")

    # Display function to display all ticket types availble in the system 
    def display_tickets(self):
        for ticket in self.tickets:
            if isinstance(ticket, Ticket):
                print(f"Ticket ID: {ticket.ID}, Name: {ticket.name}, Unit Price: {ticket.price}")
            if isinstance(ticket, GroupTicket):
                price = 0
                for ticket_type, quantity in ticket.components:
                    price += ticket_type.price * quantity

                print(f"Ticket ID: {ticket.ID}, Name: {ticket.name}, Price: {round(0.8 * price, 1)}")

    # Display function to display all bookings availble in the system 
    def display_bookings(self):
        for booking in self.bookings:
            print("Customer:", booking.customer.name)
            print("Movie:", booking.movie.name)

            for index, ticket in enumerate(booking.ticket):
                if isinstance(ticket, GroupTicket):
                    print("Ticket Type: Group Ticket")
                    print(f"ID: {ticket.ID}, name: {ticket.name}, quantity: {booking.quantity[index]}")
                    for component, component_quantity in ticket.components:
                        print(f" - {component.name}: {component_quantity}")
                else:
                    print(f"Ticket Type: {ticket.name}")
                    print(f" - Quantity: {booking.quantity[index]}")

            print(f"Discount: {booking.discount}")
            print(f"Booking Fee: {booking.booking_fee}")
            print(f"Total Cost: {booking.total_cost}")
            print("-------------------------------------------")

    # Method to generate next unique customer id to store in the customers list in records
    def give_next_customer_id(self, customer_type):
        list_customer_type_IDs : list[int] = []
        for customer in self.customers:
            if customer.ID[0].lower() == customer_type:
                list_customer_type_IDs.append(int(customer.ID[1:]))

        if len(list_customer_type_IDs) > 0:
            return max(list_customer_type_IDs) + 1

    # Method to generate next unique movie id to store in the new added movie in movies list in records        
    def give_next_movie_id(self, prefix):
        list_movie_IDs : list[int] = []
        for movie in self.movies:
            if movie.ID[0] == prefix:
                list_movie_IDs.append(int(movie.ID[1:]))

        if len(list_movie_IDs) > 0:
            return max(list_movie_IDs) + 1

# All custom exceptions classes used in the program with description        
# Refernce: https://www.programiz.com/python-programming/user-defined-exception
class InvalidMovieException(Exception):
    "Raised when the movie entered by the user is not a valid movie or the movie is sold out (0 available seats)"
    pass

class InvalidTicketTypeException(Exception):
    "Raised when the ticket type entered by the user is not a valid ticket type"
    pass

class InvalidTicketQuantityException(Exception):
    "Raised when the ticket quantity is 0, negative, not an integer, or exceed the number of available seats."
    pass

class InvalidAnswerException(Exception):
    "Raised when the answer by the user is not y or n when asking if the customer wants to join the rewards program"
    pass

class InvalidRewardTypeException(Exception):
    "Raised when the answer by the user is not F or S when asking the type of the rewards program"
    pass

class InvalidDiscountRateException(Exception):
    "Raised when the discount rate by the user is 0, negative, not an integer."
    pass

class InvalidCustomerException(Exception):
    "Raised when the customer by the user is invalid or doesn't exists"
    pass

class InvalidGroupTicketException(Exception):
    "Raised when the Group ticket fetched group_price is less than 50$"
    pass

# Main class where all operations happen, a kind of user interface for the program
class Operations:
    def __init__(self):
        self.records = Records()

    # Function to display the menu
    def display_menu(self):
        print("----------- Welcome to the RMIT movie ticketing system! -----------")
        print("###################################################################")
        print("You can choose from the following options:")
        print("1. Purchase a ticket")
        print("2. Display existing customers' information")
        print("3. Display existing movies' information")
        print("4. Display existing ticket types' information")
        print("5. Add movies")
        print("6. Adjust the discount rate of all RewardFlat customers")
        print("7. Adjust the discount rate of a RewardStep customer")
        print("8. Display all Bookings")
        print("0. Exit the program")
        print("###################################################################")

    # Function to purchase ticket
    def purchase_ticket(self):
        
        # Display welcome message and ask for customer name 
        print("----------------Ticket Station----------------")
        # Assuming that a new customer will always enter a name in the system since they don't have any ID
        customer_entered = input("Hey there! Please enter your customer ID or name [e.g. Huong]:      ")

        # Ask for movie name
        movie = self.get_movie()
        available_seats = movie.seat_available

        # Ask for ticket types as comma seprated and checking that entered type is valid or not
        while True:
            try:
                ticket_types = input("Please enter the ticket types [enter a valid ticket type only, e.g. adult, child, senior, student, concession]:     ")
                ticket_types_list = ticket_types.split(',')
                
                # Remove leading/trailing whitespace from each value in the list
                refined_ticket_types_list = [value.strip() for value in ticket_types_list]
                is_ticket_type_valid = True
                ticket_type = []
                for type in refined_ticket_types_list:
                    searched_type = self.records.find_ticket(type)
                    if searched_type is None:
                        is_ticket_type_valid = False
                        raise InvalidTicketTypeException("Sorry, ticket type entered is not valid. Please enter valid type!")

                    ticket_type.append(searched_type)

                if is_ticket_type_valid:
                    break

            except(InvalidTicketTypeException) as e:
                print(str(e))

        # Ask for ticket quantities and validate them
        while True:
            try:
                ticket_quantity = input("Please enter the ticket quantities [enter a positive interger only, e.g. 1, 2, 3]:       ")
                ticket_quantity_list = ticket_quantity.split(',')

                # Remove leading/trailing whitespace from each value in the list
                refined_ticket_quantity_list = [int(value.strip()) for value in ticket_quantity_list]
                is_quantity_list_valid = True
                for quantity in refined_ticket_quantity_list:
                    # Checking that if length of both lists matches
                    if quantity <= 0 or quantity > available_seats or len(ticket_type) != len(refined_ticket_quantity_list):
                        is_quantity_list_valid = False
                        raise InvalidTicketQuantityException("Sorry, ticket quantity entered is not valid or excedes available seats. Please enter valid quantity!")

                if not is_quantity_list_valid:
                    continue

                # Sum of all ticket types quantity entered 
                total_quantity = sum(refined_ticket_quantity_list)

                if total_quantity > available_seats:
                    raise InvalidTicketQuantityException("Sorry, ticket quantities entered are more than available seats. Please enter valid quantity!")
                
                break

            except ValueError:
                print("Invalid quantity: please enter a positive integer number of quantity")
            except InvalidTicketQuantityException as e:
                print(str(e))

        # Checking if the customer exists or not in the Records 
        customer = self.records.find_customer(customer_entered)
        if customer is None:
            #Validate name for any digit and space
            is_name_valid = self.validate_name(customer_entered)
            while not is_name_valid:
                customer_entered = input("Invalid name! Please enter a valid name(without any digit and space):     ")
                is_name_valid = self.validate_name(customer_entered)
            
            customer = self.register_new_customer(customer_entered)
        
        # Create a booking for the requested movie order and compute cost
        booking = Booking(customer, movie, ticket_type, refined_ticket_quantity_list)
        ticket_cost, booking_fee, discount, final_total_quantity = booking.compute_cost()
        # Append in bookings list in rocords to maintain database
        self.records.bookings.append(booking)

        # Calculate total ticket cost, discount amount, and booking fee
        total_cost = ticket_cost - discount + booking_fee

        # Update available seats for the movie
        movie.seat_available = movie.seat_available - final_total_quantity

       # Display receipt to customer depending upon the booking
        print("######################################################")
        print("             Receipt of " + customer.name)
        print("######################################################")
        print("Movie :" + "                                      " + movie.name)
        for i in range(len(ticket_type)):
            print("Ticket type :" + "                                " + ticket_type[i].name)

            if isinstance(ticket_type[i], GroupTicket): 
                price = 0
                for type, quantity in ticket_type[i].components:
                    price += type.price * quantity
                
                print("Ticket unit price :" + "                         ", round(0.8 * price,1))
            else:     
                print("Ticket unit price :" + "                         ", ticket_type[i].price)

            print("Ticket quantity :" + "                           ", refined_ticket_quantity_list[i])
            print("                    ---------------                    ")
        print("######################################################")
        if discount != 0.0:
            print("Discount :" + "                                  ", discount)
        print("Booking fee :" + "                               ", booking_fee)
        print("Total cost :" + "                                ", total_cost)

    # Method to validate the name entered by new customer is valid or not that is should not include whitespaces or digits
    def validate_name(self, customer_name):
        for char in str(customer_name):
            if char.isdigit() or char.isspace():
                return False
        return True

    # Method to register a new customer in the system and ask if they want to join the rewards program
    def register_new_customer(self, customer_name):
        while True:
            reward_enroll = input("Hey, you are not in the rewards program. Would you like to join the rewards program [enter y or n]:      ")
            try:    
                if reward_enroll not in ['y', 'n']:
                        raise InvalidAnswerException("Sorry, invalid answer. Please enter 'y' or 'n'.")
                break
            except(InvalidAnswerException) as e:
                print(str(e))

        if reward_enroll == "y":

            while True:
                reward_type = input("What kind of Rewards customer wants? (enter F for RewardFlat, S for RewardStep):      ")
                try:
                    if reward_type not in ['F', 'S']:
                        raise InvalidRewardTypeException("Sorry, invalid rewards type. Please enter 'F' or 'S'.")
                    break
                except(InvalidRewardTypeException) as e:
                    print(str(e))

            if reward_type == "F":
                discount_rate = 0.2 # Default discount rate = 20%
                id = reward_type + str(self.records.give_next_customer_id(reward_type.lower()))
                customer = RewardFlatCustomer(id, customer_name, discount_rate)

            elif reward_type == "S":
                discount_rate = 0.3 # Default discount rate = 30%
                threshold = 50 # Default
                id = reward_type + str(self.records.give_next_customer_id(reward_type.lower()))
                customer = RewardStepCustomer(id, customer_name, discount_rate, threshold)

            else:
                print("Invalid rewards type!")

        else:
            reward_type = "C"
            id = reward_type + str(self.records.give_next_customer_id(reward_type.lower()))
            customer = Customer(id, customer_name)

        self.records.customers.append(customer)
        print("Customer", customer.name, "successfully registered.")
        return customer
    
    # Function to get the name of movie from the customer and valid that movie exists or not
    def get_movie(self):
        while True:
            try:
                movie_name = input("Please enter the ID or the name of the movie you are looking for [enter a valid name only, e.g. Avatar]:    ")
                movie = self.records.find_movie(movie_name)
                if movie is None:
                    raise InvalidMovieException("Sorry, movie is invalid. Please enter a valid movie!")
                # Check for seat availability
                if movie.seat_available <= 0:
                    raise InvalidMovieException("Sorry, the movie is sold out. Please enter another movie!")
                
                return movie

            except(InvalidMovieException) as e:
                print(str(e))

    # Function to add movies in the system
    def add_movies(self, movies_name_list):
        existing_movie = []
        for movie_name in movies_name_list:
            movie = self.records.find_movie(movie_name)
            if movie not in self.records.movies:
                # Adding new movie
                print(f"Adding the movie {movie_name} ...")
                movie_prefix = "M"
                id = movie_prefix + str(self.records.give_next_movie_id(movie_prefix))
                new_movie = Movie(id, movie_name, 50)
                self.records.movies.append(new_movie)
            else:
                print(f"The movie {movie_name} is an existing movie, will not do anything")
                existing_movie.append(movie.name)
        
        return existing_movie
    
    # Function to adjust discount rate of all Reward Flat customers or a Reward Step customer
    def adjust_discount_rate(self, prefix, discount_rate, customer_recieved):
        if prefix == "F":
            # Adjust discount rate of Reward Flat customers
            for customer in self.records.customers:
                if customer.ID[0] == prefix:
                    customer.discount_rate = discount_rate/100

        elif prefix == "S":
            # Adjust discount rate of a Reward Step customer
            for customer in self.records.customers:
                if customer.ID == customer_recieved.ID:
                    customer.discount_rate = discount_rate/100

    # Method to display customers from records
    def display_customers(self):
        self.records.display_customers()

    # Method to display movies from records
    def display_movies(self):
        self.records.display_movies()

    # Method to display ticket types from records
    def display_tickets(self):
        self.records.display_tickets()

    # Method to display bookings from records
    def display_bookings(self):
        self.records.display_bookings()

    # Method that drives the main menu of the program 
    def run(self, customers_file = "customers.txt", movies_file = "movies.txt", tickets_file = "tickets.txt", bookings_file = "bookings.txt"):
        # Loading all txt files in the system, if not found -> exception
        self.records.read_customers(customers_file)
        self.records.read_movies(movies_file)
        self.records.read_tickets(tickets_file)
        self.records.read_bookings(bookings_file)

        while True:
            self.display_menu()
            # Enter menu choice
            choice = input("Enter your choice (0-8): ")

            if choice == "1":
                self.purchase_ticket()

            elif choice == "2":
                self.display_customers()

            elif choice == "3":
                self.display_movies()

            elif choice == "4":
                self.display_tickets()

            elif choice == "5":
                requested_movies = input("Enter the movies you want to add separated by comma :     ")
                requested_movies_list = requested_movies.split(',')

                # Remove leading/trailing whitespace from each value in the list
                requested_movies_list = [value.strip() for value in requested_movies_list]

                # Call to add the entered list of movies
                existing_movies = self.add_movies(requested_movies_list)
                if existing_movies != []:
                    print("These movies already exists in the system :      ", existing_movies)

            elif choice == "6":
                customer_prefix = "F"
                while True: 
                    try:
                        discount_rate = float(input("Enter the discount rate you want to adjust for all reward step customer:     "))
                        if discount_rate <= 0.0:
                            raise InvalidDiscountRateException("Sorry, discount rate entered is negative or 0. Please try again.")
                        break
                    except ValueError:
                        print("Invalid discount rate. Please enter a positive number")
                    except(InvalidDiscountRateException) as e:
                        print(str(e))

                self.adjust_discount_rate(customer_prefix, discount_rate, None)
                print("Successfully updated the discount rate!")
                
            elif choice == "7":
                customer_prefix = "S"
                while True: 
                    try:
                        customer = input("Please enter name or ID of the reward step customer:      ")
                        searched_customer = self.records.find_customer(customer)
                        if searched_customer is None or searched_customer.ID[0] != customer_prefix: 
                                raise InvalidCustomerException("The customer entered doesn't exists or invalid in this category. Please enter again.")
                        break
                    except(InvalidCustomerException) as e:
                        print(str(e))
                
                while True: 
                    try:
                        discount_rate = float(input("Enter the discount rate you want to adjust for all reward step customer:     "))
                        if discount_rate <= 0.0:
                            raise InvalidDiscountRateException("Sorry, discount rate entered is negative or 0. Please try again.")
                        break
                    except ValueError:
                        print("Invalid discount rate. Please enter a positive number")
                    except(InvalidDiscountRateException) as e:
                        print(str(e))

                self.adjust_discount_rate(customer_prefix, discount_rate, searched_customer)
                print("Successfully updated the discount rate!")
            
            elif choice == "8":
                    self.display_bookings()

            elif choice == "0":
                print("Exiting the program...")
                break
            else:
                print("Invalid choice. Please try again.")
                
# Create an instance of Operations and run the program
# Command line display arguments
# Reference: https://realpython.com/python-command-line-arguments/
arguments = sys.argv
# Booking.txt not mandatory or customer, movie, ticket.txt all three or not at all
if len(arguments) == 5 or len(arguments) == 4 or len(arguments) == 1:
    operations = Operations()
    passing_arguments = arguments[1:]
    operations.run(*passing_arguments)
else:
    print("Invalid")

"""
    Analysis/Reflection:

The design of the program follows an object-oriented approach, where different classes are defined to represent different entities
such as customers, movies, tickets, and bookings. The program uses inheritance to define subclasses that inherit properties and methods
from their parent classes.

The Customer class serves as the base class for different types of customers, such as normal customers, reward flat customers, and reward
step customers. Each customer type has its own implementation of the get_discount method to calculate the discount based on the ticket 
cost. The RewardFlatCustomer and RewardStepCustomer classes also have additional attributes and methods specific to their reward types.

The Movie class represents a movie and stores information about its ID, name, and available seats. The Ticket class represents a ticket 
and stores information about its ID, name, and price. The GroupTicket class represents a group ticket that can include multiple components, 
of noramal ticket types each with its own quantity. The Records class manages the records of customers, movies, and tickets. It provides methods to read data from 
files, search for customers, movies, and tickets, and display their information.

The Booking class represents a booking made by a customer and calculates the total cost, booking fee, discount, and total quantity based on 
the selected tickets and quantities. The Operations class handles the main operations of the program, such as purchasing a ticket, 
displaying information, adding movies, and adjusting discount rates.

During the code development process, I started by designing the class structure and identifying the attributes and methods required for 
each class. I used type hinting to provide hints about the types of variables and return values for better readability and error checking. 
I also added exception classes to handle specific error conditions and provide meaningful error messages to the user.

One of the challenges I encountered during the code development was handling input validation and error checking. For example, validating 
the entered ticket types and quantities to ensure they are valid and within the appropriate range. I addressed this challenge by using 
try-except blocks and raising custom exceptions to handle specific error conditions and guide the user with appropriate error messages.

Overall, the design and development process involved careful consideration of the program's requirements, decomposition of the problem into 
manageable classes, and implementation of appropriate methods and error handling mechanisms.
"""
