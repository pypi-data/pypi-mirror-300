import gcprofiler
import json
import gc

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []

def leakMemory():
    # Create circular references
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node1.next = node2
    node2.next = node3
    node3.next = node1  # Circular reference
    person1 = Person("Alice")
    person2 = Person("Bob")
    person1.friends.append(person2)
    person2.friends.append(person1)





    # Force garbage collection
    gc.collect()

    # Create a dictionary to store the leaked objects
    leaked_objects = []

    # Check for objects in gc.garbage
    if gc.garbage:
       for obj in gc.garbage:
           leaked_objects.append(repr(obj))

    # Store the leaked objects in a dictionary
    result = {"leaked_objects": leaked_objects}

    # Convert the dictionary to JSON format
    json_result = json.dumps(result, indent=4)

# Print the JSON result
    print(json_result)