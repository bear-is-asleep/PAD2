from utils.plotters import map_value_to_color
import pandas as pd
import plotly.graph_objects as go
from variables import *
import numpy as np
from time import time
from config.test import *

class PMT:
    def __init__(self, id, coating, tpc, location, waveform=None, op_pe=None, t1=t1, t0=t0, dt=dt):
        self.id = id
        self.coating = coating
        self.location = location
        self.waveform = waveform
        self.dt = dt
        self.tpc = tpc

        if op_pe is not None:
            self.op_pe = pd.DataFrame(op_pe)
            self.bins=np.arange(t0, t1+dt, dt)
            self.op_pe['time_bin'] = pd.cut(self.op_pe['op_time'], bins=self.bins,right=True,include_lowest=True)
            self.op_pe = self.op_pe.groupby('time_bin')['op_pe'].sum().reset_index()
        else:
            self.op_pe = None
            self.bins = None

    def plot_coordinates(self, start, end, cmap='magma', cmin=0, cmax=2000):
        """ 
        Plots PMTs onto PAD grid

        Args:
            start (_type_): start time window
            end (_type_): end time window
            cmap (str, optional): Defaults to 'magma'.
            cmin (int, optional): Defaults to 0.
            cmax (int, optional): Defaults to 10000.

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        #if VERBOSE: print('pds id : ',self.id)
        z = [self.location[2]]
        y = [self.location[1]]
        if self.id in [6,7]: 
            showscale = True
        else:
            showscale = False
        if self.op_pe is not None:
            s0 = time()
            start_ind = np.searchsorted(self.bins,start) 
            end_ind = np.searchsorted(self.bins,end)  -1
            if start_ind < end_ind:
                mask = np.full(len(self.op_pe),False)
                inds = list(range(start_ind,end_ind))
                mask[inds] = True
                color = self.op_pe.loc[mask, 'op_pe'].sum()
            else:
                color = 0
            if np.isnan(color):
                color = 0
        else:
            color = 0
        s1 = time()
        #if VERBOSE: print(f'-- time to bin {s1-s0:.3f} s')
        msize = 18
        hex_color = map_value_to_color(color,cmin,cmax,cmap=cmap)
        text = f'ID : {self.id:.0f}'
        text += '<br>'
        text += f'Coating : {self.coating:.2f}'
        text += '<br>'
        text += f'Cum. PE : {color:.2f}'
        # print('color : ',color)
        # print('hex : ',hex_color)
        sc = go.Scatter(
            x=z,
            y=y,
            mode='markers',
            marker=dict(
                size=msize,
                color=hex_color,
                colorscale=cmap,
                showscale=showscale,
                cmin=cmin,
                cmax=cmax,
            ),
            name=f'PMT {self.id}',
            customdata=[self.id],
            text=text,  # display the color value on hover
            hoverinfo='text+name',  # show the custom text and trace name on hover
        )
        s2 = time()
        #if VERBOSE: print(f'-- time to make scatter {s2-s1:.3f} s')
        return sc

    def plot_waveform(self):
        """
        Plots PMT waveform

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        if self.waveform is not None:
            return go.Scatter(
                x=self.waveform['time'],
                y=self.waveform['voltage'],
                mode='lines',
                name=f'Waveform for PMT {self.id}'
            )
        else:
            return None