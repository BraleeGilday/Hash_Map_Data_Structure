# Hash_Map_Data_Structure
Python implementation of a HashMap data structure in two forms: using Separate Chaining and via Open Addressing with Quadratic Probing.

Neither hash map implementation utilizes ANY built-in Python data structures and/or their methods. Therefore, the DynamicArray_and_SinglyLinkedList.py file needs included; this file was written by an Oregon State University professor and are the data structures intened to be used for this project. 

## Hash Map using Seperate Chaining
The file hash_map_oa.py contains the implementation of an optimized HashMap class that uses a dynamic array to store the hash table and chaining for collision resolution with singly linked lists. The HashMap class includes methods for inserting, resizing, retrieving, checking, and removing key/value pairs, as well as clearing the hash map. The table resizes when the load factor exceeds 1.0 to maintain performance. The class also includes a standalone function, find_mode, which determines the mode(s) and their frequency in a given dynamic array. The implementation can handle between 0 and 1,000,000 elements reliably. As noted in the docstrings, there are several pre-written hash functions which ensure efficient key indexing.

## Hash Map using Open Addressing with Quadratic Probing
The file hash_map_sc.py contains the implementation of an optimized HashMap class that uses a dynamic array to store the hash table and Open Addressing with Quadratic Probing for collision resolution inside that dynamic array. The HashMap class incorporates methods for inserting, resizing, retrieving, checking, and removing key/value pairs, as well as clearing the hash map. It also includes the dunder methods __iter__() and __next__() to facilitate iteration through the HashMap. The table resizes when the load factor exceeds 0.5 to maintain performance. This implementation makes use of the pre-written DynamicArray and HashEntry classes in DynamicArray_and_SinglyLinkedList.py. The number of objects stored in the hash map will be between 0 and 1,000,000 inclusive.

### Project Status
This project is currently complete.

### License
This project is licensed under the MIT License. See the LICENSE file for more information.

### Contact
Bralee Gilday - www.linkedin.com/in/bralee-gilday
