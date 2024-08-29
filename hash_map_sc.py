# Name: Bralee Gilday
# OSU Email: gildayb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment 6: HashMap Part 1 (chaining for collision resolution)
# Due Date: 6/6/24
# Description: Implementation of an optimized HashMap class that uses a dynamic array
# to store the hash table and chaining for collision resolution with singly linked lists.
# The HashMap class includes methods for inserting, resizing, retrieving, checking,
# and removing key/value pairs, as well as clearing the hash map. The table resizes
# when the load factor exceeds 1.0 to maintain performance. The class also includes a
# standalone function, find_mode, which determines the mode(s) and their frequency in a
# given dynamic array. Pre-written hash functions ensure efficient key indexing, and the
# implementation can handle between 0 and 1,000,000 elements reliably.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value is replaced with the new value. If the given
        key is not in the hash map, a new key/value pair is added.

        If the current load factor of the table is greater than or equal to 1.0 when this
        method is called, the table is resized to the first prime number greater than or
        equal to double its current capacity.

        :param key: The key associated with the value to be inserted or updated in the hash map.
        :param value: The value to be associated with the given key.

        :pre-conditions: DynamicArray class must be implemented.

        :post-conditions: The key/value pair is added to the hash map, or the existing key's
            value is updated. If the load factor is >= 1.0, the hash map's capacity is increased
            and elements are rehashed.

        :complexity: Average case - O(1)
        """
        # if the load factor is greater than or equal to 1.0, then resize to double the capacity
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # calculate the bucket index using the hashfunction- O(1)
        bucket_index = self._hash_function(key) % self.get_capacity()
        # save the linked_list at the hashed index
        bucket = self._buckets.get_at_index(bucket_index)

        # check if the key already exists in the LinkedList- O(1) on average since the load
        # factor is maintained at a reasonable level (less than 1.0) with resizing
        node = bucket.contains(key)
        # if the key is already in the LinkedList
        if node is not None:
            # update the value stored at that node; size stays the same
            node.value = value
        # if the key is not in the LinkedList
        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs
        are put into the new table (hash table links are rehashed).

        If the specified new capacity is less than 1, this method does nothing.
        Otherwise, it adjusts the capacity to the next prime number greater
        than or equal to the given new capacity.

        If the load factor of the hash table is greater than 1 when this method is called,
        it continues to resize the table until the load factor is less than or equal to 1.

        :param new_capacity: The desired new capacity for the hash table.

        :post-conditions: The capacity of the hash table is updated, and all
                          existing key-value pairs are rehashed.

        :complexity: O(n)
        """
        # first check that new_capacity is not less than 1; if so, the method does nothing.
        if new_capacity < 1:
            return

        # If new_capacity is 1 or more, make sure it is a prime number.
        # If not, change it to the next highest prime number.
        if self._is_prime(new_capacity) is False:
            self._capacity = self._next_prime(new_capacity)

        else:
            self._capacity = new_capacity

        # continuously resize if the load factor is greater than 1
        while self.table_load() > 1:
            self._capacity = self._next_prime(self._capacity * 2)

        # create a new array
        new_array = DynamicArray()

        # each bucket is an empty linked list
        for index in range(self._capacity):
            new_array.append(LinkedList())

        # Rehash all key/value pairs into the new table
        for index in range(self._buckets.length()):
            linked_list = self._buckets.get_at_index(index)
            # iterate through the nodes of the linkedlist (if there are any)
            for node in linked_list:
                # calculate the new index of the node (based on new capacity)
                new_index = self._hash_function(node.key) % self._capacity
                new_bucket = new_array.get_at_index(new_index)      # the new linked_list
                # hash the node into the correct linkedlist in the new array
                new_bucket.insert(node.key, node.value)

        # reassign the HashMap to the newly created DynamicArray
        self._buckets = new_array

    def table_load(self) -> float:
        """
        Computes and returns the current load factor of the hash table.

        The load factor is defined as the number of elements (key-value pairs)
        in the hash table divided by the total number of buckets (the table's capacity).

        :return: The load factor (float value) of the current hash table.

        :complexity: O(1)
        """
        load_factor = self.get_size()/self.get_capacity()

        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        :return: The number of empty buckets in the hash table.

        :complexity: O(n)
        """
        # iterate through each bucket and count how many contain no active key-value pairs
        empty = 0
        for bucket in range(self._capacity):
            linked_list = self._buckets.get_at_index(bucket)
            if linked_list.length() == 0:
                empty += 1

        return empty

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.

        :param key: The key whose associated value is to be returned.

        :returns: The value associated with the given key, or None if the key is not found.

        :complexity: Average case - O(1)
        """
        # calculate the bucket index using the hash function
        index = self._hash_function(key) % self._capacity

        # retrieve the linked list at the computed index
        linked_list = self._buckets.get_at_index(index)

        # search for the key in the linked list - O(n) where n is the length of linked list
        # this should be efficient on average due to the load factor management
        node = linked_list.contains(key)

        # if the key is not found
        if node is None:
            return None

        # if the key is found, return the associated value
        return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.

        :param key: The key to be checked in the hash map.

        :return: True if the key is found in the hash map, False otherwise.

        :complexity: Average case - O(1)
        """
        index = self._hash_function(key) % self._capacity

        linked_list = self._buckets.get_at_index(index)

        node = linked_list.contains(key)

        if node is None:
            return False

        return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.

        :param key: The key to be removed from the hash map.

        :post-conditions: If the key is found and removed, the size of the hash map is
        decremented. Otherwise, if the key is not found, the hash map remains unchanged.

        :complexity: Average case - O(1)
        """
        index = self._hash_function(key) % self._capacity

        linked_list = self._buckets.get_at_index(index)

        # attempt to remove the key from the linked list
        # if the key is found and removed, the remove method returns True
        if linked_list.remove(key) is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map.

        :return: DynamicArray containing tuples of key/value pairs from the hash map.

        :complexity: O(n). Although we iterate over all buckets and, within each bucket,
                    iterate over all elements in the linked list, the complexity remains linear.
                    This is because the load factor is maintained below 1.0, and therefore
                    the average length of each linked list is kept short.
        """
        new_array = DynamicArray()

        # iterate through the hash table searching for valid key/value pairs
        # the for loops are working *together* to iterate over the n elements in HashMap
        for bucket in range(self._capacity):
            linked_list = self._buckets.get_at_index(bucket)
            for node in linked_list:
                key_value_pair = (node.key, node.value)
                new_array.append(key_value_pair)

        return new_array

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.

        :post-conditions: All key/value pairs in the hash map are removed.
                          The size of the hash map is set to 0.

        :complexity: O(n)
        """
        empty_array = DynamicArray()

        # each bucket is an empty linked list
        for index in range(self._capacity):
            empty_array.append(LinkedList())

        self._buckets = empty_array
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    A standalone function that receives a dynamic array, which is not guaranteed to be sorted.
    This function returns a tuple containing, in this order, a dynamic array comprising the
    mode (most occurring) value(s) of the given array, and an integer representing the highest
    frequency of occurrence for the mode value(s). If there is more than one value with the highest
    frequency, all values at that frequency are included in the array being returned.

    :pre-conditions: The input array should contain at least one element and all values
                     stored in the array should be strings.

    :return: A tuple (DynamicArray, int) where the first element is a dynamic array of mode value(s)
            and the second element is the highest frequency of occurrence for these mode value(s).

    :complexity: O(n)
    """
    # initialize a new hash map to store frequency counts- O(1)
    map = HashMap(da.length())

    # create a frequency table with the values from the dynamic array- O(n)
    for index in range(da.length()):
        value = da[index]                    # O(1)
        if map.contains_key(value):          # O(1) average
            count = map.get(value) + 1       # O(1) average
            map.put(str(value), count)       # O(1) average

        else:
            map.put(str(value), 1)

    # find mode(s)
    mode_values = DynamicArray()
    highest_frequency = 1        # assume there will be at least one element

    # call get_keys_and_values to generate list of key/value pairs- O(n)
    key_value_pairs = map.get_keys_and_values()

    # iterate through key/value pairs to find the mode(s)- O(n)
    for index in range(key_value_pairs.length()):
        current_frequency = key_value_pairs[index][1]
        # if the current value has the highest frequency so far
        if current_frequency > highest_frequency:
            # clear the array and add the new mode
            mode_values = DynamicArray()
            current_key = key_value_pairs[index][0]
            mode_values.append(current_key)
            # update highest frequency
            highest_frequency = current_frequency
        # if the current value frequency matches the highest frequency
        elif current_frequency == highest_frequency:
            current_key = key_value_pairs[index][0]
            # add it to the list of modes
            mode_values.append(current_key)

    return mode_values, highest_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - from Gradescope resize example A")
    print("----------------------")
    m = HashMap(11, hash_function_2)

    # Manually insert the specified key-value pairs into the hash map
    m.put("key380", 35)
    m.put("key651", 679)
    m.put("key16", 33)
    m.put("key221", 600)
    m.put("key539", -683)
    m.put("key93", 137)

    print("Before resizing:")
    print(m)
    print(f"Capacity: {m.get_capacity()}, Size: {m.get_size()}")

    # Resize the table to the new capacity
    m.resize_table(1)

    print("\nAfter resizing:")
    print(f"Capacity: {m.get_capacity()}, Size: {m.get_size()}")
    print(m)
    print("\nExpected: ")
    print("\nCapacity: 7, Size: 6")


    print("\nPDF - from Gradescope resize example B")
    print("----------------------")
    # Initialize HashMap with a given capacity and hash function
    m = HashMap(47, hash_function_2)

    # Manually insert the specified key-value pairs into the hash map
    m.put("key220", -349)
    m.put("key211", -727)
    m.put("key410", -443)
    m.put("key501", -408)
    m.put("key250", 690)
    m.put("key601", -611)
    m.put("key252", -277)
    m.put("key171", 475)
    m.put("key219", 368)
    m.put("key543", 730)
    m.put("key148", -246)
    m.put("key752", -247)
    m.put("key464", -670)
    m.put("key906", -770)
    m.put("key493", 249)
    m.put("key467", 80)
    m.put("key197", 907)
    m.put("key963", 754)
    m.put("key459", 651)
    m.put("key882", 607)
    m.put("key747", 831)
    m.put("key919", 201)
    m.put("key768", 724)
    m.put("key876", 925)

    print("Before resizing:")
    print(m)
    print(f"Capacity: {m.get_capacity()}, Size: {m.get_size()}")

    # Resize the table to the new capacity
    m.resize_table(1)

    print("\nAfter resizing:")
    print(f"Capacity: {m.get_capacity()}, Size: {m.get_size()}")
    print("\nExpected: ")
    print("Capacity: 37, Size: 24")

#     print("\nPDF - put example 1")
#     print("-------------------")
#     m = HashMap(53, hash_function_1)
#     for i in range(150):
#         m.put('str' + str(i), i * 100)
#         if i % 25 == 24:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
#
#     print("\nPDF - put example 2")
#     print("-------------------")
#     m = HashMap(41, hash_function_2)
#     for i in range(50):
#         m.put('str' + str(i // 3), i * 100)
#         if i % 10 == 9:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
#
#     print("\nPDF - resize example 1")
#     print("----------------------")
#     m = HashMap(20, hash_function_1)
#     m.put('key1', 10)
#     print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
#     m.resize_table(30)
#     print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
