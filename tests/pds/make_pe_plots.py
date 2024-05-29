import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
sys.path.append('../..')
from Loader import Loader
from utils import plotters

PMT_ARA_NAME = '../../maps/PMT_ARAPUCA_info.csv'
HDRKEYS = ['run','subrun','event']
MAX_ENTRIES = 100 #Max number of entries to load
MODE = 'op'
DATA_DIR = '/exp/sbnd/data/users/brindenc/PDS_ml/pgun_single/data' #Waveforms and hitdumper location
#DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/test_fcl/v9'
bins = [np.arange(190,290,2),np.arange(100,2000,50)]
labels = ['Coated','Uncoated']

#Get files
files = os.listdir(DATA_DIR)
files = [f for f in files if '.root' in f and 'hitdumper' in f]

for fname in tqdm(files):
    #Clear variables
    coated = None
    uncoated = None
    ts = None
    l = None
    weights = None
    
    #Load hitdumper to get op_df
    l = Loader(
        data_dir=DATA_DIR,
        hdump_name=fname, 
        software_name=None, 
        wfm_name=None, 
        load_muon=False,
        load_crt=False,
        load_mcpart=False,
        mode=MODE,
        hdrkeys=HDRKEYS, 
        pmt_ara_name=PMT_ARA_NAME, 
        filter_primaries=False,
        max_entries=MAX_ENTRIES
    )
    #Get pmts
    coated = l.op_df[l.op_df['ophit_opdet_type'] == 1]
    uncoated = l.op_df[l.op_df['ophit_opdet_type'] == 2]

    #Setup plotting variables
    ts = [coated['ophit_peakT'].values*1e3,uncoated['ophit_peakT'].values*1e3]
    weights = [coated['ophit_pe'].values,uncoated['ophit_pe'].values]
    
    #Make plots
    for i,b in enumerate(bins):
        for use_log in [False,True]:
            if i == 0:
                savename = fname.strip('.root')
                foldername = f'plots_prompt_{plotters.day}'
            elif i == 1:
                savename = fname.strip('.root')
                foldername = f'plots_full_{plotters.day}'
                
            #Plot PE vs PeakT
            fig,ax = plt.subplots()
            ax.hist(ts,weights=weights,bins=b,label=labels,histtype='step',lw=3)
            ax.set_xlabel('PeakT (ns)')
            ax.set_ylabel('PE')
            ax.legend()
            if use_log:
                ax.set_yscale('log')
                savename += '_logy'
            ax.set_title(fname.strip('.root'))
            plotters.set_style(ax)
            plotters.save_plot(savename,fig,folder_name=foldername)
            plt.close(fig)
            plt.close('all')
            
            #Hist of PeakT
            savename+= '_peakT'
            fig,ax = plt.subplots()
            ax.hist(ts,bins=b,label=labels,histtype='step',lw=3)
            ax.set_xlabel('PeakT (ns)')
            ax.set_ylabel('Entries')
            ax.legend()
            if use_log:
                ax.set_yscale('log')
            ax.set_title(fname.strip('.root'))
            plotters.set_style(ax)
            plotters.save_plot(savename,fig,folder_name=foldername)
            plt.close(fig)
            plt.close('all')
            
            
            

