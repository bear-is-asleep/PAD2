#default.py example

#PAD settings
CMAX = 'global' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.

#Get directories
DATA_DIR = '/sbnd/data/users/brindenc/PAD/test_fcl/v1' #Waveforms and hitdumper location
SAVE_DIR = '/sbnd/data/users/brindenc/PAD/figures' 
PAD_DIR  = '/sbnd/app/users/brindenc/PAD' #Your local PAD dir

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root'
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = 'test_hist.root'

#Settings
VERBOSE = True

#Hdr keys
HDRKEYS = ['run','subrun','event']

#Coatings
COATINGS = [0,1,2,3,4] #All PDS components

#Bools
LOAD_MUON = True
LOAD_CRT = False
LOAD_MCPART = True
MODE = 'op'