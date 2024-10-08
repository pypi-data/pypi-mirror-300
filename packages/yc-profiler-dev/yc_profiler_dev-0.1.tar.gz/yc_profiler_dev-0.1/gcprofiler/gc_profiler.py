"""
    yCrash Python Profiler:GC/Mem Profiler
    This service responsible extracting and uplading the GC and memory data to yCrash server
"""

from memory_profiler import memory_usage
import types
import json
from commons.webclient import upload_json_data
from commons.common import getKey, getServerUrl
import gc
import inspect
import re
from collections import Counter
import sys

GC_DUMP_ENDPOINT = "/cm-receiver+&dt=gc"


"""
   The func retrieved and uploads GC stats, details and leaked objects to the yCrash server
"""
def ycrash_memory_extract(config):
    mem_usage = memory_usage()[0]
    gc_counts = getCounts(gc.get_count())
    gc_count_data = {
        "young": gc_counts[0],
        "middle": gc_counts[1],
        "old": gc_counts[2]
    }

    gc_threshold = getCounts(gc.get_threshold())
    gc_threshold_data = {
        "young": gc_threshold[0],
        "middle": gc_threshold[1],
        "old": gc_threshold[2]
    }

    stats = gc.get_stats()
    gc_stats_data = {
        "young": stats[0],
        "middle": stats[1],
        "old": stats[2]
    }

    stats = gc.get_stats()
    topObjects = getTopObjects()
    gc_stats = {"gc_top_objects": topObjects}

    leaked_objects = []

    # Check for objects in gc.garbage
    if gc.garbage:
        for obj in gc.garbage:
            leaked_objects.append(repr(obj))

    freeze_count = gc.get_freeze_count()

    print(stats)
    data = {"memory_usage": mem_usage,
            "gc": {"gc_counts": gc_count_data, "gc_threshold": gc_threshold_data, "gc_stats": gc_stats_data,
                   'gc_top_objects': topObjects, "leaked_objects": leaked_objects, "freeze_count": freeze_count}}

    # Get a list of all objects tracked by the garbage collector
    # Create a dictionary to store the leaked objects

    gc.get_freeze_count()

    memory_json = json.dumps(data, indent=4)
    upload_json_data('application/json', getKey(config),
                     getServerUrl(config, GC_DUMP_ENDPOINT), memory_json)

"""
   Retrieves and returns the top objects 
"""

def getTopObjects():
    objects = gc.get_objects()

    # Extract class names of objects and count occurrences
    class_names = [obj.__class__.__name__ for obj in objects]
    class_counts = Counter(class_names)

    # Sort the Counter by counts in descending order and limit to top 10
    top_10_classes = class_counts.most_common(30)

    # Create a list of dictionaries
    result_list = [{"class_name": name, "count": count} for name, count in top_10_classes]

    # Convert the list to JSON
    json_data = json.dumps(result_list)
    return json_data


def getCounts(gc_counts):
    counts_str = str(gc_counts)
    # Use regular expression to extract numbers
    counts = tuple(map(int, re.findall(r'\d+', counts_str)))
    return counts


"""
    Decorates a function to captures  memory stats
"""
def ycrash_profile_memory(func):
    def wrapper(*args, **kwargs):
        mem_usage_start = memory_usage()[0]
        result = func(*args, **kwargs)
        mem_usage_end = memory_usage()[0]
        mem_usage_diff = mem_usage_end - mem_usage_start

        print(f"Memory usage for {func.__name__}: {mem_usage_diff} MB")
        return result

    return wrapper


"""
    Finds all methods in the current modules
"""
def find_all_modules():
    for module_name, module_obj in sys.modules.items():
        print(f"*** module is {module_name} {module_obj}")
        profile_global_functions(module_obj)
        profile_classes(module_obj)


def profile_global_functions(module):
    for name, func in module.__dict__.items():
        if callable(func) and not name.startswith('__') and not name.startswith('ycrash_profile'):
            setattr(module, name, ycrash_profile_memory(func))
    return module

"""
    Decorates all class in a module for capturing memory usage
"""
def profile_classes(module):
    for name, obj in vars(module).items():
        if inspect.isclass(obj):
            # Decorate each method in the class
            for method_name, method in vars(obj).items():
                if callable(method):
                    setattr(obj, method_name, ycrash_profile_memory(method))

"""
    Decorates all methods in class in a module for capturing memory usage
"""
# Annotate the functions with their types
def ycrash_profile(cls):
    for name, method in vars(cls).items():
        if isinstance(method, types.FunctionType):
            setattr(cls, name, ycrash_profile_memory(method))
    return cls

"""
    Decorates all methods in class in a current application for capturing memory usage
"""
def profile_all_methods():
    # Get all functions defined in the current module
    current_module = __import__(__name__)
    functions = [obj for name, obj in current_module.__dict__.items() if isinstance(obj, types.FunctionType)]

    # Apply ycrash_profile_memory decorator to each function
    for func in functions:
        setattr(current_module, func.__name__, ycrash_profile_memory(func))
