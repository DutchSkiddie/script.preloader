import os
import sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'resources', 'vendor')
lib_dir = os.path.join(parent_dir, 'resources', 'lib')

sys.path.append(vendor_dir)
sys.path.append(lib_dir)

from resources.lib import setup

if __name__ == '__main__':
    setup.init()
    exit()