# ----------in terminal-------------------
# python setup.py py2app (product)
# python setup.py py2app -A (for testing)
# ----------------------------------------
from setuptools import setup

APP = ['detect-general.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'numpy'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
