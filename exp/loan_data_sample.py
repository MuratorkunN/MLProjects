import pandas as pd

# df = pd.read_pkl

import pickle
import numpy as np

# with open("loan_data_sample.pkl", "rb") as f:
#   df = pickle.load(f)

# print(type(df))

import pickletools

# Change this to your file's path
filename = "loan_data_sample.pkl"

with open(filename, "rb") as f:
    pickletools.dis(f)