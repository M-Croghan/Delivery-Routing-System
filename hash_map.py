# Hash Map Class

class HashMap:
    # Hash map constructor - Creates hash map & assigns an empty list to each bucket
    # Allows for the capacity of the map to be changed
    # Default set to 40 - The total # of packages to be handled for delivery
    def __init__(self, package_capacity=40):
        self.map = []
        for i in range(package_capacity):
            self.map.append([])

    # Inserts an item into the hash map
    # Time-Complexity - O(n)
    def insert(self, key, item):
        # Hashes the item & determines its appropriate bucket
        bucket = hash(key) % len(self.map)
        bucket_list = self.map[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches map based on the key provided
    # Returns item if found OR None if it does not exist / not found
    # Time-Complexity - O(n)
    def search(self, key):
        # Hashes the key to determine in which bucket it would be located
        bucket = hash(key) % len(self.map)
        bucket_list = self.map[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return print("NOT FOUND!")

    # Removes an item from the map if the pass in matches
    # Time-Complexity - O(n)
    def remove(self, key):
        # Hashes the key to determine in which bucket it would be located
        bucket = hash(key) % len(self.map)
        bucket_list = self.map[bucket]

        for key_value in bucket_list:
            if key_value == key:
                bucket_list.remove([key_value[0], key_value[1]])
