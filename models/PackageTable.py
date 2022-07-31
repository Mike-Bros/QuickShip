class PackageTable:
    """An abstract data structure that uses a chaining hash table to store package data

    """
    def __init__(self, initial_capacity=10):
        self.seperator = "********************************************************************************"
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert_or_update(self, key, value):
        """Insert a package into table or update existing entry

        :param key: The ID of the package to be added
        :type key: int
        :param value: The package object to be added
        :type value: models.Package
        :return: bool indicating success or failure of insert/update
        :rtype: bool
        """
        bucket = self.get_bucket(key)
        bucket_list = self.table[bucket]

        for item in bucket_list:
            if item[0] == key:
                item[1] = value
                return True

        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        """Search by package ID

        :param key: Package ID
        :type key: int
        :return: Package object or None if key does not exist
        :rtype: models.Package
        """
        bucket = self.get_bucket(key)
        # print("Looking for package key: " + str(key) + " in bucket: " + str(bucket))
        bucket_list = self.table[bucket]
        # print("Object in bucket: ", end='')
        # print(bucket_list)

        for key_value in bucket_list:
            # print("Key value = " + str(key_value))
            if key_value[0] == key:
                return key_value[1]  # return value of key found

        # If no key has been found at this point then key is not in table
        return None

    def remove(self, key):
        """Remove by package ID

        :param key: Package ID
        :type key: int
        """
        bucket = self.get_bucket(key)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])

    def print_table(self):
        """Helper function to print the current contents of the table

        Prints all buckets and their content displaying the package ID and Address for human readability

        """
        print(self.seperator)
        for i in range(len(self.table)):
            if self.table[i] != []:
                print("Bucket " + str(i) + ":", end=" ")
            else:
                print("Bucket " + str(i) + ":")

            for j in range(len(self.table[i])):
                package = self.table[i][j][1]
                package_representation = "Package: " + str(package.id) + ", " + package.address
                if j == len(self.table[i]) - 1:
                    print(package_representation)
                else:
                    print(package_representation, end=" || ")
        print(self.seperator)

    def get_bucket(self, item):
        """Helper function to get the bucket index of the given item

        :param item: Package ID
        :type item: int
        :return: Bucket Index
        :rtype: int
        """
        bucket = hash(item) % len(self.table)
        return bucket
