#intime cosmics config

#Get directories
DATA_DIR = '/sbnd/data/users/brindenc/PAD/test_fcl/v3' #Waveforms and hitdumper location

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root' #Required
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = 'test_hist.root' #SM_NAME = None if you did not make software metrics
PMT_ARA_NAME = 'PMT_ARAPUCA_info.pkl' #Sets channel id and locations

#PAD settings
CMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
VERBOSE = True
HDRKEYS = ['run','subrun','event'] #event id keys
LOAD_MUON = True #Muon tracks
LOAD_CRT = True #CRT tracks 
LOAD_MCPART = True #G4 primary particles
MODE = 'op' #op for full opreco, prompt for software pe prompt, prelim for software pe prelim
COATINGS = [0,1,2,3,4] #all