#software photoelectron example with waveforms

#Get directories
DATA_DIR = '/sbnd/data/users/ipatel/NC_trigger/test_fcl/v1' #Waveforms and hitdumper location

#Get fnames
HDUMP_NAME = None #None for no muons, crt or full op (need software name tho)
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = 'test_hist.root' #SM_NAME = None for no software metrics
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations
HDRKEYS = ['run','sub','evt']

#PDS settings
MMAX = 'global' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
COATINGS = [1,2] #only PMTs supported
MODE = 'prompt'
T0_THRESHOLDS = [10.,1.] #Min pe to denote t0
MAX_SPREAD = 1000 #Max spread of all pds's t0 in ns
t0 = -1600 #Start bin
t1 = 1600 #End bin for -1600 - 1600 ns in 2 ns steps
dt = 2  #ns step

#CRT settings
LOAD_CRT = False #CRT tracks 
CRT_FILTER_TPC = False #Filter CRT tracks to ones just in TPC

#MUON settings
LOAD_MUON = False #Muon tracks

#MCPart settings
LOAD_MCPART = False #G4 primary particles
MCPART_FILTER_TIME = False #Filter MCPart to +- 10us around beam window
MCPART_FILTER_TPC = False #Filter MCPart to TPC

#PAD settings
VERBOSE = True