import uproot
import pandas as pd
from variables import *
from config.test import *
from PMT import PMT
from Muon import Muon
from time import time
import numpy as np
from utils.helpers import convert_edges_to_centers,get_common_members

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
        if VERBOSE: print('*'*60)
        
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
        #TPCs
        self.pds_tpc0_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 0').index)
        self.pds_tpc1_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 1').index)
        #Coatings
        self.pds_undefined_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == -1').index)
        self.pmt_coated_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 0').index)
        self.pmt_uncoated_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 1').index)
        self.xa_vis_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 2').index)
        self.xa_vuv_ids = list(self.pmt_arapuca_info.query('ophit_opdet_type == 3').index)
        
        #Coatings in tpc
        self.pds_list = [
            get_common_members(self.pds_ids,self.pds_undefined_ids),
            get_common_members(self.pds_ids,self.pmt_coated_ids),
            get_common_members(self.pds_ids,self.pmt_uncoated_ids),
            get_common_members(self.pds_ids,self.xa_vis_ids),
            get_common_members(self.pds_ids,self.xa_vuv_ids),
        ]
        self.pds_tpc0_list = [
            get_common_members(self.pds_tpc0_ids,self.pds_undefined_ids),
            get_common_members(self.pds_tpc0_ids,self.pmt_coated_ids),
            get_common_members(self.pds_tpc0_ids,self.pmt_uncoated_ids),
            get_common_members(self.pds_tpc0_ids,self.xa_vis_ids),
            get_common_members(self.pds_tpc0_ids,self.xa_vuv_ids),
        ]
        self.pds_tpc1_list = [
            get_common_members(self.pds_tpc1_ids,self.pds_undefined_ids),
            get_common_members(self.pds_tpc1_ids,self.pmt_coated_ids),
            get_common_members(self.pds_tpc1_ids,self.pmt_uncoated_ids),
            get_common_members(self.pds_tpc1_ids,self.xa_vis_ids),
            get_common_members(self.pds_tpc1_ids,self.xa_vuv_ids),
        ]
        s1 = time()
        if VERBOSE: print(f'Load PMT/XA channel info : {s1-s0:.2f} s')

        #Commissioning tree info
        s0 = time()
        tree = uproot.open(f'{data_dir}/{hdump_name}:hitdumper;1/hitdumpertree;1')
        s1 = time()
        if VERBOSE: print(f'Load commissioning tree : {s1-s0:.2f} s')
        hdrkeys = ['run','subrun','event']
        self.run_list = tree.arrays(hdrkeys,library='pd').values
        
        #Op info
        s0 = time()
        opkeys = [key for key in tree.keys() if 'op' == key[:2]]
        pmtsoftkeys = [key for key in tree.keys() if 'pmtSoftTrigger' in key]
        if use_op:
            self.op_df = tree.arrays(hdrkeys+opkeys,library='pd')
        else:
            self.op_df = tree.arrays(hdrkeys+opkeys,library='pd')
        s1 = time()
        if VERBOSE: print(f'Load op info : {s1-s0:.2f} s')
        #PMT waveform info - optional
        
        if wfm_name is None:
            self.wtree = None
        else:
            s0 = time()
            self.wtree = uproot.open(f'{data_dir}/{wfm_name}')
            s1 = time()
            if VERBOSE: print(f'Load waveforms : {s1-s0:.2f} s')
        
        #Muon info - optional
        muonkeys = [key for key in tree.keys() if 'muon' in key]
        if load_muon:
            s0 = time()
            self.muon_df = tree.arrays(hdrkeys+muonkeys,library='pd')
            s1 = time()
            if VERBOSE: print(f'Load muon tracks : {s1-s0:.2f} s')
        else: 
            self.muon_df = None
        #CRT info - optional
        self.crt_df = None
        
        #Set dummy values
        self.op_evt = None
        self.muon_evt = None
        self.crt_evt = None
        
        if VERBOSE: print('*'*60)
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
    def get_pmt_list(self,tpc=None,coatings=[0,1,2,3,4]):
        """_summary_
        
        Args:
            int(tpc): tpc for
        
        Returns:
            list(PMT): list of PDS components
        """
        #Store PMTs
        s0 = time()
        pmts = []
        if tpc is None:
            #Get pds components specified by coatings
            pds_ids = []
            for c in coatings:
                pds_ids += self.pds_list[c]
        elif tpc == 0:
            #Get pds components specified by coatings
            pds_ids = []
            for c in coatings:
                pds_ids += self.pds_tpc0_list[c]
            #pmts = [PMT] * (60+96-8) #60 pmts, 96 X-ARAPUCAs per TPC, missing 8 APSIA
        elif tpc == 1:
            #Get pds components specified by coatings
            pds_ids = []
            for c in coatings:
                pds_ids += self.pds_tpc1_list[c]
            #pmts = [PMT] * (60+96-8) #60 pmts, 96 X-ARAPUCAs per TPC, missing 8 APSIA
        else:
            raise Exception(f'Invalid tpc : {tpc}')
        for ind,i in enumerate(pds_ids):
            #if VERBOSE: print('pds_id : ',i)
            #if VERBOSE: print('ind : ',ind)
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
            
            pmts.append(PMT(i, pds_coating, pds_tpc, pds_location, pmt_waveform, pds_op_pe, t1=t1, t0=t0, dt=dt))
        s1 = time()
        if VERBOSE: print(f'Get PDS objs : {s1-s0:.2f} s')
        return pmts
    def get_muon_list(self,tpc,types=[0,1,2,3,4,5]):
        
        muons = []
        #Extract info into arrays
        trk_types, tpcs, x1s, y1s, z1s, x2s, y2s, z2s, theta_xzs, theta_yzs = self.muon_evt.muontrk_type.values, self.muon_evt.muontrk_tpc.values, self.muon_evt.muontrk_x1.values, self.muon_evt.muontrk_y1.values, self.muon_evt.muontrk_z1.values, self.muon_evt.muontrk_x2.values, self.muon_evt.muontrk_y2.values, self.muon_evt.muontrk_z2.values, self.muon_evt.muontrk_theta_xz.values, self.muon_evt.muontrk_theta_yz.values
        #keep specified muons
        for i,trk_type in enumerate(trk_types):
           if trk_type in types and tpc == tpcs[i]:
               muons.append(Muon(trk_types[i], tpcs[i], x1s[i], y1s[i], z1s[i], x2s[i], y2s[i], z2s[i], theta_xzs[i], theta_yzs[i]))
        return muons
    def get_crt_list(self):
        pass
            
            


#Store muon track info

#Store CRT track info
