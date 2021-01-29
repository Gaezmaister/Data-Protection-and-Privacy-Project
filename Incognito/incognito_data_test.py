#!/usr/bin/env python3

from incognito import *
from utils import *

import pandas as pd

data = pd.read_csv("./test_data/incognito_hospital_patient",header=0, dtype=str)

# Generalization Trees: birthdate, zipcode, sex

# birthdate
birthdate_tree = GeneralizationTreeNode("*/*/*")
birthdate_tree.add_son("*/*/*","*/*/76")
birthdate_tree.add_son("*/*/*","*/*/86")

birthdate_tree.add_son("*/*/76","*/21/76")
birthdate_tree.add_son("*/*/76","*/28/76")

birthdate_tree.add_son("*/28/76", "2/28/76")
birthdate_tree.add_son("*/28/76", "4/28/76")
birthdate_tree.add_son("*/21/76","1/21/76")
#birthdate_tree.add_son("*/*/*", "2/28/76")

#birthdate_tree.add_son("*/*/*", "4/28/76")
#birthdate_tree.add_son("*/*/*","1/21/76")
#birthdate_tree.add_son("*/*/*","4/13/86")

birthdate_tree.add_son("*/*/86","*/13/86")
birthdate_tree.add_son("*/13/86","4/13/86")

# zipcode
zipcode_tree = GeneralizationTreeNode("537**")
zipcode_tree.add_son("537**","5371*")
zipcode_tree.add_son("537**","5370*")

zipcode_tree.add_son("5371*","53715")
zipcode_tree.add_son("5371*","53710")

zipcode_tree.add_son("5370*","53706")
zipcode_tree.add_son("5370*","53703")

# sex
sex_tree = GeneralizationTreeNode("Person")
sex_tree.add_son("Person","Male")
sex_tree.add_son("Person","Female")

generalization_forest = {
'Birthdate' : birthdate_tree,
'Sex' : sex_tree,
'Zipcode' : zipcode_tree
}

incognito_algorithm = Incognito(generalization_forest)
kanonymous_data = incognito_algorithm(data, 2, [0,4])

print(kanonymous_data)
