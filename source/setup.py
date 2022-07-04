from distutils.core import setup
import py2exe, os
import pymunk

pymunk_dir = os.path.dirname(pymunk.__file__)

setup(windows=['bregma.py'],
      data_files = [os.path.join(pymunk_dir, 'chipmunk.dll')],
      options={
                "py2exe":{
                        "bundle_files": 3
                }
        }
)

