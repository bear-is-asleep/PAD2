import uproot
import pandas as pd
from variables import *
from PMT import PMT
from Muon import Muon
from MCPart import MCPart
from CRT import CRTTrack
from time import time
import numpy as np
from utils.helpers import convert_edges_to_centers,get_common_members
import os

class Loader:
    def __init__(self,data_dir,hdump_name=None,software_name=None,wfm_name=None,load_muon=False,
                 load_crt=False,load_mcpart=False,mode='op',hdrkeys=['run','subrun','event'],pmt_ara_name='PMT_ARAPUCA_info.pkl'):
        """Loads and stores trees

        Args:
            data_dir (_type_): _description_
            hdump_name (_type_): _description_
            software_name (str): Name of software metrics tree
            wfm_name (_type_, optional): _description_. Defaults to None.
            load_crt (bool, optional): Load CRT info from hitdumper. Defaults to False.
            load_muon (bool, optional): Load muon info from hitdumper. Defaults to False.
            load_mcpart (bool, optional): Load mcpart info from hitdumper. Defaults to False.
            mode (str, optional): Use full optical reconstruction set to prelim for prelimPE from software trigger
                                    and set to prompt to view prompt PE
            hdrkeys (list,optional): Keys denoting the event id
            pmt_ara_name (str,optional): Name of pkl file containing PMT/XA info
        """
        if VERBOSE: print('*'*60)
        
        #Other vars
        self.data_dir = data_dir
        self.hdump_name = hdump_name
        self.software_name = software_name
        self.wfm_name = wfm_name
        self.mode = mode
        self.load_muon = load_muon
        self.load_crt = load_crt
        self.load_mcpart = load_mcpart
        self.hdrkeys = hdrkeys
        
        #PMT/XA info
        s0 = time()
        self.pmt_arapuca_info = pd.read_pickle(pmt_ara_name)
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
        if self.hdump_name is None and self.software_name is not None:
            tree = uproot.open(f'{data_dir}/{self.software_name}:pmtSoftwareTrigger/software_metrics_tree;1')
        elif self.hdump_name is not None and self.software_name is None: 
            tree = uproot.open(f'{data_dir}/{self.hdump_name}:hitdumper;1/hitdumpertree;1')
        elif self.hdump_name is not None and self.software_name is not None:  #Default to hitdumper tree if both provided
            tree = uproot.open(f'{data_dir}/{self.hdump_name}:hitdumper;1/hitdumpertree;1')
        s1 = time()
        if VERBOSE: print(f'Load commissioning tree : {s1-s0:.2f} s')
        self.run_list = tree.arrays(self.hdrkeys,library='pd').values
        
        #Op info
        s0 = time()
        opkeys = [key for key in tree.keys() if 'op' == key[:2]]
        pmtsoftkeys = [key for key in tree.keys() if 'ch_' in key]
        if mode == 'op':
            self.op_df = tree.arrays(self.hdrkeys+opkeys,library='pd')
        elif mode == 'prompt' or mode == 'prelim':
            self.op_df = tree.arrays(self.hdrkeys+pmtsoftkeys,library='pd')
        else:
            raise Exception(f'Invalid mode : {mode}')
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
        if load_muon:
            s0 = time()
            muonkeys = [key for key in tree.keys() if 'muon' in key]
            self.muon_df = tree.arrays(self.hdrkeys+muonkeys,library='pd')
            s1 = time()
            if VERBOSE: print(f'Load muon tracks : {s1-s0:.2f} s')
        else: 
            self.muon_df = None
        #CRT info - optional
        if load_crt:
            s0 = time()
            crt_trkkeys = [key for key in tree.keys() if 'ct_' in key]
            self.crt_df = tree.arrays(self.hdrkeys+crt_trkkeys,library='pd')
            s1 = time()
            if VERBOSE: print(f'Load CRT trakcs: {s1-s0:.2f} s')
        else:
            self.crt_df = None
        
        #MCPart info
        if load_mcpart:
            part_keys = [key for key in tree.keys() if 'mcpart_' in key]
            parts = tree.arrays(self.hdrkeys+part_keys,library='pd')

            #Correct columns with strings
            processes = tree.arrays(['mcpart_process'],library='np')
            endprocesses = tree.arrays(['mcpart_endprocess'],library='np')
            
            mcpart_processes = []
            mcpart_endprocesses = []
            for p in processes['mcpart_process']:
                mcpart_processes += p
            for p in endprocesses['mcpart_endprocess']:
                mcpart_endprocesses += p

            parts['mcpart_process'] = mcpart_processes
            parts['mcpart_endprocess'] = mcpart_endprocesses
            
            #Filter by timing - give 1600 ns buffer + 1600ns beam window
            start_intime = parts.mcpart_StartT > -1600
            end_intime = parts.mcpart_StartT < 3200
            parts = parts[start_intime & end_intime]
            
            #Filter by primary
            self.mcpart_df = parts.query('mcpart_process == "primary"')
            
        else:
            self.mcpart_df = None
        
        #Set dummy values
        self.op_evt = None
        self.muon_evt = None
        self.crt_evt = None
        
        if VERBOSE: print('*'*60)
    def get_event(self,run,subrun,event):
        if [run,subrun,event] not in self.run_list:
            if VERBOSE: print(f'{self.hdrkeys[0]} {run} {self.hdrkeys[1]} {subrun} {self.hdrkeys[2]} {event} not in file {self.data_dir}/{self.hdump_name}')
            return None
        query_event = f'{self.hdrkeys[0]} == {run} and {self.hdrkeys[1]} == {subrun} and {self.hdrkeys[2]} == {event}'
        self.op_evt = self.op_df.query(query_event)
        if self.muon_df is not None:
            self.muon_evt = self.muon_df.query(query_event)
        if self.mcpart_df is not None:
            self.mcpart_evt = self.mcpart_df.query(query_event)
        if self.crt_df is not None:
            self.crt_evt = self.crt_df.query(query_event)
        if self.wtree is not None:
            if any([f'pmtSoftwareTrigger/run_{run}subrun_{subrun}event_{event}_' in k for k in self.wtree.keys()]):
                self.waveform_hist_name = f'pmtSoftwareTrigger/run_{run}subrun_{subrun}event_{event}_pmtnum_PDSID;1'
            else: 
                if VERBOSE: print(f'Warning: waveform for {self.hdrkeys[0]} {run} {self.hdrkeys[1]} {subrun} {self.hdrkeys[2]} {event} not in file {self.data_dir}/{self.wfm_name}')
                self.waveform_hist_name = None
        else:
            self.waveform_hist_name = None    
        self.run = run
        self.subrun = subrun
        self.event = event
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
            if self.mode == 'op':
                op_df = self.op_evt[self.op_evt.ophit_opch == i]
                op_times = op_df.ophit_peakT.values*1e3 #Convert to ns
                op_pes = op_df.ophit_pe.values
            elif self.mode == 'prompt' or self.mode == 'prelim':
                op_df = self.op_evt[self.op_evt.ch_ID == i]
                op_pes = op_df.loc[:,f'ch_{self.mode}PE'].values
                op_times = [t0]
            pds_op_pe = {'op_time': op_times, 'op_pe': op_pes}
            s3 = time()
            #if VERBOSE: print(f'-- get op time {s3-s2:.3f} s')
            
            #Check if the waveform exists
            if i in self.pmt_ids and self.wtree is not None and self.waveform_hist_name is not None:
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
    def get_mcpart_list(self,keep_pdgs=None):
        
        mcparts = []
        #Extract info into arrays
        pdgs, engs, pxs, pys, pzs, x1s, y1s, z1s, x2s, y2s, z2s, processes, endprocesses,start_ts,end_ts = (
            self.mcpart_evt.mcpart_pdg.values,
            self.mcpart_evt.mcpart_Eng.values,
            self.mcpart_evt.mcpart_Px.values,
            self.mcpart_evt.mcpart_Py.values,
            self.mcpart_evt.mcpart_Pz.values,
            self.mcpart_evt.mcpart_StartPointx.values,
            self.mcpart_evt.mcpart_StartPointy.values,
            self.mcpart_evt.mcpart_StartPointz.values,
            self.mcpart_evt.mcpart_EndPointx.values,
            self.mcpart_evt.mcpart_EndPointy.values,
            self.mcpart_evt.mcpart_EndPointz.values,
            self.mcpart_evt.mcpart_process.values,
            self.mcpart_evt.mcpart_endprocess.values,
            self.mcpart_evt.mcpart_StartT.values,
            self.mcpart_evt.mcpart_EndT.values
        )
        if keep_pdgs is None:
            for i in range(len(pdgs)):
                mcparts.append(MCPart(pdgs[i], engs[i], pxs[i], pys[i], pzs[i], x1s[i], y1s[i], z1s[i], x2s[i], y2s[i], z2s[i], processes[i], endprocesses[i], start_ts[i], end_ts[i]))
        return mcparts
    def get_crt_list(self):
        crt_trks = []
        #Extract info into arrays
        x1s, y1s, z1s, x2s, y2s, z2s, times, pes = (
            self.crt_evt.ct_x1.values,
            self.crt_evt.ct_y1.values,
            self.crt_evt.ct_z1.values,
            self.crt_evt.ct_x2.values,
            self.crt_evt.ct_y2.values,
            self.crt_evt.ct_z2.values,
            self.crt_evt.ct_time.values,
            self.crt_evt.ct_pes.values,
        )
        for i in range(len(x1s)):
            crt_trks.append(CRTTrack(x1s[i], y1s[i], z1s[i], x2s[i], y2s[i], z2s[i], times[i], pes[i]))
        return crt_trks
    def get_pe_centroid(self,coating=0):
        pass
        
            
            


#Store muon track info

#Store CRT track info
