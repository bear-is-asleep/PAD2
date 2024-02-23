#intime cosmics config

#Get directories
#DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/test_fcl/v5' #Waveforms and hitdumper location
#DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/test_fcl/v6' #Waveforms and hitdumper location
DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/intime'
#HDUMP_NAME = 'hitdumper_tree.root' #Required
HDUMP_NAME = 'hitdumper_small.root'
#HDUMP_NAME = 'hitdumper_full.root'
#HDUMP_NAME = 'hitdumper_1.root'
WFM_NAME = None #WFM_NAME = None if you did not make waveforms
SM_NAME = None #SM_NAME = None if you did not make software metrics
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations
HDRKEYS = ['run','subrun','event'] #event id keys

#PDS settings
MMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
MODE = 'op' #op for full opreco, prompt for software pe prompt, prelim for software pe prelim
COATINGS = [0,1,2] #[undefined, coated pmt, uncoated pmt, vis xa, vuv xa]
T0_THRESHOLDS = [10.,1.] #Min pe to denote t0 [pmt,xa]
MAX_SPREAD = 1000 #Max spread of all pds's t0 in ns
t0 = -1600 #Start bin
t1 = 1600 #End bin for -1600 - 1600 ns in 2 ns steps
dt = 2  #ns step

#CRT settings
LOAD_CRT = True #CRT tracks 
CRT_FILTER_TPC = False #Filter CRT tracks to ones just in TPC

#MUON settings
LOAD_MUON = False #Muon tracks

#MCPart settings
LOAD_MCPART = True #G4 primary particles
MCPART_FILTER_TIME = True #Filter MCPart to +- 100us around beam window
MCPART_FILTER_TPC = False #Filter MCPart to TPC

#PAD settings
VERBOSE = True