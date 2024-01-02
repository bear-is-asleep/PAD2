#software photoelectron example with waveforms

#Get directories
DATA_DIR = '/sbnd/data/users/ipatel/NC_trigger/test_fcl/v1' #Waveforms and hitdumper location

#Get fnames
HDUMP_NAME = None #None for no muons, crt or full op (need software name tho)
WFM_NAME = 'test_hist.root' #WFM_NAME = None if you did not make waveforms
SM_NAME = 'test_hist.root' #SM_NAME = None for no software metrics
PMT_ARA_NAME = 'PMT_ARAPUCA_info.pkl' #Sets channel id and locations

#PAD settings
MMAX = 'global' #Setting for max color. dynamic to set for every interval. global to set for max observable pe.
VERBOSE = True
HDRKEYS = ['run','sub','evt']
COATINGS = [1,2] #only PMTs supported
LOAD_MUON = False
LOAD_CRT = False
LOAD_MCPART = False
MODE = 'prompt'
T0_THRESHOLD = 10. #Min pe to denote t0