"""
    yCrash Python Profiler: Heap Dump Analyser
    This service responsible to extract and heap dumps upload to yCrash Server
    Dependency : Requries guppy module
"""

import tracemalloc
import json
from guppy import hpy
from commons.webclient import upload_json_data
from commons.common import  getKey, getServerUrl
from gcprofiler.gc_profiler import ycrash_profile
from log.ycrash_logger import ycrash_logger

HEAP_DUMP_ENDPOINT = "/cm-receiver+&dt=hd"

@ycrash_profile
class HeapDumpCapturer:
    def __init__(self):
        tracemalloc.start()

    """
    Captures heap dump in two formats and uploads to server
    """

    def capture_heap_dump(self, config):
       #print(f"YC Config:{config}")
       ycrash_logger.debug("Capturing heap dump...")

       heapDumpJson = {'heapDumpFormat1':
                        capture_heap_tracemalloc_dump(self),
                       'heapDumpFormat2':
                        f"\'{capture_heap_guppy_dump(self)}\'"
                        }
       ycrash_logger.debug("Uploading heap dump...")
       upload_json_data('application/json', getKey(config), getServerUrl(config,HEAP_DUMP_ENDPOINT), heapDumpJson)
       #print(f'uploaded json {heapDumpJson} with key {key}')

"""
    Captures heap tracemalloc dumps, providing a configured number of objects along with their references and sizes.
"""
def capture_heap_tracemalloc_dump(self, top_n=10):
        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics('lineno')

        # Convert stats to a list of dictionaries
        heap_dump = [{
            'filename': stat.traceback[0].filename,
            'lineno': stat.traceback[0].lineno,
            'sizeInBytes': stat.size,
            'noOfTimesCalled': stat.count
        } for stat in stats[:top_n]]

        heapDumpList = []
        for entry in heap_dump:
            heapDumpList.append(json.dumps(entry, indent=4))
        return heapDumpList

"""
    Captures heap dump with guppy with providing objects and sizes
"""
def capture_heap_guppy_dump(self):
    hp = hpy()
    heap: object = hp.heap()
    print(heap)
    return heap
