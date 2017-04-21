## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['URBasic', 'URConnect', 'URplus'],
    package_dir={'URBasic': 'URBasic',
                 'URConnect': 'URConnect',
                 'URplus': 'URplus'}
)

setup(**setup_args)
