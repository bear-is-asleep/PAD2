#Your config
from config.intime_crt import *

#Rest of imports
import matplotlib.pyplot as plt
import argparse
import uproot
from utils import plotters

trk_keys = ['run','subrun','event','muontrk_x1','muontrk_y1','muontrk_z1','muontrk_x2','muontrk_y2','muontrk_z2']
mhit_keys = ['run','subrun','event','mhit_wire','mhit_peakT','mhit_plane']
hit_keys = ['run','subrun','event','hit_wire','hit_peakT','hit_plane']
tree = uproot.open(DATA_DIR + '/' + HDUMP_NAME)['hitdumper/hitdumpertree;1']
trk_muon = tree.arrays(trk_keys,library='pd')
mhit_muon = tree.arrays(mhit_keys,library='pd')
hits = tree.arrays(hit_keys,library='pd')
mhit_muon = mhit_muon[mhit_muon['mhit_plane'] == 2] #Collection plane
hits = hits[hits['hit_plane'] == 2] #Collection plane

parser = argparse.ArgumentParser(description='Input entry number')
parser.add_argument('entry',type=int,help='Entry number')
args = parser.parse_args()

#check that the event is in the muon dataframe and write inds
entry = args.entry
inds = []
for i,ind in enumerate(trk_muon.index.to_list()):
  if ind[0] == entry:
    inds.append(ind)
assert len(inds) >= 1, f'Entry {entry} not in muon dataframe'

#Make plots grouping by run, subrun, event
x1 = trk_muon.loc[inds,'muontrk_x1']
y1 = trk_muon.loc[inds,'muontrk_y1']
z1 = trk_muon.loc[inds,'muontrk_z1']
x2 = trk_muon.loc[inds,'muontrk_x2']
y2 = trk_muon.loc[inds,'muontrk_y2']
z2 = trk_muon.loc[inds,'muontrk_z2']

fig,(ax,ax2,ax3) = plt.subplots(3,1,figsize=(6,10))
ax.set_title(f'Entry {entry}')
#x,y
ax.plot([x1,x2],[y1,y2],ls='-.')
ax.set_xlabel('x (cm)')
ax.set_ylabel('y (cm)')
ax.set_xlim(-220,220)
ax.set_ylim(-220,220)

#z,x
ax2.plot([z1,z2],[x1,x2],ls='-.')
ax2.set_xlabel('z (cm)')
ax2.set_ylabel('x (cm)')
ax2.set_xlim(-20,520)
ax2.set_ylim(-220,220)

#z,y
ax3.plot([z1,z2],[y1,y2],ls='-.')
ax3.set_xlabel('z (cm)')
ax3.set_ylabel('y (cm)')
ax3.set_xlim(-20,520)
ax3.set_ylim(-220,220)

# plotters.set_style(ax)
# plotters.set_style(ax2)
# plotters.set_style(ax3)

plt.savefig('muontrk.png')

#check that the event is in the muon dataframe and rewrite inds
entry = args.entry
inds = []
for i,ind in enumerate(mhit_muon.index.to_list()):
  if ind[0] == entry:
    inds.append(ind)
assert len(inds) >= 1, f'Entry {entry} not in muon dataframe'

wmax,wmin = hits.loc[:,'hit_wire'].max(),hits.loc[:,'hit_wire'].min()
tmax,tmin = hits.loc[:,'hit_peakT'].max(),hits.loc[:,'hit_peakT'].min()

#Make plots of mhits
wire = mhit_muon.loc[inds,'mhit_wire']
time = mhit_muon.loc[inds,'mhit_peakT']

fig,ax = plt.subplots()
ax.set_title(f'Muon hits entry {entry}')
ax.scatter(wire,time,s=2)
ax.set_xlabel('Wire')
ax.set_ylabel('peakT')
ax.set_xlim(wmin,wmax)
ax.set_ylim(tmin,tmax)

plt.savefig('muonhit.png')

#check that the event is in the dataframe and rewrite inds
entry = args.entry
inds = []
for i,ind in enumerate(hits.index.to_list()):
  if ind[0] == entry:
    inds.append(ind)
assert len(inds) >= 1, f'Entry {entry} not in hits dataframe'

#Make plots of hits
wire = hits.loc[inds,'hit_wire']
time = hits.loc[inds,'hit_peakT']

fig,ax = plt.subplots()
ax.set_title(f'Hits entry {entry}')
ax.scatter(wire,time,s=2)
ax.set_xlabel('Wire')
ax.set_ylabel('peakT')
ax.set_xlim(wmin,wmax)
ax.set_ylim(tmin,tmax)

plt.savefig('hit.png')
