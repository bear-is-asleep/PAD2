import plotly.graph_objects as go
import numpy as np

#My imports
from utils.plotters import map_value_to_color
from utils.helpers import find_tpc_intersections,is_traj_in_volume
from utils.globals import *

class CRTTrack:
  def __init__(self,x1,y1,z1,x2,y2,z2,time,pes):
    self.true_start = [x1,y1,z1]
    self.true_end = [x2,y2,z2]
    #Start and end points are in the TPC
    self.start,self.end = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000)
    self.start0,self.end0 = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000,vol=TPC0_VOL)
    self.start1,self.end1 = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000,vol=TPC1_VOL)
    self.time = time
    self.pes = pes
    self.intpc0 = is_traj_in_volume([x1,y1,z1,x2,y2,z2],TPC0_VOL)
    self.intpc1 = is_traj_in_volume([x1,y1,z1,x2,y2,z2],TPC1_VOL)
  def plot_line(self,ind,tpc,max_color=1,filter_tpc=True):
    # Generate a number of intermediate points along the line
    num_points = 10000
    #Check if the track is in the TPC
    if filter_tpc:
      if tpc == 0 and self.intpc0:
        z_values = np.linspace(self.start0[2], self.end0[2], num_points)
        y_values = np.linspace(self.start0[1], self.end0[1], num_points)
        x1,y1,z1 = self.start0
        x2,y2,z2 = self.end0
      elif tpc == 1 and self.intpc1:
        z_values = np.linspace(self.start1[2], self.end1[2], num_points)
        y_values = np.linspace(self.start1[1], self.end1[1], num_points)
        x1,y1,z1 = self.start1
        x2,y2,z2 = self.end1
      else: #Not in the TPC
        return go.Scatter()
    else:  
      z_values = np.linspace(self.true_start[2], self.true_end[2], num_points)
      y_values = np.linspace(self.true_start[1], self.true_end[1], num_points)
      x1,y1,z1 = self.start
      x2,y2,z2 = self.end
    
    text = f't : {self.time:.2f}'
    text += '<br>'
    text += f'TPC start : ({x1:.2f},{y1:.2f},{z1:.2f})'
    text += '<br>'
    text += f'TPC end : ({x2:.2f},{y2:.2f},{z2:.2f})'
    text += '<br>'
    text += f'True start : ({self.true_start[0]:.2f},{self.true_start[1]:.2f},{self.true_start[2]:.2f})'
    text += '<br>'
    text += f'True end : ({self.true_end[0]:.2f},{self.true_end[1]:.2f},{self.true_end[2]:.2f})'
    text += '<br>'
    text += f'PE : {self.pes:.2f}'
    text += '<br>'
    text += f'InTPC0 : {self.intpc0}'
    text += '<br>'
    text += f'InTPC1 : {self.intpc1}'
    
    if VERBOSE: print(f'-CRTTrack {ind} : ({x1:.2f},{y1:.2f},{z1:.2f}) -> ({x2:.2f},{y2:.2f},{z2:.2f})')
    
    color = map_value_to_color(ind,0,max_color,cmap='rainbow')
    return go.Scatter(
            x=z_values,
            y=y_values,
            mode='lines',
            name = f'CRTTrack {ind}',
            text = text,
            hoverinfo = 'text+name',
            line = dict(
              color=color,
              dash='dashdot'
            )
        )
    