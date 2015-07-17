try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python Eve Sample Deploy powered by IBM Bluemix',
    'author': 'Sanjay Joshi, ...',
    'url': 'http://macreduce.mybluemix.net',
    'author_email': 'joshisa@us.ibm.com',
    'version': '0.1',
    'install_requires': ['nose', 'eve', 'redis'],
    'packages': ['macreduce'],
    'scripts': [],
    'name': 'macreduce'
}

setup(**config)
