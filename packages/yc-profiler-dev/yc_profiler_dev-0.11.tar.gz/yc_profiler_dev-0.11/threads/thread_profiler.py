import sys
import traceback
import threading
import time
import json
import psutil
from commons.webclient import upload_json_data
from commons.common import  getKey, getServerUrl
from log.ycrash_logger import ycrash_logger

THREAD_DUMP_ENDPOINT = "/yc-receiver?dt=td"

def capture_thread_states():
    threads = {}
    # Capture states and stack traces of all threads
    for thread_id, frame in sys._current_frames().items():
        thread = get_thread_by_id(thread_id)
        # print_thread_attributes(thread)
        event = get_event(thread)
        proc = psutil.Process()

        # print(f"event {event}")
        threads[thread_id] = {
            'name': thread.name,
            'native_id': thread.native_id,
            'details': vars_to_string(thread),
            'cpu_percent':  get_threads_cpu_percent(proc,thread_id),
            'event': event,
            'state': get_thread_state(thread),
            'is_waiting': is_waiting_for_lock(frame),
            'stack_trace': traceback.format_stack(frame)
        }
    return threads


def vars_to_string(obj):
    values_str = ""
    for value in vars(obj).values():
        values_str += str(value) + " "
    return values_str


def get_event(thread):
    event_value = ""
    for obj in vars(thread).values():
        if type(obj) is threading.Event:
            print(event_value)
            event_value = event_value + vars_to_string(obj)
    return event_value


def print_thread_attributes(thread):
    thread_vars = vars(thread)
    for attr_name, attr_value in thread_vars.items():
        print(f"Attribute: {attr_name}, Type: {type(attr_value)}, Value: {attr_value}")


def is_waiting_for_lock(frame):
    stack_trace = traceback.format_stack(frame)
    for line in stack_trace:
        if '_wait_for_tstate_lock' in line:
            return True
    return False


def find_locks_held_by_thread(thread_id):
    locks = set()
    for obj in threading._active.values():
        if type(obj) is threading.Lock:
            # If the lock is owned by the specified thread, add it to the set of locks
            if obj._is_owned(thread_id):
                locks.add(obj)

    return locks


def get_thread_state(thread):
    if thread.is_alive():
        return "Alive"
    if thread.daemon:
        return "Dead (Daemon)"
    if thread.ident is None:
        return "New"
    return "UNKNOWN"


def get_thread_by_id(thread_id):
    for thread in threading.enumerate():
        if thread.ident == thread_id:
            return thread
    return None


def capture_export_thread_data(config):
    ycrash_logger.debug("Capturing thread dump...")
    threads = capture_thread_states()
    condition = threading.Condition()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    thread_events = []
    for thread_id, thread_info in threads.items():
        thread_data = {
            "event_type": "THREAD_DETAILS",
            "native_id": thread_info['native_id'],
            "id": thread_id,
            "name": thread_info['name'],
            "state": thread_info['state'],
            # "cpu_percent": thread_info['cpu_percent'],
            "waiting": thread_info['is_waiting'],
            # "details": thread_info['details'],
            "thread_event": thread_info['event'],
            "stack_trace": [line.strip() for line in thread_info['stack_trace']]
        }
        thread_events.append(thread_data)
        thread = {
                "timeStamp": current_time,
                "threads": [thread_events],  # Dictionary with threadevents list as a value
        }
        thread_json = json.dumps(thread, indent=4)

    ycrash_logger.debug("Uploading thread dump...")
    upload_json_data('application/json', getKey(config), getServerUrl(config,THREAD_DUMP_ENDPOINT), thread_json)


def get_locks_and_threads():
    lock_threads = {}
    for thread_id, thread in threading._active.items():
        for lock in threading._active[thread_id]._Thread__daemonic_locks:
            lock_id = id(lock)
            if lock_id not in lock_threads:
                lock_threads[lock_id] = []
            lock_threads[lock_id].append(thread)

    return lock_threads


def is_thread_blocked_or_waiting(thread):
    # Check if the thread is blocked on a lock
    for lock in threading._active_limbo_locks:
        if thread in lock._waiters:
            return True

    # Check if the thread is blocked on an event
    for event in threading._active_limbo_events:
        if thread in event._cond._waiters:
            return True

    # Add more checks for other synchronization primitives as needed...

    return False


def find_locks_held_by_threadold(thread_id):
    locks = []

    # Iterate through all objects in threading._active, which includes all thread objects
    for obj in threading._active.values():
        # Check if the object has a _is_owned() method (indicating it's a lock)
        if hasattr(obj, '_is_owned') and callable(obj._is_owned):
            # If the lock is owned by the specified thread, add it to the list of locks
            if obj._is_owned(thread_id):
                locks.append(obj)

    return locks


def get_threads_cpu_percent(p, thread_id, interval=0.1):
    total_percent = p.cpu_percent(interval)
    total_time = sum(p.cpu_times())
    cpu_percentage = 0
    for t in p.threads():
          if t.id == thread_id:
            cpu_percentage = total_percent * ((t.system_time + t.user_time) / total_time)
    return cpu_percentage
