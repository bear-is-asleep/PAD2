#different particles from particle gun

#Get directories
DATA_DIR = '/exp/sbnd/data/users/brindenc/PAD/data/run17154' #Waveforms and hitdumper location
HDUMP_NAME = 'hitdumper_small.root'
SM_NAME = None
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations
HDRKEYS = ['run','subrun','event']

#PDS settings
MMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe. set to a number to set manually
MODE = 'op' #op for full opreco, prompt for software pe prompt, prelim for software pe prelim
COATINGS = [1,2] #[undefined, coated pmt, uncoated pmt, vis xa, vuv xa]
T0_THRESHOLDS = [5.,1.] #Min pe to denote t0 [pmt,xa]
MAX_SPREAD = 1e10 #Max spread of all pds's t0 in ns
tshift = 0#2135 #Time shift in us (add this to all peakT)
t0 = -2e3 #Start bin [ns]
t1 = 10*1e3#18.99*1e3 #End bin for -1600 - 1600 ns in 2 ns steps [ns]
dt = 2  #10 ns step
MAX_ENTRIES = 50 #Max number of entries to load
SET_TO_THRESHOLDS = False #Set colorbar scale to between t0 and t1 if True

#CRT settings
LOAD_CRT = True #CRT tracks 
CRT_FILTER_TPC = False #Filter CRT tracks to ones just in TPC
CRT_T0_MIN = -10e3 #Min CRT t0 in ns
CRT_T0_MAX = 20e3 #Max CRT t0 in ns

#MUON settings
LOAD_MUON = False #Muon tracks

#MCPart settings
LOAD_MCPART = False #G4 primary particles
MCPART_FILTER_TIME = False #Filter MCPart to +- 10us around beam window
MCPART_FILTER_TPC = False #Filter MCPart to TPC

#Waveform display settings
WFM_NAME = HDUMP_NAME #WFM_NAME = None if you did not make waveforms
WFM_RANGE = None #Range of waveforms to display in ms

#PAD settings
VERBOSE = True