import uproot
import pandas as pd
from time import time
import numpy as np
import os
from tqdm import tqdm

from PMT import PMT
from Muon import Muon
from MCPart import MCPart
from CRT import CRTTrack
from utils.helpers import convert_edges_to_centers,get_common_members,is_traj_in_volume
from utils.globals import *

class Loader:
    def __init__(self,data_dir,hdump_name=None,software_name=None,wfm_name=None,load_muon=False,
                 load_crt=False,load_mcpart=False,mode='op',hdrkeys=['run','subrun','event'],pmt_ara_name='maps/PMT_ARAPUCA_info.csv'
                 ,filter_primaries=True,max_entries=10000,wfm_range=None,tshift=0.,crt_min_t0=-1e10,crt_max_t0=1e10):
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
            filter_primaries (bool,optional): Filter mcpart to only particles within +- 10 us of beam window
            max_entries (int,optional): Maximum number of entries to load
            wfm_range (list,optional): Range of waveforms to display in us
            tshift (float,optional): Time shift in ns for peakT values for PDS
            crt_min_t0 (float,optional): Minimum t0 for CRT tracks
            crt_max_t0 (float,optional): Maximum t0 for CRT tracks
        """
        if VERBOSE: print('*'*50)
        
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
        self.wfm_range = wfm_range
        
        #PMT/XA info
        s0 = time()
        self.pmt_arapuca_info = pd.read_csv(pmt_ara_name)
        # self.pmt_ids = list(self.pmt_arapuca_info.query('"pds" in pd_type').index)
        # self.xa_ids = list(self.pmt_arapuca_info.query('"xarapuca" in pd_type').index)
        self.pds_ids = list(self.pmt_arapuca_info.index)
        #TPCs
        self.pds_tpc0_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 0').index)
        self.pds_tpc1_ids = list(self.pmt_arapuca_info.query('opdet_tpc == 1').index)
        #Coatings
        self.pds_undefined_ids = list(self.pmt_arapuca_info.query('"undefined" == pd_type').index)
        self.pmt_coated_ids = list(self.pmt_arapuca_info.query('"pmt_coated" == pd_type').index)
        self.pmt_uncoated_ids = list(self.pmt_arapuca_info.query('"pmt_uncoated" == pd_type').index)
        self.pmt_ids = self.pmt_coated_ids + self.pmt_uncoated_ids
        self.xa_vis_ids = list(self.pmt_arapuca_info.query('"xarapuca_vis" == pd_type').index)
        self.xa_vuv_ids = list(self.pmt_arapuca_info.query('"xarapuca_vuv" == pd_type').index)
        self.xa_ids = self.xa_vis_ids + self.xa_vuv_ids
        
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
        self.run_list = tree.arrays(self.hdrkeys,library='pd').values
        if max_entries is None:
            self.entries = tree.num_entries
        else:
            self.entries = min(tree.num_entries,max_entries)
        #Check for unique run values, if they're not unique then there are duplicate events and we will raise an error
        if len(self.run_list) != len(np.unique(self.run_list,axis=0)):
            raise Exception(f'Error: Duplicate events in {self.data_dir}/{self.hdump_name}')
        if VERBOSE: print(f'Load commissioning tree ({len(self.run_list)} events) : {s1-s0:.2f} s')
        if VERBOSE and len(self.run_list) >= 100: print(f'WARNING: Loading too many events. This will probably kill the kernel.')
        
        #Op info
        s0 = time()
        if VERBOSE: print(f'Loading op info for {self.entries} events...')
        opkeys = [key for key in tree.keys() if 'op' == key[:2]]
        pmtsoftkeys = [key for key in tree.keys() if 'ch_' in key]
        #Load op info in chunks to save memory
        chunk_size = 1
        chunks = []
        for start in tqdm(range(0,self.entries,chunk_size)):
            #if VERBOSE: print(f'-Loading chunk {start//chunk_size+1}/{self.entries//chunk_size}')
            stop = min(start+chunk_size,self.entries)
            if mode == 'op':
                chunk = tree.arrays(self.hdrkeys+opkeys,library='pd', entry_start=start, entry_stop=stop)
            elif mode == 'prompt' or mode == 'prelim':
                chunk = tree.arrays(self.hdrkeys+pmtsoftkeys,library='pd', entry_start=start, entry_stop=stop)
            else:
                raise Exception(f'Invalid mode : {mode}')
            chunks.append(chunk)
        self.op_df = pd.concat(chunks)
        if tshift != 0:
            self.op_df['ophit_peakT'] += tshift
            _mmin = self.op_df.ophit_peakT.min()
            _mmax = self.op_df.ophit_peakT.max()
            if VERBOSE: print(f'Adding time shift of {tshift} ns to peakT (min,max) : ({_mmin:.3f},{_mmax:.3f} us)')
        s1 = time()
        if VERBOSE: print(f'Load op info : {s1-s0:.2f} s')
        #PMT waveform info - optional
        
        if wfm_name is None:
            self.wtree = None
            if VERBOSE: print(f'No waveform data provided')
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
            crt_trkkeys = [key for key in tree.keys() if 'crt_track' in key]
            self.crt_df = tree.arrays(self.hdrkeys+crt_trkkeys,library='pd')
            #Filter between t0 values
            self.crt_df = self.crt_df.query(f'crt_track_t0 > {crt_min_t0} and crt_track_t0 < {crt_max_t0}')
            s1 = time()
            if VERBOSE: print(f'Load CRT tracks: {s1-s0:.2f} s')
        else:
            self.crt_df = None
        
        #MCPart info - optional
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
            
            #Filter by timing - give +- 100us buffer
            if filter_primaries:
                start_intime = parts.mcpart_StartT > -100000
                end_intime = parts.mcpart_StartT < 116000
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
            elif any([f'wvfana/event_{event}' in k for k in self.wtree.keys()]):
                #event_29_opchannel_163_pmt_coated_163
                #event_29_opchannel_150_xarapuca_vuv_150
                #event_29_opchannel_161_xarapuca_vis_161
                #event_29_opchannel_192_pmt_uncoated_192
                
                #Since the end of the name is an indexer dependent on what's loaded, we're just going to filter by PDSID and PDSTYPE
                self.waveform_hist_name = f'wvfana/event_{event}_opchannel_PDSID_PDSTYPE'
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
    def get_pmt_list(self,t0,t1,dt,tpc=None,coatings=[0,1,2,3,4]):
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
            pds_pd_type = meta.pd_type
            pds_tpc = meta.opdet_tpc
            pds_sampling = meta.sampling
            pds_box = meta.pds_box
            
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
            # print('pds_id : ',i)
            # print('pds_pd_type : ',pds_pd_type)
            # print(self.waveform_hist_name)
            # print(i in self.pds_ids)
            # print(self.pds_ids)
            # print(self.wtree is not None)
            if i in self.pmt_ids and self.wtree is not None and self.waveform_hist_name is not None:
                #if VERBOSE: print('pds : ',i)
                #if i == 0: print('WTF*'*120)
                #Get waveform info
                s4 = time()
                hist_name = self.waveform_hist_name.replace('PDSID',str(i))
                if 'PDSTYPE' in hist_name:
                    hist_name = hist_name.replace('PDSTYPE',pds_pd_type)
                #Now complete the key name based on what keys in the tree match what we have for hist_name
                name_candidates = [k for k in self.wtree.keys() if hist_name in k]
                if len(name_candidates) == 1:
                    hist_name = name_candidates[0]
                else:
                    raise Exception(f'Error: Multiple candidates for {hist_name} in {self.data_dir}/{self.wfm_name}')
                    print(name_candidates)
                if hist_name in self.wtree.keys():  
                    hist = self.wtree[hist_name]
                    times = hist.axis().edges()
                    voltages = hist.values()
                    #Filter to time range of interest (conserves size)
                    if self.wfm_range is not None: 
                        inds = np.where((times >= self.wfm_range[0]) & (times <= self.wfm_range[1]))[0]
                        times = times[inds]
                        voltages = voltages[inds]
                    pmt_waveform = {'time': times, 'voltage': voltages}
                    s5 = time()
                    #if VERBOSE: print(f'-- get waveform {s5-s4:.3f} s')
                else:
                    if VERBOSE: print(f'Warning: {hist_name} not in file {self.data_dir}/{self.wfm_name}')
                    pmt_waveform = None
            else:
                pmt_waveform = None
            
            pmts.append(PMT(i, pds_pd_type, pds_tpc, pds_location, pds_sampling, pds_box,waveform=pmt_waveform, op_pe=pds_op_pe, t1=t1, t0=t0, dt=dt))
        s1 = time()
        if VERBOSE: print(f'-Get PDS objs : {s1-s0:.2f} s')
        return pmts
    def get_muon_list(self,tpc,types=[0,1,2,3,4,5]):
        
        muons = []
        #Extract info into arrays
        trk_types, tpcs, x1s, y1s, z1s, x2s, y2s, z2s, theta_xzs, theta_yzs, t0s = self.muon_evt.muontrk_type.values, self.muon_evt.muontrk_tpc.values, self.muon_evt.muontrk_x1.values, self.muon_evt.muontrk_y1.values, self.muon_evt.muontrk_z1.values, self.muon_evt.muontrk_x2.values, self.muon_evt.muontrk_y2.values, self.muon_evt.muontrk_z2.values, self.muon_evt.muontrk_theta_xz.values, self.muon_evt.muontrk_theta_yz.values, self.muon_evt.muontrk_t0.values
        #keep specified muons
        for i,trk_type in enumerate(trk_types):
           if trk_type in types and tpc == tpcs[i]:
               muons.append(Muon(trk_types[i], tpcs[i], x1s[i], y1s[i], z1s[i], x2s[i], y2s[i], z2s[i], theta_xzs[i], theta_yzs[i], t0s[i]))
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
    def get_crt_list(self,filter_volume=True):
        crt_trks = []
        #Extract info into arrays
        x1s, y1s, z1s, x2s, y2s, z2s, t0s, t1s, pes = (
            self.crt_evt.crt_track_x1.values,
            self.crt_evt.crt_track_y1.values,
            self.crt_evt.crt_track_z1.values,
            self.crt_evt.crt_track_x2.values,
            self.crt_evt.crt_track_y2.values,
            self.crt_evt.crt_track_z2.values,
            self.crt_evt.crt_track_t0.values,
            self.crt_evt.crt_track_t1.values,
            self.crt_evt.crt_track_pes.values,
        )
        for i in range(len(x1s)):
            crt_trks.append(CRTTrack(x1s[i], y1s[i], z1s[i], x2s[i], y2s[i], z2s[i], t0s[i], t1s[i], pes[i]))
        return crt_trks
    def get_pe_centroid(self,coating=0):
        pass
