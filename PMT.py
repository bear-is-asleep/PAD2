from utils.plotters import map_value_to_color
import pandas as pd
import plotly.graph_objects as go
from variables import *
import numpy as np
from time import time

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

    def get_pe_start_stop(self,start,end):
        """
        Get pe within start and stop times for bins

        Args:
            op_pe (pandas dataframe): contains two columns, 'time_bin' which are pd intervals, and op_pe which contain the pe for that time bin.
            bins (numpy array): time bins aranged in even intervals
            start (number): start time
            end (number): end time

        Returns:
            _type_: _description_
        """
        start_ind = np.searchsorted(self.bins,start) 
        end_ind = np.searchsorted(self.bins,end)
        if start_ind < end_ind:
            mask = np.full(len(self.op_pe),False)
            inds = list(range(start_ind,end_ind))
            mask[inds] = True
            color = self.op_pe.loc[mask, 'op_pe'].sum()
        else:
            color = 0
        if np.isnan(color):
            color = 0
        return color

    def plot_coordinates(self, start, end, pds_ids,cmap='magma', cmin=0, cmax=None):
        """ 
        Plots PMTs onto PAD grid

        Args:
            start (_type_): start time window
            end (_type_): end time window
            pds_ids (_type_): list of pds ids that are plotted
            cmap (str, optional): Defaults to 'magma'.
            cmin (int, optional): Defaults to 0.
            cmax (int, optional): Defaults to None.

        Returns:
            go.Scatter: scatter point to be plotted on dash canvas
        """
        #if VERBOSE: print('pds id : ',self.id)
        z = [self.location[2]]
        y = [self.location[1]]
        if self.id in pds_ids[:2]: #only set colorbar for first two pds ids to avoid duplication 
            showscale = True
        else:
            showscale = False
        color = self.get_pe_start_stop(start, end)
        s1 = time()
        #if VERBOSE: print(f'-- time to bin {s1-s0:.3f} s')
        msize = 14
        hex_color = map_value_to_color(color,cmin,cmax,cmap=cmap)
        text = f'ID : {self.id:.0f}'
        text += '<br>'
        text += f'Coating : {self.coating:.0f}'
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