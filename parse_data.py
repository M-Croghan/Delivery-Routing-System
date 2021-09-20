import csv

from hash_map import HashMap
from package import Package


# Reads the package information from .csv file, creates package objects, and inserts them into the hashmap
# Time-Complexity - O(n)
def get_package_data():
    hashmap = HashMap()
    with open('data_files/package_data.csv', encoding='utf-8') as csvfile:
        packageData = csv.reader(csvfile, delimiter=',')
        next(packageData)
        for row in packageData:
            ID = int(row[0])
            address = row[1].replace('South', 'S')
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            packageInfo = Package(ID, address, city, state, zip, deadline, weight, notes)  # Package Object

            hashmap.insert(ID, packageInfo)  # Inserts package into hash map
        return hashmap


# Creates an adjacency list to be used to hold distance data between delivery addresses
# Reads distance data from .csv and inserts it into the adjacency list
# Time-Complexity - O(n)
def get_distance_data():
    adj_list = [[0] * 27 for i in range(27)]  # Adjacency list creation
    with open('data_files/distance_data.csv', encoding='utf-8-sig') as csvfile:
        distance = csv.reader(csvfile, delimiter=',')
        location = -1
        for row in distance:
            location = location + 1
            for i in range(len(row)):
                if row[i] != '':
                    adj_list[location][i] = adj_list[i][location] = float(row[i])
        return adj_list


# Reads address data from .csv and populates a list for look up to determine the distance between locations.
# Time-Complexity - O(n)
def get_address_data():
    addresses = []
    with open('data_files/address_data.csv', encoding='utf-8-sig') as csvfile:
        address = csv.reader(csvfile, delimiter=',')
        for row in address:
            pid = row[0]
            name = row[1]
            address = row[2].replace('South', 'S')
            addresses.append([pid, name, address])
        return addresses


# Retrieves a location index from address data to be used in distance calculation.
# Time-Complexity - O(n)
def get_location_index(loc):
    location = get_address_data()
    for i in range(len(location)):
        if loc in location[i][2]:
            return int(location[i][0])


# Uses an two index locations to determine the distance between the current & next address.
# Time-Complexity - O(n) | Calls get_location_index function which iterates a list of addresses
def find_distance(current, end):
    coords = get_distance_data()
    start = int(get_location_index(current))
    stop = int(get_location_index(end))
    return coords[start][stop]


