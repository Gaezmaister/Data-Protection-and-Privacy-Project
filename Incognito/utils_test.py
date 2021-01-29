#!/usr/bin/env python3

from utils import *

import pandas as pd
data = pd.read_csv("./test_data/incognito_hospital_patient",header=0)

deidentified_data = remove_features(data, [0])
only_quasi_id = remove_features(data, [0,4])

print("[--] Original data:\n",data.values)
print("[--] Without identifier:\n",deidentified_data.values)
print("[--] Only quasi-identifier:\n",only_quasi_id.values)


print("[--] Num quasi-ids: {} \t {}".format(only_quasi_id.columns.values, len(only_quasi_id.columns.values)))
