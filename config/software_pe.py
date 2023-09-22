#software photoelectron example with waveforms

#PAD settings
CMAX = 'global' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.

#Get directories
DATA_DIR = '/sbnd/data/users/ipatel/NC_trigger/test_fcl/v1' #Waveforms and hitdumper location
SAVE_DIR = '/sbnd/data/users/brindenc/PAD/figures' 
PAD_DIR  = '/sbnd/app/users/brindenc/PAD' #Your local PAD dir

#Get fnames
HDUMP_NAME = None #None for no muons, crt or full op (need software name tho)
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = 'test_hist.root' #SM_NAME = None for no software metrics

#Settings
VERBOSE = True

#Hdr keys
HDRKEYS = ['run','sub','evt']

#Coatings
COATINGS = [1,2] #only PMTs supported

#Bools
LOAD_MUON = False
LOAD_CRT = False
LOAD_MCPART = False
MODE = 'prompt'