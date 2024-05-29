#different particles from particle gun

#Get directories
DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/intime/Aprv1' #Waveforms and hitdumper location
HDUMP_NAME = 'hitdumper_tree_5.root'
SM_NAME = None
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations
HDRKEYS = ['run','subrun','event']

#PDS settings
MMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe. set to a number to set manually
MODE = 'op' #op for full opreco, prompt for software pe prompt, prelim for software pe prelim
COATINGS = [1,2] #[undefined, coated pmt, uncoated pmt, vis xa, vuv xa]
T0_THRESHOLDS = [20.,5.] #Min pe to denote t0 [pmt,xa]
MAX_SPREAD = 100 #Max spread of all pds's t0 in ns
t0 = -1600 #Start bin
t1 = 1600 #End bin for -1600 - 1600 ns in 2 ns steps
dt = 2  #ns step
MAX_ENTRIES = 5 #Max number of entries to load
SET_TO_THRESHOLDS = False #Set colorbar scale to between t0 and t1 if True

#CRT settings
LOAD_CRT = False #CRT tracks 
CRT_FILTER_TPC = True #Filter CRT tracks to ones just in TPC

#MUON settings
LOAD_MUON = False #Muon tracks

#MCPart settings
LOAD_MCPART = False #G4 primary particles
MCPART_FILTER_TIME = True #Filter MCPart to +- 10us around beam window
MCPART_FILTER_TPC = True #Filter MCPart to TPC

#Waveform display settings
WFM_NAME = None #WFM_NAME = None if you did not make waveforms
WFM_RANGE = [0.,2e-3] #Range of waveforms to display in ms

#PAD settings
VERBOSE = True