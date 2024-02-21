#different particles from particle gun

#Get directories
DATA_DIR = '/sbnd/data/users/brindenc/PDS_ml/test_fcl/pgun/pion' #Waveforms and hitdumper location
SAVE_DIR = '/sbnd/data/users/brindenc/PAD/figures' 

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root'
WFM_NAME = None #WFM_NAME = None if you did not make waveforms
SM_NAME = None
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations

#PAD settings
MMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
VERBOSE = True #Doesn't really work - see variables.py
HDRKEYS = ['run','subrun','event']
COATINGS = [0,1,2] #All PDS components [0,1,2,3,4]
LOAD_MUON = False
LOAD_CRT = False
LOAD_MCPART = True
MODE = 'op'
T0_THRESHOLD = 10. #Min pe to denote t0