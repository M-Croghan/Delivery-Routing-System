from datetime import datetime


# Establishes the Package class
class Package:
    # Package constructor
    def __init__(self, ID, address, city, state, zip, deadline, weight, notes):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.location = ''
        self.time = datetime

    # returns package attributes
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s " % (self.ID, self.address, self.city, self.state, self.zip,
                                                            self.deadline, self.weight, self.notes, self.location,
                                                            self.time)

    # Allows for a package to be updated with critical information while en-route / out for delivery.
    # Time-Complexity - O(1)
    def update_package(self, address, city, state, zip, notes):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.notes = notes

    # Returns delivery information about a package including both location and delivery time.
    # Time-Complexity - O(1)
    def delivery_status(self, location, time):
        self.location = location
        self.time = time


# Formats package delivery details for output in the main console window.
# Time-Complexity - O(1)
def format_package_details(packageinfo):
    print('{:<15} {:<45} {:<20} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(packageinfo.ID, packageinfo.address,
                                                                           packageinfo.city,
                                                                           packageinfo.state, packageinfo.zip,
                                                                           packageinfo.deadline,
                                                                           packageinfo.location,
                                                                           str(packageinfo.time)))


# Allows for a package to be searched through the main console window.
# Time-Complexity - O(n)
def id_search(search, pack_list):
    print('PACKAGE ID'.ljust(15), 'ADDRESS'.ljust(45), 'CITY'.ljust(20), 'STATE'.ljust(15), 'ZIP'.ljust(15),
          'WEIGHT'.ljust(15),
          'DEADLINE'.ljust(15), 'STATUS'.ljust(15), 'DELIVERY TIME'.ljust(15))
    for i in range(len(pack_list)):
        if int(search) == pack_list[i].ID:
            print(
                '{:<15} {:<45} {:<20} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}'.format(pack_list[i].ID,
                                                                                        pack_list[i].address,
                                                                                        pack_list[i].city,
                                                                                        pack_list[i].state,
                                                                                        pack_list[i].zip,
                                                                                        pack_list[i].weight,
                                                                                        pack_list[i].deadline,
                                                                                        pack_list[i].location,
                                                                                        str(pack_list[i].time)))
