import os
import pandas as pd

def load_csv_example(file_name):
    path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    return pd.read_csv(path)


def load_csv(file_name):
    
    return pd.read_csv(file_name)