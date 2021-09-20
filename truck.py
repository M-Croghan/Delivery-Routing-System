import datetime


# Establishes the Truck Class
class Truck:
    # Truck Constructor
    def __init__(self):
        self.capacity = 16
        self.avg_speed = 18.0
        self.cargo = []
        self.current_loc = '4001 S 700 East'
        self.mileage = 0
        self.time = datetime

    # Loads the 3 delivery trucks with the existing packages by using the hash map search function.
    # The assignment of the packages to the trucks themselves yields a time-complexity of O(1) as it is
    #  already known the quantity of the packages. However, the hash map search calls have a worst case of O(n).
    # map searching
    def load_trucks(self, truck1, truck2, truck3, hash):
        # 8:00AM Truck - First Out
        first_truck_cargo = [hash.search(1), hash.search(2), hash.search(4), hash.search(13), hash.search(14),
                             hash.search(15),
                             hash.search(16), hash.search(17), hash.search(19), hash.search(20), hash.search(29),
                             hash.search(30),
                             hash.search(10), hash.search(34), hash.search(37), hash.search(39)]

        # 9:20AM Truck - Second Out
        second_truck_cargo = [hash.search(3), hash.search(25), hash.search(6),
                              hash.search(31), hash.search(18), hash.search(22),
                              hash.search(5), hash.search(28), hash.search(32), hash.search(36), hash.search(38), hash.search(40)]

        # 10:30 Truck - Last Out
        last_truck_out = [hash.search(9), hash.search(23), hash.search(24), hash.search(26), hash.search(27), hash.search(21),
                          hash.search(33), hash.search(35), hash.search(7), hash.search(8), hash.search(11), hash.search(12)]

        organize_truck(first_truck_cargo, truck1)  # Organizes the 1st truck's cargo
        organize_truck(second_truck_cargo, truck2)  # Organizes the 2nd truck's cargo
        organize_truck(last_truck_out, truck3)  # Organizes the 3rd truck's cargo


# Takes in a truck and the packages onboard and organizes them based on priority. This was implemented as a way to
# incorporate a more advanced routing algorithm than the one used for this applications solution. It remains a part
# of the final version as a way to help think through future modifications.
# Time-Complexity - O(n)
def organize_truck(cargo_list, truck):
    route_priority = []
    for i in range(len(cargo_list)):
        if cargo_list[i].deadline != 'EOD':
            if cargo_list[i].deadline.startswith('9'):
                route_priority.insert(0, cargo_list[i])
            else:
                route_priority.append(cargo_list[i])
    for i in range(len(cargo_list)):
        if cargo_list[i].deadline == 'EOD':
            route_priority.append(cargo_list[i])

    truck.cargo = route_priority
