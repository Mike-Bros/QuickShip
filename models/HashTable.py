class HashTable:
    def __init__(self, initial_capacity=10):
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
                return key_value[1] #return value of key found
            else:
                return None

    def remove(self, key):
        bucket = self.get_bucket(key)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0],key_value[1]])

    def print_table(self):
        for i in range(len(self.table)):
            if self.table[i] != []:
                print("Bucket " + str(i) + ":", end=" ")
            else:
                print("Bucket " + str(i) + ":")

            for j in range(len(self.table[i])):
                if j == len(self.table[i])-1:
                    print(str(self.table[i][j]))
                else:
                    print(str(self.table[i][j]), end=", ")

    def get_bucket(self, item):
        bucket = self.my_hash(item) % len(self.table)
        return bucket

    def my_hash(self, item):
        # todo
        return hash(item)
