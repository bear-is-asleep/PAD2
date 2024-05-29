import os
import numpy as np

def get_random_map():
    """
    Get a random map from the maps folder
    """
    maps = os.listdir('maps')
    maps = [f for f in maps if f.endswith('.csv')] #filter to only maps
    return 'maps/'+maps[np.random.randint(len(maps))]

#Coating dictionary
COATING_MAP = {
  -1 : 'Undefined',
  0 : 'Coated (VUV) PMT',
  1 : 'Uncoated (VIS) PMT',
  2 : 'Coated (VUV) XA',
  3 : 'Uncoated (VIS) XA'
}

MUON_TYPES = {
  0 : 'anode-cathode crosser',
  1 : 'anode-piercer',
  2 : 'cathode-piercer',
  3 : 'top-bottom crosser',
  4 : 'up-downstream crosser',
  5 : 'other'
}
                