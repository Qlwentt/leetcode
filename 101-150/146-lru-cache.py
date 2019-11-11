""""
STATEMENT
Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following operations: get and put.

get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.

The cache is initialized with a positive capacity.

Follow up:
Could you do both operations in O(1) time complexity?

CLARIFICATIONS
- any space restraints? No, go for broke
- what data types for the keys/values do I need to support? ints

EXAMPLES
LRUCache cache = new LRUCache( 2 /* capacity */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // returns 1
cache.put(3, 3);    // evicts key 2
cache.get(2);       // returns -1 (not found)
cache.put(4, 4);    // evicts key 1
cache.get(1);       // returns -1 (not found)
cache.get(3);       // returns 3
cache.get(4);       // returns 4

ALGORITHM/COMMENTS
- we need insert and retrieval both at O(1). A dictionary can retrieve at O(1) and a linked list can insert at the beginning at  O(1)
- since we have unlimited space, let's combine both data structures to optimize time
- we will create a dictionary where the key is the LRUcache key and the value is a node for a linked list
- the node will contain the key and value for the LRUCache key-value pair
- because we have unlimited memory, the node will have a reference to its previous node in addition to its next node to make deletion easier (doubly linked list)
- we will also be able to easily insert nodes at either the beginning or the end with a doubly linked list

- on insert
- if key already exists in dictionary, copy node, insert node to front of list, remove from current position 
- otherwise add the item at the end of the linked list
- if current size of list == capcacity, eject the first item from the list

- on get
- if key doesn't exist, return - 1
- refresh: copy node, insert to end of list, remove from current position
- return value of node
"""

class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
        

class LRUCache(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        # why am I doing this?
        self.head.next = self.tail
        self.tail.prev = self.head
        # why??
    
    def put(self, key, value):
        # if get != -1
        # --remove
        # add
        # if capacity has been reached, eject first item
        
        
        if key in self.storage:
            node = self.storage[key]
            self._remove(node)
        node = Node(key, value)
        self._add(node)
        self.storage[key] = node

        if len(self.storage) > self.capacity:
            ejected_node = self.head.next
            self._remove(ejected_node)
            del self.storage[ejected_node.key]
        
        
        
    def get(self, key):
        if not key in self.storage:
            return -1
        # remove from current position
        node = self.storage[key]
        self._remove(node)
        # add to end
        self._add(node)
        return node.value
    
    def _remove(self, node):
        # update pointers
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add(self, node):
        # update pointers
        # its previous is head
        # head's next is new node
        tail_prev = self.tail.prev
        node.prev = tail_prev
        tail_prev.next = node
        node.next = self.tail
        self.tail.prev = node