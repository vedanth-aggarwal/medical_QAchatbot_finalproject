import os
from pathlib import Path 
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')

list_of_files = [
    'src/__init__.py',
    'src/helper.py',
    'src/prompt.py',
    '.env',
    'setup.py',
    'research/trials.ipynb',
    'app.py',
    'store_index.py',
    'static/.gitkeep',
    'templates/chat.html',
    'test.py'
]


for filepath in list_of_files:
    filepath = Path(filepath) # convert to windows format
    filedir,filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f'Creating directory - {filedir} for file - {filename}')

    if (not os.path.exists(filepath)) or (os.path.getsize(filename)):
        with open(filepath,'w') as f:
            pass
            logging.info(f'Creating empty file - {filepath}')
    else:
        logging.info(f'{filename} already exists!')