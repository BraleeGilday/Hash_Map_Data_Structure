# Author: Bralee Gilday
# Course: CS261 - Data Structures
# Assignment title: HashMap Part 2 (open addressing with quadratic probing)
# Date last modified: 6/6/24
# Description: Implementation of an optimized HashMap class that uses a
# dynamic array to store the hash table and Open Addressing with
# Quadratic Probing for collision resolution inside that dynamic array.
# The HashMap class incorporates methods for inserting, resizing, retrieving,
# checking, and removing key/value pairs, as well as clearing the hash map.
# It also includes the dunder methods __iter__() and __next__() to facilitate
# iteration through the HashMap. The table resizes when the load factor exceeds
# 0.5 to maintain performance. This implementation makes use of the pre-written
# DynamicArray and HashEntry classes in a6_include.py. The number of objects stored
# in the hash map will be between 0 and 1,000,000 inclusive. Additionally, two
# pre-written hash functions are provided in the skeleton code.


from DynamicArray_and_SinglyLinkedList import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
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
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
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
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY (pre-written by professor)
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Inserts an element in an open addressing-based hash table. Specifically,
        updates the key/value pair in the hash map. If the given key already
        exists in the hash map, its associated value is replaced with the new value.
        If the given key is not in the hash map, a new key/value pair must be added.

        When method is called, if the current load factor of the table is greater than
        or equal to 0.5, the table is resized to double its current capacity.

        :param key: The key associated with the value to be inserted or updated in the hash map.
        :param value: The value to be associated with the given key.

        :post-conditions: The key/value pair is added to the hash map, or the existing key's
            value is updated. If the load factor is >= 0.5, the hash map's capacity is increased
            and elements are rehashed.

        :complexity: Average case - O(1)
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # create HashEntry for the new key/value pair
        new_pair = HashEntry(key, value)

        # Use the hash function to compute an initial index for the element.
        initial_index = self._hash_function(key) % self._capacity
        addend = 1      # initial increment value for quadratic probing

        # starting at hashed index, iterate through the buckets until empty bucket found
        for bucket in range(self._capacity):
            # if the hash table array at initial_index is empty, insert the element there and stop
            current_hash_entry = self._buckets.get_at_index(initial_index)
            if current_hash_entry is None:
                self._buckets.set_at_index(initial_index, new_pair)
                self._size += 1
                return
            # or if the initial_index is a tombstone, insert the element there and stop
            elif current_hash_entry.is_tombstone is True:
                self._buckets.set_at_index(initial_index, new_pair)
                self._size += 1
                return

            # or if the key at initial_index matches the input key, then replace the value and stop
            elif current_hash_entry.key == key and current_hash_entry.is_tombstone is False:
                self._buckets.set_at_index(initial_index, new_pair)
                return

            # otherwise, compute the next index in the probing sequence and repeat
            else:
                # next index uses quadratic probing with wrap around
                initial_index = (initial_index + addend) % self._capacity
                addend += 2

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs are
        put into the new table, meaning all non-tombstone hash table links are rehashed.
        If new_capacity is valid, checks if it is a prime number; if not, this method
        changes the value to the next highest prime number.

        :validation: Checks that new_capacity is not less than the current number of elements
                     in the hash map; if so, the method does nothing.

        :param new_capacity: The new capacity for the hash table.

        :post-condition: The hash map's capacity is updated to the first prime number greater
                        than or equal to the input new_capacity. All existing key/value pairs
                        are rehashed into the new table with the updated capacity.

        :complexity: O(n)
        """
        # if new_capacity is not a positive integer,
        # or if new_capacity is less than self._size, immediately exit
        if new_capacity < 1 or new_capacity < self._size:
            return

        old_capacity = self._capacity
        old_hashmap = self._buckets

        # if new_capacity is not a prime number
        if self._is_prime(new_capacity) is False:
            # change it to the next highest prime number
            self._capacity = self._next_prime(new_capacity)

        else:
            self._capacity = new_capacity

        # create new array
        self._buckets = DynamicArray()
        for index in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

        # iterate through the old DynamicArray/HashMap
        for index in range(old_capacity):
            hash_entry = old_hashmap[index]
            # only put valid, non-tombstone key/value pairs into the new array
            if hash_entry is not None:
                if hash_entry.is_tombstone is False:
                    self.put(hash_entry.key, hash_entry.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor, which is the ratio
        of the number of elements in the hash table to the current
        capacity of the hash table.

        :return: the load factor (float value) of the current hash table.

        :complexity: O(1)
        """
        load_factor = self.get_size() / self.get_capacity()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: The number of empty buckets (as an integer) in the hash table.

        :complexity: O(n), where n is the capacity of the hash table.
        """
        empty = 0

        # iterate through the hash table looking for empty bucket or a tombstone
        for index in range(self._capacity):
            if self._buckets[index] is None:
                empty += 1
            elif self._buckets[index].is_tombstone:
                empty += 1

        return empty

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        :param key: The key whose associated value is to be returned.

        :return: The value associated with the given key, or None if the
        key is not in the hash map.

        :complexity: Average case - O(1)
        """
        initial_index = self._hash_function(key) % self._capacity
        addend = 1      # initial increment value for quadratic probing

        # Iterate through the hash table to find the key using quadratic probing
        while self._buckets[initial_index] is not None:
            current_hash_entry = self._buckets.get_at_index(initial_index)
            # if the key is found, and it's not a tombstone
            if current_hash_entry.key == key and current_hash_entry.is_tombstone is False:
                return current_hash_entry.value
            # if the key was not found at the current index
            else:
                # compute the next index in the quadratic probing sequence
                initial_index = (initial_index + addend) % self._capacity
                addend += 2

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.

        :param key: The key to check to see if it's in the hash map.

        :return: True if the key is in the hash map, False otherwise.

        :complexity: Average case - O(1)
        """
        initial_index = self._hash_function(key) % self._capacity
        addend = 1      # initial increment value for quadratic probing

        # start at hashed index and search for key until found or vacant spot is reached
        while self._buckets[initial_index] is not None:
            current_hash_entry = self._buckets.get_at_index(initial_index)
            # if the key is found at the current index, and it's not a tombstone
            if current_hash_entry.key == key and current_hash_entry.is_tombstone is False:
                return True
            # if the key was not found at the current index
            else:
                # compute the next index in the quadratic probing sequence
                initial_index = (initial_index + addend) % self._capacity
                addend += 2

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.

        :param key: The key for the key/value pair to be removed from the hash map.

        :post-conditions: The key, given it is actually in the hash map, and its associated
        value are removed from the hash table. If key is not in hash table, there is no change,

        :complexity: Average case - O(1)
        """
        initial_index = self._hash_function(key) % self._capacity
        addend = 1      # initial increment value for quadratic probing

        # iterate through hash table until key found or end of the hash table is reached
        while self._buckets[initial_index] is not None:
            current_hash_entry = self._buckets.get_at_index(initial_index)
            # check if the current hash entry is the key and is not a tombstone
            if current_hash_entry.key == key and current_hash_entry.is_tombstone is False:
                # key was found, so mark the entry as a tombstone and decrement the size
                current_hash_entry.is_tombstone = True
                self._size -= 1
                return

            # if the key was not found at the current index
            else:
                # move to the next index using quadratic probing
                initial_index = (initial_index + addend) % self._capacity
                addend += 2

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. The order of the keys in the dynamic array does not matter.

        :return: A DynamicArray containing tuples of key/value pairs from the hash map.

        :complexity: O(n), where n is the capacity of the hash table.
        """
        new_array = DynamicArray()

        # iterate through each bucket in the hash table
        for index in range(self._capacity):
            bucket = self._buckets[index]
            # if the bucket is not empty and not a tombstone
            if bucket is not None:
                if bucket.is_tombstone is False:
                    # add the key/value pair to the new dynamic array
                    key_value_pair = (bucket.key, bucket.value)
                    new_array.append(key_value_pair)

        return new_array

    def clear(self) -> None:
        """
        Clears the contents of the hash map.

        :post-conditions: All key/value pairs are removed form the hash map.
        The underlying hash table capacity remains unchanged.

        :complexity: O(n)
        """
        empty_array = DynamicArray()
        self._size = 0

        for index in range(self._capacity):
            empty_array.append(None)

        self._buckets = empty_array

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself. It initializes
        a variable to track the iterator’s progress through the hash map’s contents.

        :return: The hash map itself as an iterator.

        :complexity: O(1)
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next key/value pair in the hash map during iteration. If there are no more
        elements to iterate over, it raises StopIteration.

        :return: The next non-tombstone HashEntry in the hash map.

        :raises StopIteration: If there are no more elements to iterate over.
        """
        # a flag to indicate when the next valid entry is found
        found = 0
        try:
            while found == 0:
                current = self._buckets[self._index]
                # check if index has an HashEntry object
                if current is not None:
                    # then make sure the key is not a previously removed node
                    if current.is_tombstone is False:
                        found = 1
                value = self._buckets[self._index]
                # move to the next index for the next iteration
                self._index += 1
        except DynamicArrayException:
            raise StopIteration

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
