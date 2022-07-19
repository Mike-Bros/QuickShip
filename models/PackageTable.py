class PackageTable:
    """An abstract data structure that uses a chaining hash table to store package data

    """
    def __init__(self, initial_capacity=10):
        self.seperator = "********************************************************************************"
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert_or_update(self, key, value):
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
        bucket = self.get_bucket(key)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]  # return value of key found
            else:
                return None

    def remove(self, key):
        bucket = self.get_bucket(key)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])

    def print_table(self):
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
        bucket = hash(item) % len(self.table)
        return bucket
