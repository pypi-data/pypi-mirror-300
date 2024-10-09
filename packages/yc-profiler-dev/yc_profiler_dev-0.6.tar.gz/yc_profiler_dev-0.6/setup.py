from setuptools import setup, find_packages

setup(
    name='yc-profiler-dev',
    version='0.6',
    packages=find_packages(include=['ycrash', 'threads', 'gcprofiler', 'heap', 'logger', 'memory', 'process', 'system']),
    description='yCrash Python Agent',
    install_requires=['pyyaml', 'requests', 'memory_profiler','psutil'],
    url='https://ycrash.io',
    author='yCrash Team',
    author_email='mahesh@tier1app.com'
)
