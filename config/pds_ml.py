#default.py example

#PAD settings
CMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.

#Get directories
DATA_DIR = '/sbnd/data/users/brindenc/PDS_ml/test_fcl/pgun/pion' #Waveforms and hitdumper location
SAVE_DIR = '/sbnd/data/users/brindenc/PAD/figures' 
PAD_DIR  = '/sbnd/app/users/brindenc/PAD' #Your local PAD dir

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root'
WFM_NAME = None #WFM_NAME = None if you did not make waveforms
SM_NAME = None

#Settings
VERBOSE = True

#Hdr keys
HDRKEYS = ['run','subrun','event']

#Coatings
COATINGS = [0,1,2] #All PDS components [0,1,2,3,4]

#Bools
LOAD_MUON = False
LOAD_CRT = False
LOAD_MCPART = True
MODE = 'op'