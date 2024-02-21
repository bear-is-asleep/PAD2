#Boilerplate
import pandas as pd

def switch_channels(df, i, j):
    #Save to a copy
    df_copy = df.copy()
    
    # Store channels i and j
    channel_i = df_copy.loc[i].copy()
    channel_j = df_copy.loc[j].copy()

    # Switch all columns except the ones to keep fixed
    columns_to_switch = ['ophit_opdet_x','ophit_opdet_y','ophit_opdet_z',]
    df_copy.loc[i, columns_to_switch] = channel_j[columns_to_switch]
    df_copy.loc[j, columns_to_switch] = channel_i[columns_to_switch]
    return df_copy


#Create a map of the channels
op = pd.read_csv('PMT_ARAPUCA_info.csv')
#TPC 0
switch_channels(op,6,36).to_csv('PMT_ARAPUCA_info_6_36.csv') #coated to uncoated same box - edge
switch_channels(op,16,40).to_csv('PMT_ARAPUCA_info_16_40.csv') #coated to uncoated same box - edge
switch_channels(op,6,88).to_csv('PMT_ARAPUCA_info_6_88.csv') #coated to coated different box (but close) - edge
switch_channels(op,16,88).to_csv('PMT_ARAPUCA_info_16_88.csv') #coated to coated different box (but close) - edge
switch_channels(op,16,10).to_csv('PMT_ARAPUCA_info_16_10.csv') #coated to coated different box (but close) - edge
switch_channels(op,6,8).to_csv('PMT_ARAPUCA_info_6_8.csv') #coated to coated same box - edge
switch_channels(op,90,164).to_csv('PMT_ARAPUCA_info_90_164.csv') #coated to coated different box (but close) - center
switch_channels(op,90,194).to_csv('PMT_ARAPUCA_info_90_194.csv') #coated to uncoated different box (but close) - center
switch_channels(op,116,194).to_csv('PMT_ARAPUCA_info_116_194.csv') #uncoated to uncoated different box (but close) - center

#TPC 1
switch_channels(op,7,37).to_csv('PMT_ARAPUCA_info_7_37.csv') #coated to uncoated same box - edge
switch_channels(op,17,41).to_csv('PMT_ARAPUCA_info_17_41.csv') #coated to uncoated same box - edge
switch_channels(op,7,89).to_csv('PMT_ARAPUCA_info_7_89.csv') #coated to coated different box (but close) - edge
switch_channels(op,17,89).to_csv('PMT_ARAPUCA_info_17_89.csv') #coated to coated different box (but close) - edge
switch_channels(op,17,11).to_csv('PMT_ARAPUCA_info_17_11.csv') #coated to coated different box (but close) - edge
switch_channels(op,7,9).to_csv('PMT_ARAPUCA_info_7_9.csv') #coated to coated same box - edge
switch_channels(op,91,165).to_csv('PMT_ARAPUCA_info_91_165.csv') #coated to coated different box (but close) - center
switch_channels(op,91,195).to_csv('PMT_ARAPUCA_info_91_195.csv') #coated to uncoated different box (but close) - center
switch_channels(op,117,195).to_csv('PMT_ARAPUCA_info_117_195.csv') #uncoated to uncoated different box (but close) - center

#Different tpcs
switch_channels(op,6,7).to_csv('PMT_ARAPUCA_info_6_7.csv') #coated to coated different tpcs (same location) - edge
switch_channels(op,6,37).to_csv('PMT_ARAPUCA_info_6_37.csv') #coated to uncoated different tpcs - edge
switch_channels(op,90,165).to_csv('PMT_ARAPUCA_info_90_165.csv') #coated to coated different box, different tpc (but close) - center
switch_channels(op,90,195).to_csv('PMT_ARAPUCA_info_90_195.csv') #coated to uncoated different box, different tpc (but close) - center