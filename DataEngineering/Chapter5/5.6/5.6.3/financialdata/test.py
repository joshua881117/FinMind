import os
import pandas as pd

from financialdata.backend.db import *
os.system("make run-celery-twse")
os.system("")
os.system("make run-celery-tpex")
