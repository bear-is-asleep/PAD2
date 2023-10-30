import plotly.graph_objects as go
import numpy as np
from utils.plotters import map_value_to_color
from variables import *

class CRTTrack:
  def __init__(self,x1,y1,z1,x2,y2,z2,time,pes):
    self.x1 = x1
    self.y1 = y1
    self.z1 = z1
    self.x2 = x2
    self.y2 = y2
    self.z2 = z2
    self.time = time
    self.pes = pes
  def plot_line(self,ind,max_color=1):
    # Generate a number of intermediate points along the line
    num_points = 10000
    z_values = np.linspace(self.z1, self.z2, num_points)
    y_values = np.linspace(self.y1, self.y2, num_points)
    
    text = f't : {self.time:.2f}'
    text += '<br>'
    text += f'x1 : {self.x1:.2f}'
    text += '<br>'
    text += f'y1 : {self.y1:.2f}'
    text += '<br>'
    text += f'z1 : {self.z1:.2f}'
    text += '<br>'
    text += f'x2 : {self.x2:.2f}'
    text += '<br>'
    text += f'y2 : {self.y2:.2f}'
    text += '<br>'
    text += f'z2 : {self.z2:.2f}'
    text += '<br>'
    text += f'PE : {self.pes:.2f}'
    
    if VERBOSE: print(f'CRTTrack {ind} : ({self.x1:.2f},{self.y1:.2f},{self.z1:.2f}) to ({self.x2:.2f},{self.y2:.2f},{self.z2:.2f})')
    
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
    