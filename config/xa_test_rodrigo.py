#intime cosmics config

#Get directories
DATA_DIR = '/exp/sbnd/data/users/rodrigoa/CALLOS/BearHitDumper' #Waveforms and hitdumper location

#Get fnames
HDUMP_NAME = 'hitdumper_tree.root' #Required
WFM_NAME = None #WFM_NAME = None if you did not make waveforms
SM_NAME = None #SM_NAME = None if you did not make software metrics
PMT_ARA_NAME = 'maps/PMT_ARAPUCA_info.csv' #Sets channel id and locations

#PAD settings
MMAX = 'dynamic' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
VERBOSE = True
HDRKEYS = ['run','subrun','event'] #event id keys
LOAD_MUON = False #Muon tracks
LOAD_CRT = False #CRT tracks 
LOAD_MCPART = False #G4 primary particles
MODE = 'op' #op for full opreco, prompt for software pe prompt, prelim for software pe prelim
COATINGS = [3,4] #all
T0_THRESHOLD = 0.01 #Min pe to denote t0