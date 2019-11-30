"""Read Saved Pickle Measurements"""

import pickle


# Read file
with open('data.pkl', 'rb') as f:
  data_in = pickle.load(f)

print(data_in)
