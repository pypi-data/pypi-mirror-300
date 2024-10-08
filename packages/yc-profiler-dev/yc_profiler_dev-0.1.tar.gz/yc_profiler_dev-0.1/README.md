# README #

yCrash ycrash-python-agent profiles python applications capturing the system details

* Threads
* Heap
* GC
* Process
* Logs
* System Commands

### How to build and upload the module ###

1. Change the version in setup.py
2. To build 'python3.8 setup.py sdist'
3. To upload 'twine upload --verbose dist/*' ( Requires https://pypi.org/ account and setup )


### How to use ###
Just install using pip
1. Install ycrash profiler
pip install ycrash-profile-dev

2. Import the profiler in code
from ycrash import profiler

3. profiler.ycrash_init({absolutePathOfyCrashConfig})
Init the profiler with configuration file location as per 
https://docs.ycrash.io/ycrash-agent/launch-modes/m3-mode.html
   (we need have python documentation)
    




