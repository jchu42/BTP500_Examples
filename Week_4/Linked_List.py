'''
Here we have a full fledged linked list implementation.
Sentinel nodes and everything!
'''

# A class representing a single node in the Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
    def display(self):
        print(f"{self.data}", end="")
        if self.next:
            print("->", end="")

# Useful for edge cases!
class SentinelNode:
    def __init__(self):
        self.next = None

# Iterator Class
class ListIterator:
    def __init__(self, linked_list):
        self.current = linked_list.start # hehehe

    def __iter__(self):
        return self

    def __next__(self):
        self.current = self.current.next
        if self.current == None:
            raise StopIteration
        return self.current

class LinkedList:
    def __init__(self):
        self.start = SentinelNode() 
        self.end = SentinelNode()
    
    def is_empty(self):
        return self.start.next == None

    def push(self, data):
        '''Insert an element at the beginning of the list.'''
        new_node = Node(data)
        new_node.next = self.start.next
        if self.is_empty():
            self.end.next = new_node
        self.start.next = new_node

    def append(self, data):
        '''Insert an element at the end of the list.'''
        '''Insert an element at the end of the list.'''
        new_node = Node(data)
        if not self.start.next:
            self.start.next = new_node
        if self.end.next:
            self.end.next.next = new_node
        self.end.next = new_node

    def pop(self):
        '''Remove the element from the beginning of the list.'''
        if not self.start.next:
            return None
        popped_node = self.start.next
        self.start.next = popped_node.next
        if self.start.next == None:
            self.end.next = None
        return popped_node.data

    def search(self, key):
        '''Search for an element in the list. Linear search'''
        current = self.start.next
        flag = False
        while current and not flag:
            if current.data == key:
                flag = True
            current = current.next
        return flag
    
    def remove(self, element):
        '''Removes a specified element.'''
        current = self.start.next
        prev = None
        found = False
        while current and not found:
            if current.data == element:
                found = True
            else:
                prev = current
                current = current.next
        if found:
            prev.next = current.next
            return current
        return None

    def display(self):
        '''Display the elements in the list.'''
        for data in iter(self):
            data.display()
        print()
    
    # Iter is short for iterator
    def __iter__(self):
        return ListIterator(self)

if __name__ == "__main__":
    # Create a linked list (please don't name your variables
    # as poorly as I do mine)
    ll = LinkedList()
    
    # Push a few elements
    ll.push(10)
    ll.push(20)
    ll.push(30)

    print("After pushing elements:")
    ll.display()

    # Append some more elements
    ll.append(40)
    ll.append(50)

    print("After appending elements:")
    ll.display()

    # Pop the last element
    popped = ll.pop()
    print(f"Popped element: {popped}") # f string formatting hooray
    
    print("After popping an element:")
    ll.display()

    # Search for 40
    found = ll.search(40)
    print(f"Element 40 found: {found}") 

    removed = ll.remove(40)
    print(f"Element 40 removed:")
    ll.display()

    not_found = ll.search(100)
    print(f"Element 100 found: {not_found}")

    # Using an iterator
    print("Iterating through the list:")
    for value in ll:
        value.display()
    print()

    print ("After removing all elements from the list:")
    for value in ll:
        ll.pop()
    ll.display()