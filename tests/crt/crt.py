#Your config
from config.intime_crt import *

#Rest of imports
import matplotlib.pyplot as plt
import argparse
import uproot
from utils import plotters

chit_keys = ['run','subrun','event','chit_x','chit_y','chit_z','chit_time','chit_plane']
ctrk_keys = ['run','subrun','event','ct_x1','ct_y1','ct_z1','ct_x2','ct_y2','ct_z2','ct_time','ct_pes']

tree = uproot.open(DATA_DIR + '/' + HDUMP_NAME)['hitdumper/hitdumpertree;1']
ctrk = tree.arrays(ctrk_keys,library='pd')
chit = tree.arrays(chit_keys,library='pd')

parser = argparse.ArgumentParser(description='Input entry number')
parser.add_argument('entry',type=int,help='Entry number')
args = parser.parse_args()
entry = args.entry

#check that the event is in the dataframe and write inds
inds = []
for i,ind in enumerate(ctrk.index.to_list()):
  if ind[0] == entry:
    inds.append(ind)
assert len(inds) >= 1, f'Entry {entry} not in dataframe'

#Make plots grouping by run, subrun, event
x1 = ctrk.loc[inds,'ct_x1']
y1 = ctrk.loc[inds,'ct_y1']
z1 = ctrk.loc[inds,'ct_z1']
x2 = ctrk.loc[inds,'ct_x2']
y2 = ctrk.loc[inds,'ct_y2']
z2 = ctrk.loc[inds,'ct_z2']
time = ctrk.loc[inds,'ct_time']
pes = ctrk.loc[inds,'ct_pes']
max_t,min_t = time.max(),time.min()

#check that the event is in the dataframe and write inds
inds = []
for i,ind in enumerate(chit.index.to_list()):
  if ind[0] == entry:
    inds.append(ind)
assert len(inds) >= 1, f'Entry {entry} not in dataframe'

#Make plots grouping by run, subrun, event
x = chit.loc[inds,'chit_x']
y = chit.loc[inds,'chit_y']
z = chit.loc[inds,'chit_z']
hit_time = chit.loc[inds,'chit_time']
plane = chit.loc[inds,'chit_plane']

min_t = min(min_t,hit_time.min())
max_t = max(max_t,hit_time.max())
time_color = [plotters.map_value_to_color(t,min_t,max_t) for t in time]
hit_time_color = [plotters.map_value_to_color(t,min_t,max_t) for t in hit_time]

fig,(ax,ax2,ax3) = plt.subplots(3,1,figsize=(6,10))
title = chit.loc[inds,['run','subrun','event']].iloc[0]
title = f'Run {title[0]} Subrun {title[1]} Event {title[2]}'
ax.set_title(f'CRT (time) ({title})')

#x,y
for _x1,_y1,_x2,_y2,_time in zip(x1,y1,x2,y2,time_color):
  ax.plot([_x1,_x2],[_y1,_y2],color='red',alpha=0.7,ls='-.')
im = ax.scatter(x,y,c=hit_time)
ax.set_xlabel('x (cm)')
ax.set_ylabel('y (cm)')
fig.colorbar(im,ax=ax,label='Time (ns)')
ax.hlines([-200,200],xmin=-200,xmax=200,color='black',alpha=0.5)
ax.vlines([-200,200],ymin=-200,ymax=200,color='black',alpha=0.5)

#z,x
ax2.plot([z1,z2],[x1,x2],color='red',alpha=0.7,ls='-.')
im = ax2.scatter(z,x,c=hit_time)
ax2.set_xlabel('z (cm)')
ax2.set_ylabel('x (cm)')
fig.colorbar(im,ax=ax2,label='Time (ns)')
ax2.hlines([-200,200],xmin=0,xmax=500,color='black',alpha=0.5)
ax2.vlines([0,500],ymin=-200,ymax=200,color='black',alpha=0.5)

#z,y
ax3.plot([z1,z2],[y1,y2],color='red',alpha=0.7,ls='-.')
im = ax3.scatter(z,y,c=hit_time)
ax3.set_xlabel('z (cm)')
ax3.set_ylabel('y (cm)')
fig.colorbar(im,ax=ax3,label='Time (ns)')
ax3.hlines([-200,200],xmin=0,xmax=500,color='black',alpha=0.5)
ax3.vlines([0,500],ymin=-200,ymax=200,color='black',alpha=0.5)
#ax3.axhline(200,xmin=0,xmax=500,color='black',alpha=0.5)

plt.savefig(f'crt{entry}.png')
