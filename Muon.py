import plotly.graph_objects as go
import numpy as np
from utils.plotters import map_value_to_color
from utils.maps import MUON_TYPES
from variables import *

class Muon:
    def __init__(self, trk_type, tpc, x1, y1, z1, x2, y2, z2, theta_xz, theta_yz):
        self.trk_type = trk_type
        self.tpc = tpc 
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.theta_xz = theta_xz
        self.theta_yz = theta_yz
        
    def plot_line(self,ind,tpc):
        if self.tpc != tpc: 
          return None
        # Generate a number of intermediate points along the line
        num_points = 1000
        z_values = np.linspace(self.z1, self.z2, num_points)
        y_values = np.linspace(self.y1, self.y2, num_points)

        text = f'Type : {MUON_TYPES[self.trk_type]}'
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
        text += f'theta_xz : {self.theta_xz:.2f}'
        text += '<br>'
        text += f'theta_yz : {self.theta_yz:.2f}'
        text += '<br>'
        
        if VERBOSE: print(f'Muon {ind} TPC{self.tpc}: ({self.x1:.2f},{self.y1:.2f},{self.z1:.2f}) to ({self.x2:.2f},{self.y2:.2f},{self.z2:.2f})')
        
        color = map_value_to_color(self.trk_type,0,5,cmap='rainbow')
        return go.Scatter(
            x=z_values,
            y=y_values,
            mode='lines',
            name = f'Muon {ind}',
            text = text,
            hoverinfo = 'text+name',
            line = dict(
              color=color,
              dash='dash'
            )
        )
        

        