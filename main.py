import datetime

from package import id_search, format_package_details
from parse_data import get_package_data, get_distance_data, get_address_data, find_distance
from truck import Truck

# Creates 3 Delivery Trucks and sets their designated departure times, which will be updated during delivery.
t1 = Truck()
t1.time = datetime.timedelta(hours=8, minutes=00, seconds=00)
t2 = Truck()
t2.time = datetime.timedelta(hours=9, minutes=30, seconds=00)
t3 = Truck()
t3.time = datetime.timedelta(hours=10, minutes=30, seconds=00)

# Sets the departure time for each delivery truck to use as a reference for scheduling.
first_truck = datetime.timedelta(hours=8, minutes=00, seconds=00)
second_truck = datetime.timedelta(hours=9, minutes=30, seconds=00)
third_truck = datetime.timedelta(hours=10, minutes=30, seconds=00)

# Parses package data from .csv to create packages to deliver.
find_packages = get_package_data()
# Parses distance data from .csv to assemble an adjacency matrix.
find_coordinates = get_distance_data()
# Parses location data from .csv to determine delivery addresses.
find_addresses = get_address_data()
# Creates a delivery log to hold package information after successful delivery.
delivered = []

# Loads and organizes each truck with packages.
Truck().load_trucks(t1, t2, t3, find_packages)


# Main algorithm for the application. Applies a nearest neighbor approach to determine the next delivery address.
# The supplemental write up document included with this submission has more detailed pseudo code.
# The algorithm mimics a graph-like representation using an adjacency list to hold distances (edges) that can be
# looked up based on the index of the address data (vertices). Worst case Time-Complexity - O(n^2)
def start_delivery(truck):
    while len(truck.cargo) != 0:
        max_d = 50
        cargo_item = 0
        nextstop = ''
        # Checks for address change constraints & updates package information if found
        for i in range(len(truck.cargo)):
            if truck.time.__gt__(datetime.timedelta(hours=10, minutes=20, seconds=00)) and truck.cargo[i].ID == 9:
                truck.cargo[i].update_package('410 S State St', 'Salt Lake City', 'UT', '84111',
                                              'Address Updated @ 10:20AM')
        # Checks for packages with deadline constraints and prioritizes delivery
        for i in range(len(truck.cargo)):
            if truck.cargo[i].deadline == datetime.timedelta(hours=10, minutes=30, seconds=00):
                max_d = find_distance(truck.current_loc, truck.cargo[i].address)
                nextstop = truck.cargo[i].address
                cargo_item = truck.cargo[i]
            # Finds the closest address and prioritizes it as the next stop
            else:
                if find_distance(truck.current_loc, truck.cargo[i].address) < max_d:
                    max_d = find_distance(truck.current_loc, truck.cargo[i].address)
                    nextstop = truck.cargo[i].address
                    cargo_item = truck.cargo[i]
        # Once the closest address has been identified: tracks change of time & truck mileage. Update package status
        # and delivery log. If the truck has no more packages to deliver, sets the final destination to the main hub
        # address updating the final time and mileage.
        updatetime = float(max_d) / float(truck.avg_speed)
        truck.time = truck.time + datetime.timedelta(hours=updatetime)
        cargo_item.time = truck.time
        cargo_item.location = 'DELIVERED'
        delivered.append(cargo_item)
        truck.cargo.remove(cargo_item)
        truck.current_loc = nextstop
        truck.mileage += max_d
        if len(truck.cargo) == 0:
            returnhome = find_distance(truck.current_loc, '4001 S 700 East')
            truck.mileage += returnhome
            updatetime = float(returnhome) / float(truck.avg_speed)
            truck.time = truck.time + datetime.timedelta(hours=updatetime)


# Executes the main algorithm and delivery of packages for each truck.
start_delivery(t1)
start_delivery(t2)
start_delivery(t3)

# Records the total mileage as the sum that each truck traveled.
total_mileage = t1.mileage + t2.mileage + t3.mileage


# Provides search functionality for looking up the delivery status of ALL PACKAGES based on time.
# Time complexity - O(n)
def status_by_time(time):
    ts = time.split(':')
    parsed_time = datetime.timedelta(hours=int(ts[0]), minutes=int(ts[1]), seconds=int(ts[2]))

    for i in range(len(delivered)):
        if parsed_time.__lt__(first_truck):
            delivered[i].delivery_status('AT HUB', parsed_time)
        if first_truck.__lt__(parsed_time) and parsed_time.__lt__(second_truck):
            if delivered[i].time.__lt__(parsed_time):
                continue
            elif parsed_time.__lt__(delivered[i].time) and delivered[i].time.__lt__(second_truck):
                delivered[i].delivery_status('EN ROUTE', parsed_time)
            else:
                delivered[i].delivery_status('AT HUB', parsed_time)

        if second_truck.__lt__(parsed_time) and parsed_time.__lt__(t1.time):
            if delivered[i].time.__lt__(parsed_time):
                continue
            elif parsed_time.__lt__(delivered[i].time) and delivered[i].time.__lt__(t1.time):
                delivered[i].delivery_status('EN ROUTE', parsed_time)
            else:
                delivered[i].delivery_status('AT HUB', parsed_time)

        if t1.time.__lt__(parsed_time) and parsed_time.__lt__(third_truck):
            if delivered[i].time.__lt__(parsed_time):
                continue
            elif parsed_time.__lt__(delivered[i].time) and delivered[i].time.__lt__(third_truck):
                delivered[i].delivery_status('EN ROUTE', parsed_time)
            else:
                delivered[i].delivery_status('AT HUB', parsed_time)

        if third_truck.__lt__(parsed_time) and parsed_time.__lt__(t3.time):
            if delivered[i].time.__lt__(parsed_time):
                continue
            elif parsed_time.__lt__(delivered[i].time) and delivered[i].time.__lt__(t3.time):
                delivered[i].delivery_status('EN ROUTE', parsed_time)

    for i in range(len(delivered)):
        print(
            '{:<15} {:<45} {:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(delivered[i].ID,
                                                                                    delivered[i].address,
                                                                                    delivered[i].city,
                                                                                    delivered[i].state,
                                                                                    delivered[i].zip,
                                                                                    delivered[i].weight,
                                                                                    delivered[i].deadline,
                                                                                    delivered[i].location,
                                                                                    str(delivered[i].time)))


# Main console display for a supervisor to view and interact with.
# Has the ability to view ALL packages & offers various search functionality.
print()
print('<<<<<<< WELCOME TO THE WGUPS DELIVERY MANAGEMENT SYSTEM >>>>>>>')
print('-------------------------------------------------------')
print('---------------- DELIVERY STATISTICS ------------------')
print('-------------------------------------------------------')
print(
    'TOTAL MILEAGE: {} || Truck 1 Mileage: {:0.1f} || Truck 2 Mileage: {} || Truck 3 Mileage: {}'.format(total_mileage,
                                                                                                         # Displays the TOTAL mileage & mileage for each truck
                                                                                                         t1.mileage,
                                                                                                         t2.mileage,
                                                                                                         t3.mileage))
print('-------------------------------------------------------')
print('START & END TIMES || TRUCK 1: [{} / {}] || TRUCK 2: [{} / {}] || TRUCK 3: [{} / {}]'.format(first_truck, t1.time,
                                                                                                   # Displays the start & end times overall & for each truck
                                                                                                   second_truck,
                                                                                                   t2.time,
                                                                                                   third_truck,
                                                                                                   t3.time))
print('-------------------------------------------------------')
print('-------------------------------------------------------')
print('PACKAGES HANDLED: {} ||| PACKAGES DELIVERED: {}'.format(len(find_packages.map),
                                                               len(delivered)))  # Displays the total number of packages parsed in & total number delivered
print('-------------------------------------------------------')
print('-------------------------------------------------------')
print(' What would you like to do? Please enter a selection from the menu below:')
user_start = input('1 - Display status of ALL packages at end of day...\n'
                   '2 - Display status of ALL packages at a SPECIFIC TIME...\n'
                   '3 - Display information of a SPECIFIC PACKAGE...\n'
                   '`Exit` - Close the application\n').lower()

while user_start != 'exit':
    if user_start == '1':  # Menu Choice 1 - displays status if all packages at the end of the day - Time Complexity O(n)
        print('PACKAGE ID'.ljust(15), 'ADDRESS'.ljust(45), 'CITY'.ljust(20), 'STATE'.ljust(15), 'ZIP'.ljust(15),
              'DEADLINE'.ljust(15), 'STATUS'.ljust(15), 'DELIVERY TIME'.ljust(15))
        for i in range(len(delivered)):
            format_package_details(delivered[i])
        break
    elif user_start == '2':  # Menu Choice 2 - displays all package statuses based on a specific time. - Time Complexity (n)
        time_choice = input(
            'Please enter a time in HH:MM:SS format...\n Type `Exit` to close the application\n').lower()
        if time_choice == 'exit':
            break
        else:
            try:
                status_by_time(time_choice)
                pass
                break
            except ValueError:
                print('Invalid Input! Please try again!')
                pass
    elif user_start == '3':  # Menu Choice 3 - displays package based on package ID - Time Complexity O(n)
        package_search = input('Please enter Package ID:\nOr type `Exit` to close application\n').lower()
        if 1 <= int(package_search) <= 40:
            id_search(package_search, delivered)
            break
        elif package_search == 'exit':
            break
        else:
            print('No Package Found')
            break
    else:
        print('Invalid Input. Please try again.')
        break
