import plotly.graph_objects as go
import numpy as np
from utils.plotters import map_value_to_color
from utils.helpers import find_tpc_intersections,is_traj_in_volume
from utils.globals import SBND_VOL,TPC0_VOL,TPC1_VOL
from utils.globals import *

class MCPart:
    def __init__(self, pdg, eng, px, py, pz, x1, y1, z1, x2, y2, z2, process, endprocess, start_t, end_t):
        self.pdg = pdg
        self.eng = eng
        self.px = px
        self.py = py
        self.pz = pz
        self.true_start = [x1,y1,z1]
        self.true_end = [x2,y2,z2]
        #Start and end points are in the TPC
        self.start,self.end = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000,vol=SBND_VOL)
        self.start0,self.end0 = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000,vol=TPC0_VOL)
        self.start1,self.end1 = find_tpc_intersections(x1,y1,z1,x2,y2,z2,n=10000,vol=TPC1_VOL)
        self.process = process
        self.endprocess = endprocess
        self.start_t = start_t
        self.end_t = end_t
        self.intpc0 = is_traj_in_volume([x1,y1,z1,x2,y2,z2],TPC0_VOL)
        self.intpc1 = is_traj_in_volume([x1,y1,z1,x2,y2,z2],TPC1_VOL)
        
    def plot_line(self,ind,tpc,max_color=1,filter_tpc=True):
        # Generate a number of intermediate points along the line
        num_points = 10000
        #Check if the particle is in the TPC
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

        text = f'Pdg : {self.pdg}'
        text += '<br>'
        text += f'E : {self.eng:.4f}'
        text += '<br>'
        text += f'p : ({self.px:.4f},{self.py:.4f},{self.pz:.4f})'
        text += '<br>'
        text += f'TPC start : ({x1:.2f},{y1:.2f},{z1:.2f})'
        text += '<br>'
        text += f'TPC end : ({x2:.2f},{y2:.2f},{z2:.2f})'
        text += '<br>'
        text += f'True start : ({self.true_start[0]:.2f},{self.true_start[1]:.2f},{self.true_start[2]:.2f})'
        text += '<br>'
        text += f'True end : ({self.true_end[0]:.2f},{self.true_end[1]:.2f},{self.true_end[2]:.2f})'
        text += '<br>'
        text += f'StartT : {self.start_t:.2f}'
        text += '<br>'
        text += f'EndT : {self.end_t:.2f}'
        text += '<br>'
        text += f'process : {self.process}'
        text += '<br>'
        text += f'end process : {self.endprocess}'
        text += '<br>'
        text += f'In TPC0 : {self.intpc0}'
        text += '<br>'
        text += f'In TPC1 : {self.intpc1}'
        
        if VERBOSE: print(f'-MCPart {ind} : ({x1:.2f},{y1:.2f},{z1:.2f}) -> ({x2:.2f},{y2:.2f},{z2:.2f})')
        
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
            
        
        

        