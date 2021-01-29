import pandas as pd

def remove_features(data: pd.DataFrame, idxlist: list):
    if idxlist is None or len(idxlist) ==0:
        return data
    return data.drop([data.columns[i] for i in idxlist], axis='columns')
