import pandas as pd
#Convert to hitdumper format
columns = ['ophit_opch','pd_type','pds_box','sensible_to_vuv','sensible_to_vis','opdet_tpc','sampling','ophit_opdet_x','ophit_opdet_y','ophit_opdet_z']
pds_map = pd.read_json('pds_map_withcoords.json')
pds_map.columns = columns
pds_map['ophit_opdet'] = pds_map['ophit_opch']
pds_map.set_index('ophit_opch',inplace=True)

#Save to pickle and csv
pds_map.to_csv('PMT_ARAPUCA_info.csv')
