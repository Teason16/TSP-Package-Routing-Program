# Hash table class that uses chaining
# Citing source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py

class ChainingHashTable:
    # constructor with default capacity parameter
    # assigns all buckets with an empty list
    def __init__(self, initial_capacity=25):
        # initialize hash table with empty bucket list entries
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # insert item into hash table or update item in hash table
    def insert(self, key, value):
        # get bucket where item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update item if already in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
                return True

        # insert new item at the end of the bucket list
        key_value = [key, value]
        bucket_list.append(key_value)
        return True

    # search for item by key
    def search(self, key):
        # get bucket location where key would be found
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for key in bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

