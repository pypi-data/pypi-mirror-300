from setuptools import setup, find_packages

setup(
    name='yc-profiler-dev',
    version='0.9',
    packages=find_packages(exclude=['tests*']),
    description='yCrash Python Agent',
    install_requires=['pyyaml', 'requests', 'memory_profiler','psutil'],
    url='https://ycrash.io',
    author='yCrash Team',
    author_email='mahesh@tier1app.com'
)
