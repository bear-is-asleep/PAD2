import plotly.graph_objects as go
import numpy as np
from utils.plotters import map_value_to_color
from variables import *

class MCPart:
    def __init__(self, pdg, eng, px, py, pz, x1, y1, z1, x2, y2, z2, process, endprocess, start_t, end_t):
        self.pdg = pdg
        self.eng = eng
        self.px = px
        self.py = py
        self.pz = pz
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.process = process
        self.endprocess = endprocess
        self.start_t = start_t
        self.end_t = end_t
        
    def plot_line(self,ind,max_color=2212):
        # Generate a number of intermediate points along the line
        num_points = 10000
        z_values = np.linspace(self.z1, self.z2, num_points)
        y_values = np.linspace(self.y1, self.y2, num_points)

        text = f'Pdg : {self.pdg}'
        text += '<br>'
        text += f'E : {self.eng:.4f}'
        text += '<br>'
        text += f'px : {self.px:.4f}'
        text += '<br>'
        text += f'py : {self.py:.4f}'
        text += '<br>'
        text += f'pz : {self.pz:.4f}'
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
        text += f'StartT : {self.start_t:.2f}'
        text += '<br>'
        text += f'EndT : {self.end_t:.2f}'
        text += '<br>'
        text += f'process : {self.process}'
        text += '<br>'
        text += f'end process : {self.endprocess}'
        text += '<br>'
        
        if VERBOSE: print(f'MCPart {ind} : ({self.x1:.2f},{self.y1:.2f},{self.z1:.2f},{self.start_t:.2f}) to ({self.x2:.2f},{self.y2:.2f},{self.z2:.2f},{self.end_t:.2f})')
        
        color = map_value_to_color(ind,0,max_color,cmap='rainbow')
        return go.Scatter(
            x=z_values,
            y=y_values,
            mode='lines',
            name = f'MCPart {ind}',
            text = text,
            hoverinfo = 'text+name',
            line = dict(
              color=color
            )
        )
        

        