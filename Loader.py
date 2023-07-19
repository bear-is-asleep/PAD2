import uproot
import pandas as pd
from variables import *
from config.test import *
from PMT import PMT
from time import time
import numpy as np
from utils.helpers import convert_edges_to_centers

class Loader:
    def __init__(self,data_dir,pad_dir,hdump_name,wfm_name=None,load_muon=False,
                 load_crt=False,save_dir=None,use_op=True):
        """Loads and stores trees

        Args:
            data_dir (_type_): _description_
            pad_dir (_type_): _description_
            hdump_name (_type_): _description_
            wfm_name (_type_, optional): _description_. Defaults to None.
            save_dir (_type_, optional): _description_. Defaults to None.
            use_op (bool, optional): _description_. Defaults to True.
        """
        if VERBOSE: print('*'*120)
        
        #Other vars
        self.data_dir = data_dir
        self.pad_dir = pad_dir
        self.hdump_name = hdump_name
        
        #PMT/XA info
        s0 = time()
        self.pmt_arapuca_info = pd.read_pickle(f'{pad_dir}/PMT_ARAPUCA_info.pkl')
        self.pmt_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 0 or ophit_opdet_type == 1').index)
        self.xa_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 2 or ophit_opdet_type == 3').index)
        self.pds_ids = list(self.pmt_arapuca_info.index)
        self.pds_tpc0_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 0').index)
        self.pds_tpc1_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 1').index)
        s1 = time()
        if VERBOSE: print(f'Load PMT/XA channel info : {s1-s0:.2f} s')

        #Commissioning tree info
        s0 = time()
        tree = uproot.open(f'{data_dir}/{hdump_name}:hitdumper;1/hitdumpertree;1')
        hdrkeys = ['run','subrun','event']
        self.run_list = tree.arrays(hdrkeys,library='pd').values
        
        #Op info
        opkeys = [key for key in tree.keys() if 'op' == key[:2]]
        pmtsoftkeys = [key for key in tree.keys() if 'pmtSoftTrigger' in key]
        if use_op:
            self.op_df = tree.arrays(hdrkeys+opkeys,library='pd')
        else:
            self.op_df = tree.arrays(hdrkeys+opkeys,library='pd')
        s1 = time()
        if VERBOSE: print(f'Load commissioning tree : {s1-s0:.2f} s')

        #PMT waveform info - optional
        s0 = time()
        if wfm_name is None:
            self.wtree = None
        else:
            self.wtree = uproot.open(f'{data_dir}/{wfm_name}')
        s1 = time()
        if VERBOSE: print(f'Load waveforms : {s1-s0:.2f} s')
        
        #Muon info - optional
        muonkeys = [key for key in tree.keys() if 'muon' in key]
        if load_muon:
            self.muon_df = tree.arrays(hdrkeys+muonkeys)
        else: 
            self.muon_df = None
        #CRT info - optional
        self.crt_df = None
        
        #Set dummy values
        self.op_evt = None
        self.muon_evt = None
        self.crt_evt = None
        
        if VERBOSE: print('*'*120)
    def get_event(self,run,subrun,event):
        if [run,subrun,event] not in self.run_list:
            if VERBOSE: print(f'run {run} subrun {subrun} event {event} not in file {self.data_dir}/{self.hdump_name}')
            return None
        query_event = f'run == {run} and subrun == {subrun} and event == {event}'
        self.op_evt = self.op_df.query(query_event)
        if self.muon_df is not None:
            self.muon_evt = self.muon_df.query(query_event)
        self.waveform_hist_name = f'pmtSoftwareTrigger/run_{run}subrun_{subrun}event_{event}_pmtnum_PDSID;1'
        #if VERBOSE: print(f'Got run {run} subrun {subrun} event {event}')
        #Implement CRT here
    def get_pmt_list(self,tpc=None,coatings=[0,1,2,3]):
        """_summary_

        Returns:
            list(PMT): list of PDS components
        """
        #Store PMTs
        s0 = time()
        if tpc is None:
            pds_ids = self.pds_ids
            pmts = [PMT] * (120+192) #120 pmts, 192 X-ARAPUCAs
        elif tpc == 0:
            pds_ids = self.pds_tpc0_ids
            pmts = [PMT] * (60+96-8) #60 pmts, 96 X-ARAPUCAs per TPC, missing 8 APSIA
        elif tpc == 1:
            pds_ids = self.pds_tpc1_ids
            pmts = [PMT] * (60+96-8) #60 pmts, 96 X-ARAPUCAs per TPC, missing 8 APSIA
        else:
            raise Exception(f'Invalid tpc : {tpc}')
        for ind,i in enumerate(pds_ids):
            #if VERBOSE: print('pds_id : ',i)
            #Meta data
            meta = self.pmt_arapuca_info.loc[i]
            pds_location = np.array([meta.ophit_opdet_x,
                                    meta.ophit_opdet_y,
                                    meta.ophit_opdet_z])
            pds_coating = meta.ophit_opdet_type
            pds_tpc = meta.opdet_tpc
            
            #Get op info
            s2 = time()
            op_df = self.op_evt[self.op_evt.ophit_opch == i]
            op_times = op_df.ophit_peakT.values
            op_pes = op_df.ophit_pe.values
            pds_op_pe = {'op_time': op_times, 'op_pe': op_pes}
            s3 = time()
            #if VERBOSE: print(f'-- get op time {s3-s2:.3f} s')
            
            if i in self.pmt_ids and self.wtree is not None:
                #if VERBOSE: print('pds : ',i)
                #if i == 0: print('WTF*'*120)
                #Get waveform info
                s4 = time()
                hist_name = self.waveform_hist_name.replace('PDSID',str(i))
                hist = self.wtree[hist_name]
                #print(hist.to_numpy()[1])
                times = convert_edges_to_centers(hist.to_numpy()[1])
                voltages = hist.to_numpy()[0]
                pmt_waveform = {'time': times, 'voltage': voltages}
                s5 = time()
                #if VERBOSE: print(f'-- get waveform {s5-s4:.3f} s')
            else:
                pmt_waveform = None
            
            pmts[ind] = PMT(i, pds_coating, pds_tpc, pds_location, pmt_waveform, pds_op_pe, t1=t1, t0=t0, dt=dt)
        s1 = time()
        if VERBOSE: print(f'Get PDS objs : {s1-s0:.2f} s')
        return pmts
    def get_muon_list(self):
        pass
    def get_crt_list(self):
        pass
            
            


#Store muon track info

#Store CRT track info
